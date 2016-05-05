import sys
sys.path.append("../")

from DB.db_wrapper import *

db_global_object  = DbWrapper()

def get_user_data(user_name):
    db_global_object.get_values_by_field(table_name='Users')