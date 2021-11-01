from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View
import requests
import praw
import pandas as pd
import datetime as dt
import time
import os
import dotenv
from psaw import PushshiftAPI

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'api/home.html')

def dataget(request):

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(os.environ.get('CLIENT_ID'), os.environ.get('SECRET_TOKEN'))
    print(os.environ['CLIENT_ID'])

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': os.environ.get('USERNAME'),
            'password': os.environ.get('PASSWORD')}

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'radditbot/0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    print("Token => ", res.json()['access_token'])

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    # a = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    # a = requests.get('https://oauth.reddit.com/r/Home/', headers=headers)
    a = requests.get('https://www.reddit.com/subreddits.json')
    print(a)
    return JsonResponse({"Data": a.json()})


def test_data(request):
    api = PushshiftAPI()
    most_recent_subs = api.search_submissions(limit=1000)
    # results = (most_recent_subs)
    return   HttpResponse( most_recent_subs)