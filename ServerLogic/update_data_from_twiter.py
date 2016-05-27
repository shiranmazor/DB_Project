'''
this module contain functions for updating data from twitter api
- insert new users that are not in DB
- update all users from screch - maybe
- update followers
- update tweets - from specific date!
'''
import sys
import time
from TwitterApi.twitter_api import *
from DB.db_wrapper import *
from DB.db_logic import *
from ServerLogic.common import *
import traceback
import argparse

db_obj = DbWrapper()
db_logic = DBLogic(db_wrapper_obj=db_obj)
twiter_obj = Twitter_Api()

def add_uew_users():
    '''
    this function  gets all existing users from DB and extract all the new users from csv that are not in users table
    connect twitter api, get the information and insert to users table
    :return:
    '''
    sleeping_time = 60 * 20  # 16minutes
    requests_limit = 120  # the limit is 180 requests
    request_counter = 0
    #get existing users
    users_id_screen_name = db_logic.get_userid_screen_name_db()
    existing_screen_names = [x['screen_name'] for x in users_id_screen_name]
    new_users = []
    for screen_name in users_data:
        if screen_name not in existing_screen_names:
            new_users.append(users_data[screen_name])

    #inserting new users to users table:
    for screen_name in new_users:
        print 'inserting user {0]'.format(screen_name)
        try:
            if request_counter == requests_limit:
                print 'reach requests limit sleeping for {0} seconds starting from {1}'.format(sleeping_time,
                                                                                               datetime.datetime.now())
                time.sleep(sleeping_time)
                request_counter = 0

            user_output = twiter_obj.get_user_data(screen_name=screen_name)
            request_counter += 1
            if len(user_output) > 0:
                fields = ['full_name', 'screen_name', 'description', 'location', 'followers_count', 'friends_count',
                          'twitter_id', 'profile_picture_url', 'role_id', 'party_id']

                # getting rol_id and party_id value
                party_id, role_id = get_party_role_id(db_obj, screen_name)

                values = [user_output['full_name'], user_output['screen_name'], user_output['description'],
                          user_output['location'], user_output['followers_count'], user_output['friends_count'],
                          user_output['twitter_id'], user_output['profile_picutre_url'], role_id, party_id]

                db_obj.insert_to_table(table_name='Users', fields=fields, values=values)
                print 'insert user {0}'.format(screen_name)
            else:
                print 'problem getting user data on {0}'.format(screen_name)
                print traceback.format_exc()

        except:
            print 'problem inserting user {0}'.format(screen_name)
            print traceback.format_exc()

def update_followers():
    '''
    1. for each user in db - select all followers from followers table and get last followers and update in DB if not exist
    or each user in db - select all friends from followers table and get last friends and update in DB if not exist
    :return:
    '''
    users_id_screen_name = db_logic.get_userid_screen_name_db()
    existing_screen_names = [x['screen_name'] for x in users_id_screen_name]
    ids_lst = [x['id'] for x in users_id_screen_name]

    sleeping_time_followers = 60 * 20  # 16 minutes
    requests_limit_followers = 15  # the limit is 180 requests
    request_counter_followers = 0

    for user_id in ids_lst:
        try:

            #get all followers:
            followers = db_obj.get_values_by_field( table_name = 'followers', field_name = 'followee_id', field_value = user_id)
            followees = db_obj.get_values_by_field( table_name = 'followers', field_name = 'follower_id', field_value = user_id)
            if request_counter_followers >= requests_limit_followers:
                print 'reaching request limit on followers ans friends sleeping for {0} seconds from {1}'. \
                    format(sleeping_time_followers, datetime.datetime.now())
                request_counter_followers = 0
                time.sleep(sleeping_time_followers)

            ##### followers!!
            print 'insert new followers!'
            request_counter_followers += 1
            followers_twitter_ids = twiter_obj.get_user_followers(user_id=user_id, cursor=True)
            for t_follower in followers_twitter_ids:#new follower must be in out users list
                user_data = db_logic.get_user_data_by_twitter_id(twitter_id=t_follower)
                if len(user_data) == 0:
                    continue
                else:
                    followee_id = user_id
                    follower_user_id = user_data[0]['id']
                    if follower_user_id not in followers:
                        fields = ['follower_id', 'followee_id']
                        values = [follower_user_id, followee_id]
                        try:
                            db_obj.insert_to_table(table_name='followers', fields=fields, values=values)
                        except:
                            # in case the tuple was already exist!
                            pass

            ##### friends
            print 'insert new followees!'
            request_counter_followers += 1
            followees_twitter_ids = twiter_obj.get_user_followees(user_id=user_id, cursor=True)
            for t_followee in followees_twitter_ids:  # new followee must be in out users list
                user_data = db_logic.get_user_data_by_twitter_id(twitter_id=t_followee)
                if len(user_data) == 0:
                    continue
                else:
                    follower_id = user_id
                    followee_user_id = user_data[0]['id']
                    if followee_user_id not in followees:
                        fields = ['follower_id', 'followee_id']
                        values = [follower_id, followee_user_id]
                        try:
                            db_obj.insert_to_table(table_name='followers', fields=fields, values=values)
                        except:
                            # in case the tuple was already exist!
                            pass

        except:
            pass

def update_Tweets(all = False, users = None,from_date = None):
    '''
    this function update tweets, tweets_files, mentions table
    from specific date or from the last
    :param all: update tweets for all users
    :param users: list of users to update - list contain
    :param from_date: optional, if none - the update will be from the last data of the tweet
    :return:
    '''
    sleeping_time = 60 * 20  # 16minutes
    requests_limit = 150  # the limit is 180 requests
    request_counter = 0
    # get all users id and screen_name from db
    users_info = db_logic.get_userid_screen_name_db()
    existing_screen_names = [x['screen_name'] for x in users_info]
    ids_lst = [x['id'] for x in users_info]
    if all:
        print 'update tweets for all users'
        # get the max tweet date from tweet table by user and update his tweets from there
        user_id_last_dates = db_logic.get_lastest_tweet_date()

        for user_info in users_info:
            user_db_id = user_info['id']
            screen_name = user_info['screen_name']
            if not from_date:
                from_date = get_user_last_tweet_date(user_db_id, user_id_last_dates)

            if request_counter >= requests_limit:
                request_counter = 0
                print 'reaching request limit {0} sleeping for {1} seconds'.format(requests_limit, sleeping_time)
                time.sleep(sleeping_time)


            request_counter += 1
            update_user_tweet( user_db_id, screen_name, from_date, db_logic)

    elif users and len(users) > 0:
        pass
    else:
        print 'no users to update.'

def get_user_last_tweet_date(user_id, user_id_last_dates):
    for item in user_id_last_dates:
        id = item["user_id"]
        last_date = item["latest_date"]
        if user_id == id:
            return last_date
    return None


def update_user_tweet( user_db_id, screen_name,from_date, db_logic):
    '''
    find the tweet_id closet to the from date and get tweets with since_id
    :param user_db_id:
    :param screen_name:
    :param from_date:
    :param db_logic:
    :return:
    '''
    print 'checking uset tweets for user : {0} from date {1}'.format(screen_name, from_date)
    output = db_logic.get_latest_tweet_id( user_id = user_db_id, from_date = from_date)[0]
    since_tweet_id = output["tweet_id"]
    user_tweets = twiter_obj.get_timeline_only(screen_name=screen_name, count=500, since_id=since_tweet_id)

    # insert to tweets table
    tweets_fields = ["text", "date", "url", "User_id", "tweet_id"]
    tweet_files_fields = ["file_type", "file_url", "Tweets_id"]
    mentions_fields = ["tagged_users_id", "Tweet_id"]
    users_id_screen_name = db_logic.get_userid_screen_name_db()
    screen_names = [x['screen_name'] for x in users_id_screen_name]

    if len(user_tweets) > 0:
        print 'update user tweets : {0} from date {1}'.format(screen_name, from_date)
    for tweet in user_tweets:
        try:
            # tweet table:
            urls = ''
            for tweet_url in tweet['urls']:
                urls += tweet_url + '; '

            tweet_values = [tweet["text"], tweet["time"], urls, user_db_id, tweet["tweet_id"]]
            db_obj.insert_to_table(table_name='tweets', fields=tweets_fields, values=tweet_values)
            db_tweet_id = db_logic.get_last_id_from_table('tweets')[0]['last_id']
            # tweet files table:
            tweet_files = tweet['tweet_files']
            for tweet_file in tweet_files:
                tweet_files_values = [tweet_file['file_type'], tweet_file['file_url'], db_tweet_id]
                db_obj.insert_to_table(table_name='tweet_files', fields=tweet_files_fields, values=tweet_files_values)
                # finish deal with tweet files

            ############mentions table:
            ids, mentions_users = return_mentions_hoc_users(tweet['mentions'], users_id_screen_name, screen_names)

            # search mentions in tweet text and add them to ids list
            text = tweet['text']
            for screen_name in screen_names:
                if str(screen_name) in text:
                    ids.append(get_id_by_screenname(screen_name, users_id_screen_name))

            for user_id in ids:
                mention_values = [user_id, db_tweet_id]
                db_obj.insert_to_table(table_name='mentions', fields=mentions_fields, values=mention_values)

        except:
            print 'Error in loading tweets for user {0}'.format(screen_name)
            print traceback.format_exc()



if __name__ == '__main__':

    update_Tweets(all = True)