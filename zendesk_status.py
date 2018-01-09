from slackclient import SlackClient
import requests
import os

slack_token = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(slack_token)


#Get updates from Zendesk
zd_text = requests.get('https://status.zendesk.com/api/internal/incidents.json').text
zd_text = zd_text[22:-2]
#parse string
if len(zd_text) > 0:
	#post to slack
	sc.api_call(
  	"chat.postMessage",
  	channel="#chat",
  	text=("*Zendesk Status Update: *" + zd_text)
	)
	##Will need to add date handling (and probably text stripping) once a 
	##status update happens and we know how it actually looks


updates.close()