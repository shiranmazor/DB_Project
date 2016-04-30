from twitter import *
import datetime
import re
import csv
from consts import *


class Twitter_Api():
    def __init__(self):
        self.name_to_screen = {}
        self.screen_to_name = {}
        self.t = Twitter(auth=OAuth(TOKEN, TOKEN_KEY, CON_SECRET, CON_SECRET_KEY))
        #load users to dict
        self.load_users_from_csv()
        self.users_id_to_screen_name = {}


    def load_users_from_csv(self):
        with open(CSV_PATH, 'rb') as csvfile:
            csv_data = csv.DictReader(csvfile)
            for row in csv_data:
                real_name = row["real_name"]
                screen_name = row["screen_name"]
                if real_name != "" and screen_name != "":
                    self.name_to_screen[real_name] = screen_name
                    self.screen_to_name[screen_name] = real_name

    def get_hoc_users_id(self):
        '''
        fill in the dict that connect user id to screen name
        :return:
        '''
        for screen_name in self.screen_to_name:
            user_id = self.get_userid_by_screen_name(screen_name==screen_name)
            self.users_id_to_screen_name[user_id] = screen_name




    def get_timeline(self,screen_name, datetime_limit=None,count=200):
        '''
        Input: twitter screen name, datetime object limit (optional)
        :param screen_name:
        :param datetime_limit:
        :param count:
        :return: list of latest 200 tweets as dicts with 4 fields:
                 id - long number tweet id
                  text - tweet text
                  mentions - political screen names mentioned in the tweet
                  time - datetime object of creation time
        '''
        d = self.t.statuses.user_timeline(screen_name=screen_name, count=count, trim_user=True, include_rts=True)
        result = []
        for item in d:
            create_time = datetime.datetime.strptime(re.sub(r"[+-]([0-9])+", "", str(item["created_at"])),"%a %b %d %H:%M:%S %Y")
            if datetime_limit is not None and create_time <= datetime_limit:
                break # Reached datetime limit, older posts are irrelevant
            text = item["text"].encode('utf-8')
            # Add twitter account tagged only if screen name exists in CSV
            mentions = [u_m["screen_name"].encode('utf-8') for u_m in item["entities"]["user_mentions"] if u_m["screen_name"] in self.screen_to_name]
            # Search the text for more mentions
            for real_name in self.name_to_screen:
                if real_name in text:
                    mentions.append(self.screen_to_name[real_name])

            temp_dict = {"id": item["id"], "text": text, "mentions": mentions, "time": create_time}
            result.append(temp_dict)
        return result

    def get_followees(self,screen_name, count= 5000):
        '''

        :param screen_name:
        :return:latest 5000 political ***twitter ids*** (as long numbers) this user has followed

        '''
        d = self.t.friends.ids(screen_name=screen_name, count=count)["ids"]


    def get_timeline_only(self,screen_name, count):
        '''
        get only x last record of tweets from a specific screen name
        :param screen_name:
        :param count:
        :return:list of dict
        '''
        result=[]
        output_dict = self.t.statuses.user_timeline(screen_name=screen_name, count=count, trim_user=True, include_rts=True)
        for item in output_dict:
            create_time = datetime.datetime.strptime(re.sub(r"[+-]([0-9])+", "", str(item["created_at"])),
                                                     "%a %b %d %H:%M:%S %Y")

            text = item["text"].encode('utf-8')
            # Add twitter account tagged only if screen name exists in CSV
            mentions =[]

            temp_dict = {"id": item["id"], "text": text, "mentions": mentions, "time": create_time}
            result.append(temp_dict)
        return result

    def get_userid_by_screen_name(self,screen_name):
        output = self.t.users.show(screen_name=screen_name)
        if output.has_key("id"):
            return long(output["id"])
        else :
            return -1

    def get_user_data(self, screen_name = None, userid=None):
        '''
        return user full data by screen name or id
        :param screen_name:
        :return:dict - id,screen_name,description,location,followers_count,friends_count,name,profile_image_url
        '''
        output = {}
        result = {}
        if screen_name:
            output = self.t.users.show(screen_name=screen_name)
        elif id:
            output = self.t.users.show(user_id=str(userid))

        result['id'] = output['id']
        result['screen_name'] = output['screen_name']
        result['description'] = output['description']
        result['location'] = output['location']
        result['followers_count'] = output['followers_count']
        result['friends_count'] = output['friends_count']
        result['name'] = output['name']
        result['profile_image_url'] = output['profile_image_url']
        return result

    def get_user_retweets(self, user_id):
        output = self.t.statuses.retweets(id = user_id)
        return output