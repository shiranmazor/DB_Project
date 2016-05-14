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
from ServerLogic.common import *
import traceback

def insert_new_data():
    print 'connecting to db'
    db_obj = DbWrapper()
    twiter_obj = Twitter_Api()
    return db_obj,twiter_obj


def load_users_table(db_obj, twiter_obj):
    '''

    :param db_obj:
    :param twiter_obg:
    :return:
    '''
    sleeping_time = 60*20 #16minutes
    requests_limit = 120 # the limit is 180 requests
    request_counter = 0
    for screen_name in users_data:
        try:
            if request_counter == requests_limit:
                print 'reach requests limit sleeping for {0} seconds starting from {1}'.format(sleeping_time, datetime.datetime.now())
                time.sleep(sleeping_time)
                request_counter =0

            user_output = twiter_obj.get_user_data(screen_name = screen_name)
            request_counter+=1
            if len(user_output)>0:
                fields = ['full_name', 'screen_name', 'description', 'location', 'followers_count', 'friends_count',
                          'twitter_id','profile_picture_url','role_id','party_id']

                #getting rol_id and party_id value
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
            print 'problem with loading and inserting user {0}'.format(screen_name)
            print traceback.format_exc()
    print 'done with Users table!'

def load_Followers(db_obj,twiter_obj ):
    '''
    scan all the users id in db from users table, for each user id:
    1. get followers list from twitter
    2. get friends list \ followee id
    3. save all in different records in followers table
    :param db_obj:
    :param twiter_obj:
    :return:
    '''
    try:
        sleeping_time_followers = 60 * 20  # 16 minutes
        requests_limit_followers = 15  # the limit is 180 requests
        request_counter_followers = 0

        # get all user_id from db
        outputs = db_obj.get_userid_screen_name_db()
        ids_lst = [x['id'] for x in outputs]
        for output_id in outputs:
            try:
                user_id = output_id['id']
                screen_name = output_id['screen_name']
                print 'start inserting followers+ followees for user :{0}'.format(screen_name)
                # get followers id
                if request_counter_followers >= requests_limit_followers:
                    print 'reaching request limit on followers ans friends sleeping for {0} seconds'.format(
                        sleeping_time_followers)
                    request_counter_followers = 0
                    time.sleep(sleeping_time_followers)

                request_counter_followers += 1
                followers_ids = twiter_obj.get_user_followers(screen_name=screen_name)

                request_counter_followers += 1
                followees_ids = twiter_obj.get_user_followees(screen_name=screen_name)

                # insert data to db
                # first as user_id as followee_id - insert all followers of this user to DB
                followee_id = user_id
                for follower_id in followers_ids:
                    # check if follower is in our users:
                    user_data = db_obj.get_user_data_by_twitter_id(twitter_id=follower_id)
                    if len(user_data) == 0:
                        continue
                    else:
                        follower_user_id = user_data[0]['id']

                        fields = ['follower_id', 'followee_id']
                        values = [follower_user_id, followee_id]
                        try:
                            db_obj.insert_to_table(table_name='followers', fields=fields, values=values)
                        except:
                            #in case the tuple was already exist!
                            print traceback.format_exc()

                #insert all followee data about the user:
                follower_id = user_id
                for followee_id in followees_ids:
                    # check if followee is in our users:
                    user_data = db_obj.get_user_data_by_twitter_id(twitter_id=followee_id)
                    if len(user_data) == 0:
                        continue
                    else:
                        followee_user_id = user_data[0]['id']
                        fields = ['follower_id', 'followee_id']
                        values = [follower_id, followee_user_id]
                        try:
                            db_obj.insert_to_table(table_name='followers', fields=fields, values=values)
                        except:
                            # in case the tuple was already exist!
                            print traceback.format_exc()

            except:
                print 'problen getting followers+followees of user {0}'.format(output_id)
                print traceback.format_exc()
    except:
        print traceback.format_exc()
    print 'done with followers table!'

def get_party_role_id(db_obj,screen_name):
    role_name = users_data[screen_name]['role']
    party_letter = users_data[screen_name]['party']
    party_name = 'Democratic' if party_letter == 'D' else 'Republican'
    party_out = db_obj.get_values_by_field(table_name = 'Party', field_name = 'party_name', field_value = party_name)
    role_out = db_obj.get_values_by_field(table_name='Role', field_name='rol_name', field_value=role_name)
    return party_out[0]['party_id'],role_out[0]['role_id']

def load_party_data(db_obj):
    '''
    loading party static record from user_data dict
    the parites are - Democratic -1, Republican -2
    :return:
    '''
    fields = ['party_name']
    values = ['Democratic','Republican']
    try:
        for value in values:
            db_obj.insert_to_table(table_name='Party', fields=fields, values=[value])
    except Exception as Ex:
        print 'problem with writing party name to db'
        print traceback.format_exc()

def load_Role_data(db_obj):
    '''
    loading party static record from user_data dict
    the parites are - Democratic -1, Republican -2
    :return:
    '''
    fields = ['rol_name']
    roles = get_values_by_key('role')
    try:
        for value in roles:
            db_obj.insert_to_table(table_name='Role', fields=fields, values=[value])
    except Exception as Ex:
        print 'problem with writing party name to db'
        print traceback.format_exc()


def load_tweets_all_users(db_obj , twiter_obj):
    '''
    this function geting all user ids fro db and load all tweets for all users
    also update tables - tweet_files, mentions
    :param db_obj:
    :param twiter_obj:
    :return:
    '''
    sleeping_time = 60*20 #16minutes
    requests_limit = 150 # the limit is 180 requests
    request_counter = 0

    if request_counter >= requests_limit:
        request_counter = 0
        print 'reaching request limit {0} sleeping for {1} seconds'.format(requests_limit,sleeping_time)
        time.sleep(sleeping_time)

    #get all users id and screen_name from db
    users_info = db_obj.get_userid_screen_name_db()
    request_counter+=1
    for user_info in users_info:
        user_db_id = user_info['id']
        screen_name = user_info['screen_name']
        load_tweets_user(db_obj, twiter_obj, user_db_id, screen_name)

def load_tweets_user(db_obj , twiter_obj, user_db_id, screen_name):
    '''
    getting the last 500 tweets of the user by screen name and insert them to db
    fill in - Mentions table, tweets and tweet files
    :param db_obj:
    :param twiter_obj:
    :param user_db_id:
    :param screen_name:
    :return:
    '''
    try:
        print 'loading tweets for user {0}'.format(screen_name)
        user_tweets = twiter_obj.get_timeline_only(screen_name= screen_name, count=500)
        #insert to tweets table
        tweets_fields = ["text","date","url","User_id","tweet_id"]
        tweet_files_fields = ["file_type","file_url","Tweets_id"]
        mentions_fields = ["tagged_users_id","Tweet_id"]
        users_id_screen_name = db_obj.get_userid_screen_name_db()
        screen_names = [x['screen_name'] for x in users_id_screen_name]

        for tweet in user_tweets:
            try:
                # tweet table:
                urls = ''
                for tweet_url in tweet['urls']:
                    urls+=tweet_url+'; '

                tweet_values = [tweet["text"],tweet["time"],urls, user_db_id,tweet["tweet_id"]]
                db_obj.insert_to_table(table_name='tweets', fields=tweets_fields, values=tweet_values)
                db_tweet_id = db_obj.get_last_id_from_table('tweets')['id']
                #tweet files table:
                tweet_files = tweet['tweet_files']
                for tweet_file in tweet_files:

                    tweet_files_values = [tweet_file['file_type'], tweet_file['file_url'],db_tweet_id]
                    db_obj.insert_to_table(table_name='tweet_files', fields=tweet_files_fields, values=tweet_files_values)

                #finish deal with tweet files
                ############mentions table:
                ids,mentions_users = return_mentions_hoc_users(db_obj, tweet['mentions'], users_id_screen_name, screen_names)

                #search mentions in tweet text and add them to ids list
                text = tweet['text']
                for screen_name in screen_names:
                    if screen_name in text:
                        ids.append(get_id_by_screenname(screen_name, users_id_screen_name))

                for user_id in ids:
                    mention_values = [user_id, db_tweet_id]
                    db_obj.insert_to_table(table_name='mentions', fields=mentions_fields, values=mention_values)
            except:
                print 'error in loading tweet continue to the next one'
                print traceback.format_exc()
    except:
        print 'Error in loading tweets for user {0}'.format(screen_name)
        print traceback.format_exc()


def get_id_by_screenname(screen_name,users_id_screen_name):
    for item in users_id_screen_name:
        if item['screen_name'] == screen_name:
            return item['id']

def return_mentions_hoc_users(db_obj, mentions, users_id_screen_name, screen_names):
    '''
    get the mentions list and remove all the users that are not in db
    :param db_obj:
    :param mentions:
    :return: two lists: user_ids, screen_names
    '''
    users_screen_names = []
    ids = []

    for name in mentions:
        if name  in screen_names:
            users_screen_names.append(name)
    ids = [x['id'] for x in users_id_screen_name if x['screen_name'] in users_screen_names]
    return ids , users_screen_names

def update_data():
    pass

def run():
    db_obj = DbWrapper()
    twiter_obj = Twitter_Api()
    #load_party_data(db_obj)
    #load_Role_data(db_obj)
    #load_users_table(db_obj, twiter_obj)
    load_Followers(db_obj, twiter_obj)

def fill_db_from_screch():
    db_obj = DbWrapper()
    twiter_obj = Twitter_Api()
    print 'loading party table'
    load_party_data(db_obj)
    print 'loading role table'
    load_Role_data(db_obj)
    print 'loading users table'
    load_users_table(db_obj, twiter_obj)
    print 'loading followers'
    load_Followers(db_obj, twiter_obj)
    print 'loading tweets table with tweet files and mentions on all users'
    load_tweets_all_users(db_obj, twiter_obj)
    print 'finish loading table!'


if __name__ == '__main__':
    fill_db_from_screch()
