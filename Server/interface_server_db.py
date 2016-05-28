import ServerLogic.user_data as ud
from ServerLogic.friendship_data import *
from ServerLogic.searches_logic import *
from time import gmtime, strftime
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

def get_friendship(screen_name_1, screen_name_2):
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
                    followers = shared_info["followers"]
                    followers = followers[0:100]
                    followers = str(followers).strip('[]')
                if followers != "":
                        html += (html_pattern + "have the common followers: " + followers)
                if key == "followees":
                    followees = shared_info["followees"]
                    followees = followees[0:100]
                    followees = str(followees).strip('[]')
                    if followees != "":
                        html += (html_pattern + "and follow: " + followers)
        except:
            print traceback.format_exc()
    return html

def get_shared_tweets(screen_name_1, screen_name_2):
    shared = get_shared_tweets(screen_name_1, screen_name_2)
    shared_tweets = shared[0]
    shared_tweets = shared_tweets[0:20]
    return "<br /> The shared Tweets are: ".format(str(shared_tweets).strip('[]'))

def get_tweets_user_mentions(screen_name_1, screen_name_2):
    shared = get_shared_tweets(screen_name_1, screen_name_2)

    user1_mentions = shared[1]
    user1_mentions = user1_mentions[0:10]
    user1_mentions = str(user1_mentions).strip('[]')

    user2_mentions = shared[2]
    user2_mentions = user2_mentions[0:10]
    user2_mentions = str(user2_mentions).strip('[]')

    return "<br /> {0} was mentioned in: {1}. {2} was mentioned in: {3}".format(users_data[screen_name_2]["full_name"], user1_mentions, users_data[screen_name_1]["full_name"], user2_mentions)


def get_user_data(screen_name):
    html = "<br /> <img src={}>".format(users_data[screen_name]["profile_picture_url"])
    html += "<br />{} ".format(users_data[screen_name]["full_name"])
    html += "<br />is a {} ".format(users_data[screen_name]["role_name"])
    html += "<br />from {} ".format(users_data[screen_name]["location"])
    html += ""
    return html

def get_popular_searched():
    searched_list = str(get_popular_users(3).strip('[]'))
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return "<br /> The most popular congress members searched, till {0} are: {1}".format(date, searched_list)

def update_search(screen_name):
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    update_user_search(screen_name, date)
    return