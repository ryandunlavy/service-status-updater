from slackclient import SlackClient
import time
import feedparser as fp
import os

slack_token = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(slack_token)

updates = open('updates.txt', 'r+')
aws_date = updates.read(19)
updates.seek(0)

#Get updates from AWS
d = fp.parse('https://status.aws.amazon.com/rss/ec2-us-east-1.rss')
update_str = time.strftime('%Y-%m-%d %H:%M:%S', d.entries[0].published_parsed)
if update_str != aws_date:
	#post to slack
	sc.api_call(
  	"chat.postMessage",
  	channel="#chat",
  	text=("*AWS Status Update: *" + d.entries[0].description)
	)
	#add date to updates.txt
	updates.seek(0)
	updates.write(update_str)

updates.close()