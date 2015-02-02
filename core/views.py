import oauth2 as oauth
import cgi
import logging
import os
import httplib2
import urllib
import json



from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.shortcuts import redirect

from core.forms import RegistrationForm

request_token_url = 'https://twitter.com/oauth/request_token'
authenticate_url = 'https://twitter.com/oauth/authenticate'
access_token_url = 'https://twitter.com/oauth/access_token'

LOGFILE = os.path.join(settings.BASE_DIR, 'log.log')

logging.basicConfig(
    filename=LOGFILE,
    format='[%(asctime)s] %(message)s',
    level=logging.DEBUG)


#def fblogin(request):
#    if request.method == 'POST':
#        form = RegistrationForm(request.POST)
#        if form.is_valid():
#            email = form.cleaned_data['email']
#            name = form.cleaned_data['name']
#            pwd = form.cleaned_data['pwd'][:100]
#            try:
#                user = User.objects.get(username=email)
#                # need to reset password or it won't authenticate
#                user.set_password(pwd)
#                user.save()
#            except User.DoesNotExist:
#                user = User.objects.create_user(
#                    email, email=email, password=pwd)
#                user.first_name = name
#                user.save()
#            usr = authenticate(username=email, password=pwd)
#            login(request, usr)
#            return HttpResponse('Ok')
#    return HttpResponse('Bad')


def fblogin(request):
    params = {
        'redirect_uri': request.build_absolute_uri('/facebook'),
        'client_id': settings.FB_CLIENT_ID
    }
    base_url = 'https://graph.facebook.com/oauth/authorize?'
    return redirect(base_url + urllib.urlencode(params))


def fbauthenticated(request):
    token_url = 'https://graph.facebook.com/oauth/access_token?'
    code = request.GET.get('code')
    if code:
        params = {
            'client_id': settings.FB_CLIENT_ID,
            'redirect_uri': request.build_absolute_uri('/facebook'),
            'code': code,
            'client_secret': settings.FB_APP_SECRET,
        }
    resp = urllib.urlopen(token_url + urllib.urlencode(params))
    data = cgi.parse_qs(resp.read())
    logging.info(data)
    access_token = data['access_token'][-1]

    #profile
    params = urllib.urlopen(dict(access_token=access_token))
    profile = json.load(urllib.urlopen(
        'https://graph.facebook.com/me?' + params))
    logging.info(profile)


def twtlogin(request):
    consumer = oauth.Consumer(
        key=settings.CONSUMER_KEY, secret=settings.CONSUMER_SECRET)
    client = oauth.Client(consumer)

    # Request token url

    resp, content = client.request(request_token_url, "GET")
    logging.info("content: {}".format(content))
    if resp['status'] != '200':
        return HttpResponse('crap')
    request.session['twitter_token'] = dict(cgi.parse_qsl(content))

    url = "%s?oauth_token=%s" % (
        authenticate_url,
        request.session['twitter_token']['oauth_token'])

    return HttpResponseRedirect(url)


def twtauthenticated(request):
    logging.info("content: {}".format(request.GET))
    verifier = request.GET.get('oauth_verifier')
    consumer = oauth.Consumer(
        key=settings.CONSUMER_KEY, secret=settings.CONSUMER_SECRET)

    token = oauth.Token(
        request.session['twitter_token']['oauth_token'],
        request.session['twitter_token']['oauth_token_secret'])
    token.set_verifier(verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, 'GET')
    if resp['status'] != '200':
        return HttpResponse('Could not log you in. Please go back')
        #return HttpResponse('Invalid response from Twitter')
    access_token = dict(cgi.parse_qsl(content))

    name = access_token['screen_name']
    email = '{}@twitter.com'.format(name)
    pwd = access_token['oauth_token']
    try:
        user = User.objects.get(username=email)
        # need to reset password or it won't authenticate
        user.set_password(pwd)
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            email, email=email, password=pwd)
        user.first_name = name
        user.save()
    usr = authenticate(username=email, password=pwd)
    login(request, usr)
    return redirect('profile')


def gplogin(request):
    redirect_uri = request.build_absolute_uri('/gplus')
    scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    params = {
        'token_url': 'https://accounts.google.com/o/oauth2/auth',
        'client_id': settings.GPLUS_CLIENT_KEY,
        'scope': scope,
        'redirect_uri': redirect_uri
    }
    url = '{token_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'.format(**params)
    print url
    return redirect(url)


def gpauthenticated(request):
    parser = httplib2.Http()
    if 'error' in request.GET or 'code' not in request.GET:
        return redirect('home')
    access_uri = 'https://accounts.google.com/o/oauth2/token'
    #profile_uri = 'https://www.googleapis.com/oauth2/v1/userinfo?'
    profile_uri = 'https://www.googleapis.com/plus/v1/people/me'
    redirect_uri = request.build_absolute_uri('/gplus')
    params = urllib.urlencode({
        'code': request.GET['code'],
        'redirect_uri': redirect_uri,
        'client_id': settings.GPLUS_CLIENT_KEY,
        'client_secret': settings.GPLUS_CLIENT_SECRET,
        'grant_type': 'authorization_code'})
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    resp, content = parser.request(
        access_uri, method='POST', body=params, headers=headers)
    if resp['status'] != '200':
        return HttpResponse(
            'Google could not log you in, please try again later')
    access_token = json.loads(content)

    resp, content = parser.request(
        '{uri}?access_token={token}'.format(
            uri=profile_uri, token=access_token['access_token']))
    if resp['status'] != '200':
        return HttpResponse(
            'Google could not log you in, please try again later')
    profile = json.loads(content)
    name = profile['displayName']
    emails = profile['emails']
    if emails:
        email = emails[0]['value']
    else:
        email = '{name}@gplus.com'.format(name=name)
    pwd = access_token['access_token']

    try:
        user = User.objects.get(username=email)
        # need to reset password or it won't authenticate
        user.set_password(pwd)
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            email, email=email, password=pwd)
        user.first_name = name
        user.save()
    usr = authenticate(username=email, password=pwd)
    login(request, usr)

    return redirect('/profile')
