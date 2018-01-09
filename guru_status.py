from slackclient import SlackClient
import time
import feedparser as fp
import os
import string

slack_token = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(slack_token)

updates = open('updates.txt', 'r+')
updates.seek(40)
guru_date = updates.read(19)
updates.seek(0)

#Get updates from Guru

d = fp.parse('http://status.getguru.com/history.rss')
guru_text = str(d.entries[0])
latest_date = time.strftime('%Y-%m-%d %H:%M:%S', d.entries[0].published_parsed)
#parse text
guru_text = guru_text.split("<p>")[1]
guru_text = string.replace(guru_text, '<small>', '')
guru_text = string.replace(guru_text, '</small><br />', ' - ')
guru_text = string.replace(guru_text, '<strong>', '*')
guru_text = string.replace(guru_text, '</strong>', '*')
guru_text = string.replace(guru_text, '</p>', '')
#check if update is new
if latest_date != guru_date:
	#post to slack
	sc.api_call(
  	"chat.postMessage",
  	channel="#chat",
  	text=("*Guru Status Update:* " + guru_text)
	)
	#add date to updates.txt
	updates.seek(40)
	updates.write(latest_date)

updates.close()