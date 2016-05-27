import sys
sys.path.append("../")
from user_data import *
from common import *



def get_shared_info(full_name1, full_name2):
    '''
    extrating all user data from db and comparing the all fields
    :param full_name1:
    :param full_name2:
    :return:
    '''
    user1_output = get_user_data(full_name=full_name1)
    user2_output = get_user_data(full_name=full_name2)
    #comparing role_name, party_name,

def get_shared_followers(full_name1, full_name2):
    pass