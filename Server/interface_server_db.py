import ServerLogic.user_data as ud
from ServerLogic.friendship_data import *
import traceback

users_data = ud.get_user_list()

def create_tuples(*fields):
    try:
        result = []
        for user in users_data.keys():
            temp = [users_data[user]["screen_name"]]
            for field in fields:
                temp.append(users_data[user][field])
            result.append(temp)
        return sorted(result, key=lambda item: item[1])
    except:
        print traceback.format_exc()

def compare_fields(field, screen_name_1, screen_name_2):
    return users_data[screen_name_1][field] == users_data[screen_name_2][field]

def get_friendship(screen_name_1, screen_name_2):
    html = ""
    if screen_name_1 == screen_name_2:
        html = "<br />You chose to compare the same person! Please choose different persons"
    else:
        shared_info = get_shared_info(screen_name_1, screen_name_2)
        html = ""
        html_pattern = "<br />{0} and {1} are both ".format(users_data[screen_name_1]["full_name"], users_data[screen_name_2]["full_name"])
        try:
            for key in shared_info.keys():
                if key == "party_name":
                    html += (
                    html_pattern + str_replace(users_data[screen_name_1]["party_name"], "Republican", "Republicans",
                                         "Democratic", "Democrats"))
                if key == "role_name":
                    html += (html_pattern + shared_info["role_name"] + "s")
                if key == "location":
                    html += (html_pattern + "from " + shared_info["location"])
                if key == "followers":
                    followers = str(shared_info["followers"]).strip('[]')
                    if followers != "":
                        html += (html_pattern + "have the common followers: " + followers)
                if key == "followees":
                    followees = str(shared_info["followees"]).strip('[]')
                    if followees != "":
                        html += (html_pattern + "and follow: " + followers)
        except:
            print traceback.format_exc()
    return html
def get_shared(screen_name_1):
    pass