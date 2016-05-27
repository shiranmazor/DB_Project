import sys
sys.path.append("../")
from common import *


def update_user_search(screen_name, search_date):
    try:
        #check if the user exist in DB
        user_id = db_logic.get_user_id_by_field(field_name='screen_name', field_value=screen_name)

    except:
        pass


def insert_new_user_search():
    pass



def update_existing_user():
    pass

def get_popular_searches():
    pass



