import ServerLogic.user_data as ud
from ServerLogic.friendship_data import *
from ServerLogic.searches_logic import *
from time import gmtime, strftime
import traceback

def create_tuples(*fields):
    try:
        users_data = ud.get_user_list()
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
        users_data = ud.get_user_list()
        shared_info = get_shared_info(screen_name_1, screen_name_2)
        html = ""
        html_pattern = "<br />{0} and {1} are both ".format(users_data[screen_name_1]["full_name"], users_data[screen_name_2]["full_name"])
        html_pattern_followers = "<br />{0} and {1} ".format(users_data[screen_name_1]["full_name"],
                                                             users_data[screen_name_2]["full_name"])
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
                    count = len(followers)
                    f = ""
                    for follow in followers:
                        f += str(follow) + ", "
                    f = f[:-2]
                    if f != "":
                        f += "."
                        if count > 1:
                            html += (html_pattern_followers + "have the common followers: " + f)
                        else:
                            html += (html_pattern_followers + "have the common follower: " + f)

                if key == "followees":
                    followees = shared_info["followees"]
                    followees = followees[0:100]
                    f = ""
                    for follow in followees:
                        f += str(follow) + ", "
                    f = f[:-2]
                    if f != "":
                        f += "."
                        html += (html_pattern_followers + "and follow: " + f)
        except:
            print traceback.format_exc()
    return html

def get_shared_tweets(screen_name_1, screen_name_2):
    shared = get_shared_tweets(screen_name_1, screen_name_2)
    shared_tweets = shared[0]
    shared_tweets = shared_tweets[0:20]
    tweets = ""
    count = 1
    for tweet in shared_tweets:
        tweets +="<br /> " + str(count) + ". " + str(tweet)
        count += 1
    return "<br /> The shared Tweets are: " + tweets

def get_tweets_user_mentions(screen_name_1, screen_name_2):
    users_data = ud.get_user_list()
    shared = get_shared_tweets(screen_name_1, screen_name_2)

    user1_mentions = shared[1]
    user1_mentions = user1_mentions[0:10]
    mention1 = ""
    count = 1
    for mention in user1_mentions:
        mention1 += "<br /> " + str(count) + ". " + str(mention)
        count += 1

    user2_mentions = shared[2]
    user2_mentions = user2_mentions[0:10]

    mention2 = ""
    count = 1
    for mention in user2_mentions:
        mention2 += "<br /> " + str(count) + ". " + str(mention)
        count += 1

    return "<br /> {0} was mentioned in: {1}. {2} was mentioned in: {3}".format(users_data[screen_name_2]["full_name"], mention1, users_data[screen_name_1]["full_name"], mention2)

def get_user_data(screen_name):
    users_data = ud.get_user_list()
    html = "<br /> <img src={}>".format(users_data[screen_name]["profile_picture_url"])
    html += "<br />{} ".format(users_data[screen_name]["full_name"])
    html += "<br />is a {} ".format(users_data[screen_name]["role_name"])
    html += "<br />from {} ".format(users_data[screen_name]["location"])
    html += ""
    return html

def get_popular_searched(count = 5):
    searched_list = str(get_popular_users(count).strip('[]'))
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return "<br /> The most popular congress members searched, till {0} are: {1}".format(date, searched_list)

def update_search(screen_name):
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    update_user_search(screen_name, date)
    return