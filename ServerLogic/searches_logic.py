import sys
sys.path.append("../")
from common import *


def update_user_search(screen_name, search_date):
    try:
        #check if the user exist in DB
        user_id = db_logic.get_user_id_by_field(field_name='screen_name', field_value=screen_name)
        searches_lst = db_logic.get_searches_by_id(user_id = user_id)
        if len(searches_lst) > 0:
            update_existing_user(user_id, search_date, searches_lst[0])
        else:
            insert_new_user_search(user_id, search_date)
    except:
        pass


def insert_new_user_search(user_id, search_date):
    pass



def update_existing_user(user_id, search_date):
    pass

def get_popular_searches():
    pass



