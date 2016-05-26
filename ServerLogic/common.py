import csv
from consts import *
import sys
sys.path.append("../")

name_to_screen = {}
screen_to_name = {}
users_data = {} #keys are "screen_name" values - list of all csv fields



def load_users_from_csv():
    try:
        with open(CSV_PATH, 'rb') as csvfile:
            csv_data = csv.DictReader(csvfile)
            for row in csv_data:
                real_name = row["real_name"]
                screen_name = row["screen_name"]
                if real_name != "" and screen_name != "":
                    name_to_screen[real_name] = screen_name
                    screen_to_name[screen_name] = real_name
    except Exception as ex:
        print 'Error in parsing CSV file! dictionaries will be Empty!'
        print ex.message

def load_users_dict():
    try:
        with open(CSV_PATH, 'rb') as csvfile:
            csv_data = csv.DictReader(csvfile)
            for row in csv_data:
                users_data[row["screen_name"]] = row
    except Exception as ex:
        print 'Error in parsing CSV file! dictionaries will be Empty!'
        print ex.message

def create_sorted_tuples(*fields):
    result = []
    for user in users_data.keys():
        #print user
        #print str(users_data)
        temp = [users_data[user]["screen_name"]]
        for field in fields:
            temp.append(users_data[user][field])
        result.append(temp)
        #print str(temp)
    return sorted(result, key=lambda item: item[0])

def get_values_by_key(key_name):
    '''
    getting list of values from user_data by specific key
    :param key_name:
    :return: list
    '''
    values = []
    for item in users_data:
        if users_data[item][key_name] not in values:
            values.append(users_data[item][key_name])

    return values

def str_replace(text, *params):
    assert len(params) % 2 == 0
    for i in range(0, len(params), 2):
        text = text.replace(params[i], params[i + 1])
    return text

def remove_hexa_bytes(data):
    return data.decode('unicode_escape').encode('ascii', 'ignore')


def return_mentions_hoc_users( mentions, users_id_screen_name, screen_names):
    '''
    get the mentions list and remove all the users that are not in db
    :param mentions:
    :return: two lists: user_ids, screen_names
    '''
    users_screen_names = []
    ids = []

    for name in mentions:
        if name  in screen_names:
            users_screen_names.append(name)
    ids = [x['id'] for x in users_id_screen_name if x['screen_name'] in users_screen_names]
    return ids , users_screen_names

def get_id_by_screenname(screen_name,users_id_screen_name):
    for item in users_id_screen_name:
        if item['screen_name'] == screen_name:
            return item['id']

def get_party_role_id(db_obj,screen_name):
    '''
    recive screen_name and returns the party_id,role_id
    from db
    :param db_obj:
    :param screen_name:
    :return:
    '''
    role_name = users_data[screen_name]['role']
    party_letter = users_data[screen_name]['party']
    party_name = 'Democratic' if party_letter == 'D' else 'Republican'
    party_out = db_obj.get_values_by_field(table_name = 'Party', field_name = 'party_name', field_value = party_name)
    role_out = db_obj.get_values_by_field(table_name='Role', field_name='rol_name', field_value=role_name)
    return party_out[0]['party_id'],role_out[0]['role_id']

load_users_from_csv()
load_users_dict()
#for i in range(len(users_data_sorted)):
#    users_data_sorted[i] = (users_data_sorted[i][0], users_data_sorted[i][1], users_data[users_data_sorted[i][1]]["party"])
