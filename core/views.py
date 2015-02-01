import oauth2 as oauth
import cgi
import logging
import os
import httplib

httplib.HTTPConnection.debuglevel = 1


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
#LOGFILE = 'log.log'

logging.basicConfig(
    filename=LOGFILE,
    format='[%(asctime)s] %(message)s',
    level=logging.DEBUG)


def fblogin(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            pwd = form.cleaned_data['pwd'][:100]
            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email, email=email, password=pwd)
                user.first_name = name
                user.save()
            usr = authenticate(username=email, password=pwd)
            login(request, usr)
            return HttpResponse('Ok')
    return HttpResponse('Bad')


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
        return HttpResponse(content + str(resp))
        #return HttpResponse('Invalid response from Twitter')
    access_token = dict(cgi.parse_qsl(content))

    name = access_token['screen_name']
    email = '{}@twitter.com'.format(name)
    pwd = access_token['oauth_token']
    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            email, email=email, password=pwd)
        user.first_name = name
        user.save()
    usr = authenticate(username=email, password=pwd)
    login(request, usr)
    return redirect('profile')
