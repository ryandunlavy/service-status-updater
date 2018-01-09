from slackclient import SlackClient
import tweepy
import os

slack_token = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(slack_token)

updates = open('updates.txt', 'r+')
updates.seek(20)
gh_date = updates.read(19)
updates.seek(0)


#Get updates from GitHub
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

tweepy_api = tweepy.API(auth)

latest_tweet = tweepy_api.user_timeline(screen_name = 'githubstatus',count=1)[0]
update_str = str(latest_tweet.created_at)

if update_str != gh_date:
	#post to slack
	sc.api_call(
  	"chat.postMessage",
  	channel="#chat",
  	text=("*GitHub Status Update:* " + latest_tweet.text)
	)
	#add date to updates.txt
	updates.seek(20)
	updates.write(update_str)


updates.close()