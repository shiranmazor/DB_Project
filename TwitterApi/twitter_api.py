import sys
sys.path.append("twitter.egg")
from twitter import *
import datetime
import re
import csv
from consts import *
import traceback
from ServerLogic.common import *


class Twitter_Api():
    '''
    implemet twitter api relevent functions
    important dicts: name_to_screen,screen_to_name,users_id_to_screen_name
    '''
    def __init__(self):
        #self.name_to_screen = {}
        #self.screen_to_name = {}
        self.t = Twitter(auth=OAuth(TOKEN, TOKEN_KEY, CON_SECRET, CON_SECRET_KEY))
        #load users to dict
        self.users_id_to_screen_name = {}




    def get_hoc_users_id(self):
        '''
        fill in the dict that connect user id to screen name
        :return:
        '''
        for screen_name in screen_to_name:
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
            mentions = [u_m["screen_name"].encode('utf-8') for u_m in item["entities"]["user_mentions"] if u_m["screen_name"] in screen_to_name]
            # Search the text for more mentions
            for real_name in name_to_screen:
                if real_name in text:
                    mentions.append(screen_to_name[real_name])

            temp_dict = {"id": item["id"], "text": text, "mentions": mentions, "time": create_time}
            result.append(temp_dict)
        return result



    def get_timeline_only(self,screen_name= None, user_id = None, count=500, since_id = None):
        '''
        get only x last record of tweets from a specific screen name
        :param screen_name:
        :param since_id: Returns results with an ID greater than (that is, more recent than) the specified ID.
        :param count:
        :return:list of dict : {"tweet_id": item["id"], "text": text, "mentions": mentions, "time": create_time,
         "urls":urls, "tweet_files":tweet_files_data}
        '''
        result=[]
        output_dict={}
        if screen_name:
            if since_id:
                output_dict = self.t.statuses.user_timeline(screen_name=screen_name, count=count, trim_user=True,
                                                            include_rts=True, since_id=since_id)
            else:
                output_dict = self.t.statuses.user_timeline(screen_name=screen_name, count=count, trim_user=True,
                                                    include_rts=True)
        elif user_id:
            if since_id:
                output_dict = self.t.statuses.user_timeline(user_id=user_id, count=count, trim_user=True,
                                                            include_rts=True, since_id=since_id)
            else:
                output_dict = self.t.statuses.user_timeline(user_id =user_id, count=count, trim_user=True,
                                                        include_rts=True)
        for item in output_dict:
            mentions = []
            create_time = datetime.datetime.strptime(re.sub(r"[+-]([0-9])+", "", str(item["created_at"])),
                                                     "%a %b %d %H:%M:%S %Y")

            text = item["text"].encode('utf-8')
            #remove hex data from text:
            text = remove_hexa_bytes(text)
            # Add twitter account tagged only if screen name exists in CSV
            urls = []
            user_mentions = []
            if item['entities'].has_key("user_mentions"):
                user_mentions = item['entities']['user_mentions']
            if item['entities'].has_key("urls"):
                tweet_urls = item['entities']["urls"]
                for url_dict in tweet_urls:
                    urls.append(url_dict["url"])

            mentions.extend(user_mentions)
            #get all pictures and media
            tweet_files_data = [] #list of dict with all the relevet fields
            if  item['entities'].has_key("media"):
                medias = item['entities']["media"]
                for media in medias:
                    file_dict = {}
                    file_dict['file_url'] = media['media_url']
                    file_dict['file_type'] = media['type']
                    file_dict['tweet_id'] = media['id']
                    tweet_files_data.append(file_dict)

            temp_dict = {"tweet_id": item["id"], "text": text, "mentions": mentions, "time": create_time, "urls":urls, "tweet_files":tweet_files_data}
            result.append(temp_dict)

        return result

    def get_userid_by_screen_name(self,screen_name):
        output = self.t.users.show(screen_name=screen_name)
        if output.has_key("id"):
            return long(output["id"])
        else :
            return -1

    def get_relationship(self,use_id = True,source_id = None, source_screen_name = None, target_id = None,
                         target_screen_name = None):
        '''
        Returns detailed information about the relationship between two arbitrary users.
        :param use_id:
        :param source_id:
        :param source_screen_name:
        :param target_id:
        :param target_screen_name:
        :return:
        '''
        if use_id:
            output = self.t.friendships.show(source_id = source_id, target_id = target_id)
        else:
            output = self.t.friendships.show(source_screen_name=source_screen_name, target_screen_name=target_screen_name)
        return output

    def get_user_data(self, screen_name = None, userid=None):
        '''
        return user full data by screen name or id
        :param screen_name:
        :return:dict - twitter_id,screen_name,description,location,followers_count,friends_count,name,profile_image_url
        '''
        try:
            output = {}
            result = {}
            if screen_name:
                output = self.t.users.show(screen_name=screen_name)
            elif id:
                output = self.t.users.show(user_id=str(userid))

            result['twitter_id'] = output['id']
            result['screen_name'] = output['screen_name']
            result['description'] = output['description']
            result['location'] = output['location']
            result['followers_count'] = output['followers_count']
            result['friends_count'] = output['friends_count']
            result['full_name'] = output['name']
            result['profile_picutre_url'] = output['profile_image_url']
            return result
        except Exception as Ex:
            print traceback.format_exc()
            return {}


    def get_user_followees(self, screen_name = None, user_id = None, count = 5000, cursor = False):
        '''
        return list of user ids the user is following - followees
        :param screen_name:
        :param user_id:
        :param count:
        :return: list
        '''
        ids = []
        output = {}
        if screen_name:
            output = self.t.friends.ids(screen_name=screen_name)
            if len(output) > 0:
                ids = output["ids"]
                if cursor:
                    c = output['next_cursor']
                    while (c != 0):
                        ids.extend(output["ids"])
                        output = self.t.friends.ids(screen_name=screen_name, cursor = c)
        elif user_id:
            output = self.t.friends.ids(user_id=user_id, count=count)
            if len(output) > 0:
                ids = output["ids"]
                if cursor:
                    c = output['next_cursor']
                    while (c != 0):
                        ids.extend(output["ids"])
                        output = self.t.friends.ids(user_id=user_id, cursor=c)

        return ids

    def get_user_followers(self, screen_name = None, user_id = None, count = 5000, cursor = False):
        ids = []
        output = {}
        if screen_name:
            output = self.t.followers.ids(screen_name=screen_name)
            if len(output) > 0:
                ids = output["ids"]
                if cursor:
                    c = output['next_cursor']
                    while (c != 0):
                        ids.extend(output["ids"])
                        output = self.t.followers.ids(screen_name=screen_name, cursor = c)
        elif user_id:
            output = self.t.followers.ids(user_id=user_id)
            if len(output) > 0:
                ids = output["ids"]
                if cursor:
                    c = output['next_cursor']
                    while (c != 0):
                        ids.extend(output["ids"])
                        output = self.t.followers.ids(user_id=user_id,  cursor = c)


        return ids


    def get_user_retweets(self, user_id):
        output = self.t.statuses.retweets(id = user_id)
        return output