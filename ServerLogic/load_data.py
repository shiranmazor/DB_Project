'''
this module will contain functions for filling and updaing the db from twiter
uses twitter_api module
1. insert_all_data
2. update_existing_data(from_date)
3. insert_user_table
4. insert_new_tweets(user_id)
'''
import sys

from TwitterApi.twitter_api import *
from DB.db_wrapper import *
