import sys
sys.path.append("../")
from common import *
import user_data

def update_user_search(screen_name, search_date):
    '''

    :param screen_name:
    :param search_date: type = datetime
    :return:
    '''
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
    try:
        print 'insert new serach for user id :{0} at date {1}'.format(user_id, search_date)
        search_fields = ['user_id','last_date','count']
        search_values = [user_id, search_date, 1]
        db_global_object.insert_to_table(table_name='searches', fields=search_fields, values=search_values)
    except:
        print traceback.format_exc()




def update_existing_user(user_id, search_date, search_record):
    #get search count
    count = search_record['count']+1
    fields = ['last_date','count']
    values=[search_date, count]
    condition_str= 'user_id = {0}'.format(user_id)
    db_global_object.update_table(table_name='searches', fields = fields, values = values, condition_str =condition_str)

def get_popular_users(count = 5):
    '''
    return last 'count' searches
    :param count:
    :return:
    '''
    try:
        output = []
        popular_searches = db_logic.get_popular_searches(count=count)
        #for each user get user_data
        for search in popular_searches:
            user_id = search['user_id']
            count = search['count']
            #get user_id data
            data = db_global_object.get_values_by_field(table_name='Users', field_name='id', field_value=user_id)[0]
            d={}
            d['screen_name'] = str(data['screen_name'])
            #print "MATTAN " + str(user_data.get_user_data(screen_name=data['screen_name']).keys())
            d['full_name'] = str(user_data.get_user_data(screen_name=data['screen_name'])['full_name'])
            d['count'] = count
            d['last_date'] = search['last_date']
            output.append(d)

        return output
    except:
        print traceback.format_exc()








