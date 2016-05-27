import sys
sys.path.append("../")
from user_data import *
from common import *



def get_shared_info(screen_name1, screen_name2):
    '''
    extrating all user data from db and comparing the all fields
    :param full_name1:
    :param full_name2:
    :return:dict with keys of the shared values: party_name,rol_name, location,followers,followees
    '''
    shared_output = {}
    try:

        user1_output = get_user_data(screen_name=screen_name1)
        user2_output = get_user_data(screen_name=screen_name2)
        #comparing role_name, party_name
        if user1_output['party_name'] == user2_output['party_name']:
            shared_output['party_name'] =user1_output['party_name']

        if user1_output['rol_name'] == user2_output['rol_name']:
            shared_output['rol_name'] = user1_output['rol_name']
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