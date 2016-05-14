import sys
sys.path.append("../")

from TwitterApi.twitter_api import *
from DB.db_wrapper import *

'''
twiter_obg  = Twitter_Api()
output_timeline = twiter_obg.get_user_data(screen_name = 'shiranmazor1')
db_obj = DbWrapper()
fields = ['full_name', 'screen_name','description','location','followers_count','friends_count','twitter_id']
valuse = [output_timeline['name'],output_timeline['screen_name'],output_timeline['description'],
          output_timeline['location'] ,output_timeline['followers_count'],output_timeline['friends_count'],output_timeline['id']]
db_obj.insert_to_table(table_name = 'Users',fields=fields, values=valuse)
'''

twiter_obg  = Twitter_Api()
output_timeline = twiter_obg.get_timeline_only(screen_name = 'shiranmazor1')
i=6


twiter_obg  = Twitter_Api()
