import sys
sys.path.append("../")
from user_data import *
from common import *



def get_shared_info(screen_name1, screen_name2):
    '''
    extrating all user data from db and comparing the all fields
    :param full_name1:
    :param full_name2:
    :return:dict with keys of the shared values: party_name, rol_name, location, followers, followees
    '''
    shared_output = {}
    try:

        user1_output = get_user_data(screen_name=screen_name1)
        user2_output = get_user_data(screen_name=screen_name2)
        #comparing role_name, party_name
        if user1_output['party_name'] == user2_output['party_name']:
            shared_output['party_name'] =user1_output['party_name']

        if user1_output['role_name'] == user2_output['role_name']:
            shared_output['role_name'] = user1_output['role_name']
        #location
        if user1_output['location'] == user2_output['location']:
            shared_output['location'] = user1_output['location']

        #present shared members
        shared_followers = get_shared_followers_from_users(user1_output, user2_output)
        shared_output["followers"] = shared_followers

        shared_followews = get_shared_followees_from_users(user1_output, user2_output)
        shared_output["followees"] = shared_followews

    except:
        return shared_output
    return shared_output

def get_shared_followers_from_users(user1_output, user2_output):
    shared = []
    user1_followers = user1_output['followers_names']
    user2_followers = user2_output['followers_names']
    shared = [x for x in user1_followers if x in user2_followers]
    return shared

def get_shared_followees_from_users(user1_output, user2_output):
    shared = []
    user1_followees = user1_output['followees_names']
    user2_followees = user2_output['followees_names']
    shared = [x for x in user1_followees if x in user2_followees]
    return shared



def get_shared_followers(screen_name1, screen_name2):
    user1_output = get_user_data(screen_name=screen_name1)
    user2_output = get_user_data(screen_name=screen_name2)
    shared = get_shared_followers_from_users(user1_output,user2_output )
    return shared

def get_shared_followees(screen_name1, screen_name2):
    user1_output = get_user_data(screen_name=screen_name1)
    user2_output = get_user_data(screen_name=screen_name2)
    shared = get_shared_followers(user1_output, user2_output)
    return shared


def get_shared_tweets(screen_name1, screen_name2):
    '''
    returns all the shared tweet objects and tweet_files
    present tweets whe the mentions each other
    present tweets with the same users
    :param screen_name1:
    :param screen_name2:
    :return:tuple of : shared_users_tweets, user1_mention2_tweets,user2_mention1_tweets,
    each list contain tweet dict
    '''
    try:
        user1_mention2_tweets = []
        user2_mention1_tweets = []
        shared_users_tweets = []
        #get user id
        user_id1 = db_logic.get_user_id_by_field(field_name='screen_name', field_value=screen_name1)
        user_id2 = db_logic.get_user_id_by_field(field_name='screen_name', field_value=screen_name2)

        #get all tweets
        user1_tweets = db_logic.get_user_tweets(user_id=user_id1)
        user2_tweets = db_logic.get_user_tweets(user_id=user_id2)

        user1_data = []
        user2_data = []
        #for each get tweet_files and mentions
        #user1:
        for user1_tweet in user1_tweets:
            #get mentions for this tweet
            tweet_id = user1_tweet['id']
            #tagged_users_id
            tagged_users = db_logic.get_mentions_userid(tweet_id=tweet_id)
            tagged_ids = [x['tagged_users_id'] for x in tagged_users]
            if user_id2 in tagged_ids:
                user1_mention2_tweets.append(user1_tweet)

            #get tweet_files:
            tweet_files = db_logic.get_tweet_files(tweet_id = tweet_id)
            user1_tweet['tagged_users'] = tagged_ids
            user1_tweet['tweet_files'] = tweet_files
            user1_data.append(user1_tweet)

        for user2_tweet in user2_tweets:
            # get mentions for this tweet
            tweet_id = user2_tweet['id']
            # tagged_users_id
            tagged_users = db_logic.get_mentions_userid(tweet_id=tweet_id)
            tagged_ids = [x['tagged_users_id'] for x in tagged_users]
            if user_id1 in tagged_ids:
                user2_mention1_tweets.append(user2_tweet)

            # get tweet_files:
            tweet_files = db_logic.get_tweet_files(tweet_id=tweet_id)
            user2_tweet['tagged_users'] = tagged_ids
            user2_tweet['tweet_files'] = tweet_files
            user2_data.append(user2_tweet)

        #search tweets with the same users mentions
        for user_tweet in user1_data:

            tagged1 = user_tweet['tagged_users']
            tweets = return_tweets_with_tags(user2_data, tagged1)
            if len(tweets) > 0:
                #user_tweet contains poeple mentions in user2 tweets
                shared_users_tweets.extend(tweets)
                shared_users_tweets.append(user_tweet)

        return shared_users_tweets, user1_mention2_tweets,user2_mention1_tweets
    except:
        print traceback.format_exc()
        return [],[],[]


def return_tweets_with_tags(user_data, tagged_lst):
    result = []
    for tweet in user_data:
        tagged2 = tweet['tagged_users']
        for user_id in tagged_lst:
            if user_id in tagged2:
                result.append(tweet)

    return result