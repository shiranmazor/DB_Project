import sys
sys.path.append("../")
from common import *
from TwitterApi.twitter_api import *



def get_user_data(full_name = None, screen_name = None, user_id= None):
    '''
    return user dict from users table
    :param full_name:
    :return: dict of: db_id,twitter_id, full_name,profile_picture_url location, followers_count,friends_count, description,
     followers_screen_names, followees_screen_names, role_name, party_name, role_id, party_id
    '''
    try:
        user_output = {}
        if full_name:
            user_output = db_global_object.get_values_by_field(table_name='users', field_name = 'full_name', field_value = full_name)[0]
        elif screen_name:
            user_output = db_global_object.get_values_by_field(table_name='users', field_name='screen_name', field_value=screen_name)[0]
        elif user_id:
            user_output = db_global_object.get_values_by_field(table_name='users', field_name='screen_name', field_value=screen_name)[0]

        #extract role_name and party name:
        pary_out = db_global_object.get_values_by_field(table_name='party', field_name = 'party_id', field_value = user_output['party_id'])[0]
        user_output['party_name'] = pary_out['party_name']

        # extract role_name and role name:
        role_out = db_global_object.get_values_by_field(table_name='role', field_name='role_id',
                                                        field_value=user_output['role_id'])[0]
        user_output['role_name'] = role_out['rol_name']

        #get followers and friends names:
        user_output['followers_names'] = get_followers_screen_names(user_id=user_output['id'])
        user_output['followees_names'] = get_followees_screen_names(user_id=user_output['id'])
        return user_output
    except:
        print 'problem in getting user data'
        print traceback.format_exc()
        return {}

def get_followers_screen_names(user_id = None, full_name = None, screen_name = None):
    try:
        followers_out = {}
        if user_id:
            followers_out = db_logic.get_followers_screen_name(user_id=user_id)
        elif full_name:
            user_id = db_logic.get_user_id_by_field(field_name='full_name', field_value=full_name)
            followers_out = db_logic.get_followers_screen_name(user_id=user_id)
        elif screen_name:
            user_id = db_logic.get_user_id_by_field(field_name='screen_name', field_value=screen_name)
            followers_out = db_logic.get_followers_screen_name(user_id=user_id)

        followers = [x['screen_name'] for x in followers_out]
        return followers
    except:
        print traceback.format_exc()
        return []

def get_followees_screen_names(user_id = None, full_name = None, screen_name = None):
    try:
        followees_out = []
        if user_id:
            followees_out = db_logic.get_followees_screen_name(user_id=user_id)
        elif full_name:
            user_id = db_logic.get_user_id_by_field(field_name='full_name',field_value=full_name )
            followees_out = db_logic.get_followees_screen_name(user_id=user_id)
        elif screen_name:
            user_id = db_logic.get_user_id_by_field(field_name='screen_name', field_value=screen_name)
            followees_out = db_logic.get_followees_screen_name(user_id=user_id)


        followees = [x['screen_name'] for x in followees_out]
        return followees
    except:
        print traceback.format_exc()
        return []

def get_user_list():
    '''
    return a list of dict with : id, screen_name, full_name, party_name
    :return:
    '''
    output = {}
    users_output = db_logic.get_users_list_with_party()
    for user in users_output:
        output[user['screen_name']] = user

    return output

def get_last_tweets(count = 0,from_date = None, user_id = None, full_name = None, screen_name = None):
    '''
    return last tweets
    :param user_id:
    :param count:
    :param from_date:
    :return:list of tweets contain: key1= tweet value=tweet record, key2 = tweet_files, key3 = mentions
    '''
    output_lst = []
    if not user_id and not full_name and not screen_name:
        print 'Error ! empty args'
        return None
    if full_name:
        user_id = db_logic.get_user_id_by_field(field_name='full_name',field_value= full_name)
    if screen_name:
        user_id = db_logic.get_user_id_by_field(field_name='screen_name', field_value=screen_name)

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
        tweet_dict = {}
        tweet_dict['tweet'] = tweet
        tweet_files = get_tweet_files(tweet['id'])
        tweet_mentions = get_tweet_mentions(tweet['id'])
        tweet_dict['tweet_files'] = tweet_files
        tweet_dict['mentions'] = tweet_mentions
        output_lst.append(tweet_dict)

    return output_lst

def get_tweet_files(tweet_id):
    files_out = db_global_object.get_values_by_field( table_name = 'tweet_files', field_name = 'tweet_id', field_value = tweet_id)
    return files_out

def get_tweet_mentions(tweet_id):
    mentions = db_global_object.get_values_by_field(table_name='mentions', field_name='tweet_id',
                                                     field_value=tweet_id)
    return mentions




if __name__ == '__main__':
    get_last_tweets(user_id=3, count=5)