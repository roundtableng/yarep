import oauth2 as oauth
import cgi
import logging
import os
import httplib2
import urllib
import json
from datetime import datetime

from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from reps.models import State, LGA
from core.models import Account
from core.forms import LoginForm, TopicForm, PostForm
from pybb.models import Topic, Forum, Post

request_token_url = 'https://twitter.com/oauth/request_token'
authenticate_url = 'https://twitter.com/oauth/authenticate'
access_token_url = 'https://twitter.com/oauth/access_token'

LOGFILE = os.path.join(settings.BASE_DIR, 'log.log')

logging.basicConfig(
    filename=LOGFILE,
    format='[%(asctime)s] %(message)s',
    level=logging.DEBUG)


def get_default_forum():
    forums = Forum.objects.all()
    if not forums:
        raise NotImplementedError('You need to create a forum')
    else:
        return forums[0]


def login_user(request, name, email, password):
    try:
        user = User.objects.get(username=email)
        user.set_password(password)
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(email, email=email, password=password)
        user.first_name = name
        user.save()
    usr = authenticate(username=email, password=password)
    login(request, usr)


def fblogin(request):
    params = {
        'redirect_uri': request.build_absolute_uri('/facebook'),
        'client_id': settings.FB_CLIENT_ID,
        'scope': 'public_profile,email',
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
    access_token = data['access_token'][-1]

    #profile
    params = urllib.urlencode(dict(access_token=access_token))
    profile = json.load(urllib.urlopen(
        'https://graph.facebook.com/me?' + params))
    login_user(request, profile['name'], profile['email'], profile['id'])
    return redirect('profile')


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
    login_user(request, name, email, pwd)
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
    return redirect(url)


def gpauthenticated(request):
    parser = httplib2.Http()
    if 'error' in request.GET or 'code' not in request.GET:
        return redirect('home')
    access_uri = 'https://accounts.google.com/o/oauth2/token'
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

    login_user(request, name, email, pwd)
    return redirect('/profile')


@login_required
def profile(request):
    if not request.user.account.lga:
        return redirect('select_lga')
    forum = get_default_forum()
    # Get topics of forum
    topics = Topic.objects.filter(forum=forum)
    return render(
        request,
        'core/profile.html',
        {'topics': topics, 'forum_id': forum.pk}
    )


def select_lga(request):
    if request.method == 'POST':
        lga_id = request.POST.get('lga')
        lga = LGA.objects.get(pk=lga_id)
        account, _ = Account.objects.get_or_create(user=request.user)
        account.lga = lga
        account.save()
        return redirect('profile')
    return render(
        request,
        'core/select_lga.html',
        {
            'states': State.objects.all()
        })


def get_lgas(request):
    state_id = request.GET.get('state')
    state = State.objects.get(pk=state_id)
    json_data = serialize('json', state.lga_set.all())
    return HttpResponse(json_data)


def home(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'core/home.html', {'form': form})


def replist(request):
    return render(request, 'core/replist.html', {'lgas': LGA.objects.all()})


@login_required
def new_topic(request):
    now = datetime.now()
    forum = get_default_forum()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            post = form.cleaned_data['post']
            new_topic = Topic.objects.create(
                name=name,
                forum=forum,
                created=now,
                updated=now,
                user=request.user)
            Post.objects.create(
                topic=new_topic,
                user=request.user,
                created=now,
                updated=now,
                body=post,
                body_html=post,
                body_text=post)
            return redirect('profile')
    else:
        form = TopicForm()
    return render(request, 'core/add_topic.html', {'form': form})


@login_required
def topic(request, topic_id):
    now = datetime.now()
    topic = get_object_or_404(Topic, pk=topic_id)
    posts = Post.objects.filter(topic=topic)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.cleaned_data['post']
            Post.objects.create(
                topic=topic,
                user=request.user,
                created=now,
                updated=now,
                body=post,
                body_html=post,
                body_text=post)
            return redirect('profile')
    else:
        form = PostForm()
    return render(
        request,
        'core/topic.html',
        {
            'form': form,
            'topic': topic,
            'posts': posts
        })
