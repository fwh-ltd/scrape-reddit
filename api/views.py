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
    reddit = praw.Reddit(client_id='PwzYIOrHfdlKkPGD7ThIEw', \
                     client_secret='pYMG5FBScurIhDku1jYGtbYD5RUSIw ', \
                     user_agent='radditbot', \
                     username='sunilpragroot', \
                     password='Rajput@1996')
    subreddit = reddit.subreddit('Nootropics')
    # subreddit = reddit.subreddit()
    top_subreddit = subreddit.top(limit=50)
    print(top_subreddit)
    topics_dict = { "title":[], 
                "score":[], 
                "id":[], "url":[], 
                "comms_num": [], 
                "created": [], 
                "body":[]}
    # for submission in top_subreddit:
    #     topics_dict["title"].append(submission.title)
    #     topics_dict["score"].append(submission.score)
    #     topics_dict["id"].append(submission.id)
    #     topics_dict["url"].append(submission.url)
    #     topics_dict["comms_num"].append(submission.num_comments)
    #     topics_dict["created"].append(submission.created)
    #     topics_dict["body"].append(submission.selftext)
    # topics_data = pd.DataFrame(topics_dict)
    # print("==> ", topics_data)
    # # for i in reddits:
    # #     print("=> ", i)
    print("=====================> : <=====================")
    for submission in subreddit.top(limit=1):
        print("=> ", submission.title, submission.id)
    return JsonResponse({"Data": "Ok"})
