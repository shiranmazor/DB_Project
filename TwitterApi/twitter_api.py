from twitter import *
import datetime
import re
import csv
from consts import *

csv_path = r'../Utillities/Congress.csv'

# Constant app parameters from Mattan's account


t = Twitter(auth=OAuth(TOKEN, TOKEN_KEY, CON_SECRET, CON_SECRET_KEY))

# Generate real name to screen name and vice versa dicts

real_to_screen = {}
screen_to_real = {}

with open(csv_path, 'rb') as csvfile:
    csv_data = csv.DictReader(csvfile)
    for row in csv_data:
        real_name = row["real_name"]
        screen_name = row["screen_name"]
        if real_name != "" and screen_name != "":
            real_to_screen[real_name] = screen_name
            screen_to_real[screen_name] = real_name

# Input: twitter screen name, datetime object limit (optional)
# Output: list of latest 200 tweets as dicts with 4 fields:
## id - long number tweet id
## text - tweet text
## mentions - political screen names mentioned in the tweet
## time - datetime object of creation time

def get_timeline(screen_name, datetime_limit=None,count=200):
    d = t.statuses.user_timeline(screen_name=screen_name, count=count, trim_user=True, include_rts=True)
    result = []
    for item in d:
        create_time = datetime.datetime.strptime(re.sub(r"[+-]([0-9])+", "", str(item["created_at"])),"%a %b %d %H:%M:%S %Y")
        if datetime_limit is not None and create_time <= datetime_limit:
            break # Reached datetime limit, older posts are irrelevant
        text = item["text"].encode('utf-8')
        # Add twitter account tagged only if screen name exists in CSV
        mentions = [u_m["screen_name"].encode('utf-8') for u_m in item["entities"]["user_mentions"] if u_m["screen_name"] in screen_to_real]
        # Search the text for more mentions
        for real_name in real_to_screen:
            if real_name in text:
                mentions.append(real_to_screen[real_name])
        
        temp_dict = {"id": item["id"], "text": text, "mentions": mentions, "time": create_time}
        result.append(temp_dict)
    return result

# Input: twitter screen name
# Output: latest 5000 political ***twitter ids*** (as long numbers) this user has followed

def get_followees(screen_name):
    d = t.friends.ids(screen_name=screen_name, count=5000)["ids"]

get_timeline(screen_name='shiranmazor1')