'''
this module will contain functions for filling and updaing the db from twiter
uses twitter_api module
1. insert_all_data
2. update_existing_data(from_date)
3. insert_user_table
4. insert_new_tweets(user_id)
'''
import sys
import time
from TwitterApi.twitter_api import *
from DB.db_wrapper import *

def insert_new_data():
    print 'connecting to db'
    db_obj = DbWrapper()
    twiter_obj = Twitter_Api()


def load_users_table(db_obj, twiter_obj):
    '''

    :param db_obj:
    :param twiter_obg:
    :return:
    '''
    sleeping_time = 60*16 #16minutes
    requests_limit = 150 # the limit is 180 requests
    request_counter = 0
    for screen_name in twiter_obj.screen_to_name:
        try:
            if request_counter == requests_limit:
                print 'reach requests limit sleeping for {0} seconds'.format(sleeping_time)
                time.sleep(sleeping_time)
            user_output = twiter_obj.get_user_data(screen_name = screen_name)
            request_counter+=1
            if len(user_output)>0:
                fields = ['full_name', 'screen_name', 'description', 'location', 'followers_count', 'friends_count',
                          'twitter_id','profile_picture_url']
                values = [user_output['full_name'], user_output['screen_name'], user_output['description'],
                          user_output['location'], user_output['followers_count'], user_output['friends_count'],
                          user_output['twitter_id'], user_output['profile_picutre_url']]
                db_obj.insert_to_table(table_name='Users', fields=fields, values=values)
            else:
                print 'problem getting user data on {0}'..format(screen_name)
        except:
            print 'problem with loading and inserting user {0}'.format(screen_name)

def update_data():
    pass

def run():
    db_obj = DbWrapper()
    twiter_obj = Twitter_Api()
    load_users_table(db_obj, twiter_obj)

if __name__ == '__main__':

    run()
