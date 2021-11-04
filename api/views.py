import json
import os
import requests
import time
from bs4 import BeautifulSoup

def write_to_file(data, **kwargs):
    '''Writes a string to a file'''
    global json_file_path
    end = kwargs.pop('end', False)
    if end:
        # once we're at the end of the script, remove the trailing ", "
        with open(json_file_path, 'rb+') as f:
            f.seek(-2, os.SEEK_END)
            f.truncate()
    with open(json_file_path, 'a') as f:
        f.write(data)


def output_subreddits(num_of_subs):
    '''Writes the subreddits to the file you specified'''
    subreddits_url = "http://www.reddit.com/reddits"
    after = ""
    count = 0

    # required by reddit's API rules
    headers = {'User-agent': 'platform:appID:version (by u/username)'}

    while (after is not None) and count < num_of_subs:
        url = "%s.json?limit=125&after=%s" % (subreddits_url, after)
        print(url)
        response = requests.get(url, headers=headers)
        data = response.json()['data']

        for child in data['children']:
            subreddit = child['data']['display_name']
            write_to_file('"%s", ' % subreddit)
        
        count += 125
        
        # used to get the next page of subreddits
        after = data['after']
        # required by reddit's API rules
        time.sleep(2)

# ==== CONFIGURATION ==== #
# the path to your json file
json_file_path = "./filename.json"
# the number of subreddits you want
subreddit_cap = 20000

# ==== MAIN THINGY ==== #
write_to_file("[")
output_subreddits(subreddit_cap)
write_to_file("]", end=True)
print("DONE!")
for i in range(1,36):
    res=requests.get("http://redditlist.com/?page=%s" %(i) )
    # print(soup.text)
    soup=BeautifulSoup(res.text,'html.parser')
    all_reddit_name=(soup.find_all('span',{'class':'subreddit-url'}))
    for one_reddit_name in all_reddit_name:
        # print(one_reddit_name.text)
        reddit_name_list.append(one_reddit_name.text)
    print(len(reddit_name_list))    

    

reddit = praw.Reddit(client_id='PwzYIOrHfdlKkPGD7ThIEw', client_secret='pYMG5FBScurIhDku1jYGtbYD5RUSIw', user_agent='radditbot/0.0.1')
hot_posts = reddit.subreddit('Home')
# ml_subreddit = reddit.subreddit('MachineLearning')
posts=[]
for post in hot_posts.hot(limit=1):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])

print(posts)