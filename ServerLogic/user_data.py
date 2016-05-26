import sys
sys.path.append("../")

from DB.db_wrapper import *
from DB.db_logic import *
from common import *

db_global_object  = DbWrapper()
db_logic = DBLogic(db_wrapper_obj = db_global_object)

def get_user_data(full_name):
    '''
    return user dict from users table
    :param full_name:
    :return: dict of: db_id,twitter_id, full_name,profile_picture_url location, followers_count,friends_count, description,
     followers_names (full_names), followees_names, role_name, party_name, role_id, party_id
    '''
    user_output = db_global_object.get_values_by_field(table_name='Users', field_name = 'full_name', field_value = full_name)[0]
    #extract role_name and party name:
    pary_out = db_global_object.get_values_by_field(table_name='party', field_name = 'party_id', field_value = user_output['party_id'])[0]
    user_output['party_name'] = pary_out['party_name']

    # extract role_name and role name:
    role_out = db_global_object.get_values_by_field(table_name='role', field_name='role_id',
                                                    field_value=user_output['role_id'])[0]
    user_output['role_name'] = role_out['rol_name']

    #get followers and friends names:
    followers_out = db_logic.get_followers_name(user_id = user_output['id'])
    followees_out = db_logic.get_followees_name(user_id=user_output['id'])
    followers = [x['full_name'] for x in followers_out]
    followees = [x['full_name'] for x in followees_out]
    user_output['followers_names'] = followers
    user_output['followees_names'] = followees

    return user_output


def get_user_list():
    '''
    return a list of dict with : id, screen_name, full_name
    :return:
    '''
    return_fileds = ['id','screen_name','full_name']
    users_output = db_global_object.get_multiple_values_by_field(return_fileds,  table_name = 'users')
    return users_output

def get_last_tweets(count = 0,from_date = None, user_id = None, full_name = None):
    '''
    return lasr
    :param user_id:
    :param count:
    :param from_date:
    :return:list of tweets contain: key1= tweet value=weet record, key2 = tweet_files, key3 = mentions
    '''
    output_lst = []
    if not user_id and not full_name:
        print 'Error ! empty args'
        return None
    if full_name:
        user_id = db_logic.get_user_id_by_name(full_name=full_name)

    #first get all tweets from db
    query = 'select * from tweets where user_id = %s '
    values = (user_id,)
    if count > 0 and from_date:
        query+= ' and date > %s order by date desc LIMIT %s'
        values = (user_id,from_date, count)
    elif from_date:
        values = (user_id,from_date, )
        query+='and date > %s'
        query += 'order by date desc'
    elif count > 0:
        values = (user_id, count,)
        query += ' order by date desc LIMIT %s'
    else:
        query+=' order by date desc'


    cursor = db_global_object.con.cursor()
    cursor.execute(query, values)
    columns = cursor.description
    user_tweets = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
    cursor.close()

    for tweet in user_tweets:
        tweet_dict ={}
        tweet_dict['tweet'] = tweet
        tweet_files = get_tweet_files(tweet['id'])
        tweet_mentions = get_tweet_mentions(tweet['id'])
        tweet_dict['tweet_files'] = tweet_files
        tweet_dict['mentions'] = tweet_mentions
        output_lst.append(tweet_dict)

    return  output_lst

def get_tweet_files(tweet_id):
    files_out = db_global_object.get_values_by_field( table_name = 'tweet_files', field_name = 'tweets_id', field_value = tweet_id)
    return files_out

def get_tweet_mentions(tweet_id):
    mentions = db_global_object.get_values_by_field(table_name='mentions', field_name='tweet_id',
                                                     field_value=tweet_id)
    return mentions

def update_user_data(full_name):
    pass


if __name__ == '__main__':
    get_last_tweets(user_id=3, count=5)