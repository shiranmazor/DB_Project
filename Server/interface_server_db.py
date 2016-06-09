import datetime
import threading
import time
from time import gmtime, strftime
import os

import ServerLogic.friendship_data as fd
import ServerLogic.searches_logic as sd
import ServerLogic.update_data_from_twiter as upd
import ServerLogic.user_data as ud
from ServerLogic.common import *

'''
Every function in this module return a tuple of 2:
return-tuple[0] is the data requested or the traceback text in case of an error
return-tuple[1] is the error code- 0 if success, and 1 if failure.
The server checks error code in the server, for every use of this functions
'''

def create_tuples(*fields):
    '''
    extrating user data from db with selected fields, sorted by the second parameter (which should be full_name)
    :param fields:
    :return:sorted list with the chosen fields, th key is screen_name, error code
    '''
    try:
        users_data = ud.get_user_list()
        result = []

        for user in users_data.keys():
            temp = [users_data[user]["screen_name"]]

            for field in fields:
                temp.append(users_data[user][field])
            result.append(temp)

        return sorted(result, key=lambda item: item[1]), 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1


def get_friendship(screen_name_1, screen_name_2):
    '''
    this function generates an html text that gives all the shared data of the two given screen names.
    including: party, role, location, followers and followees
    :param screen_name_1:
    :param screen_name_2:
    :return:html text as described up, error code
    '''
    try:
        if screen_name_1 == screen_name_2:
            return "<br />You chose to compare the same person! Please choose different persons", 0
        else:
            users_data = ud.get_user_list()
            shared_info = fd.get_shared_info(screen_name_1, screen_name_2)
            html_prev = "<center><br />Shared information between {0} and {1}:".format(users_data[screen_name_1]["full_name"],
                                                                 users_data[screen_name_2]["full_name"])
            html_party = ""
            html_role = ""
            html_followers = ""
            html_followees = ""
            html_location = ""
            html_tweets = "<br />Tweets mentioning each other:<br />" + get_related_tweets(screen_name_1, screen_name_2)
            html_tweets += "<br />Tweets mentioning same people:<br />" + get_tweets_shared(screen_name_1, screen_name_2)[0]
            for key in shared_info.keys():
                if key == "party_name":
                    html_party = "<br />Both are {0}.".format(shared_info["party_name"])
                    if shared_info["party_name"] in LOGOS:
                        html_party = "<img src='{0}' style='width:30px;height:auto' />".format(LOGOS[shared_info["party_name"]]) + html_party

                if key == "role_name":
                    html_role = "<br />They are {0}s.".format(shared_info["role_name"])

                if key == "location":
                    htmtl_location = "<br />They live in {0}.".format(shared_info["location"])

                if key == "follow_each_other":
                    if users_data[screen_name_1]["full_name"].split()[0] == users_data[screen_name_2]["full_name"].split()[0]:
                        name1 = users_data[screen_name_1]["full_name"]
                        name2 = users_data[screen_name_2]["full_name"]
                    else:
                        name1 = users_data[screen_name_1]["full_name"].split()[0]
                        name2 = users_data[screen_name_2]["full_name"].split()[0]
                    if shared_info["follow_each_other"] == [0, 0]:
                        html_follow_each_other = "<br />They don't follow each other."
                    if shared_info["follow_each_other"] == [1, 0]:
                        html_follow_each_other = "<br />{0} Follows {1} but not the other way around."\
                            .format(name1, name2)
                    if shared_info["follow_each_other"] == [0, 1]:
                        html_follow_each_other = "<br />{0} Follows {1} but not the other way around." \
                            .format(name2, name1)
                    if shared_info["follow_each_other"] == [1, 1]:
                        html_follow_each_other = "<br />They follow each other."

                if key == "followers":
                    followers = shared_info["followers"]
                    followers = followers[0:100]

                    count = len(followers)
                    num = 1
                    f = ''

                    for follow in followers:
                        try:
                            f += "<br />"+ str(users_data[follow]["full_name"])
                            num += 1
                        except:
                            pass
                    if count > 1:
                        html_followers = "<br />Shared followers:" + f
                    elif count == 1:
                        html_followers = "<br />Shared follower:" + "<br />{0}".format(str(users_data[followers[0]]["full_name"]))
                if key == "followees":
                    followees = shared_info["followees"]
                    followees = followees[0:100]
                    f = ""
                    count = len(followees)
                    num = 1
                    for followee in followees:
                        try:
                            f += "<br />"+ str(users_data[followee]["full_name"])
                            num += 1
                        except:
                            pass
                    if count > 1:
                        html_followees = "<br />Shared followees:" + f
                    elif count == 1:
                        html_followees = "<br />Shared followee:" + "<br />{0}".format(users_data[followees[0]]["full_name"])
        if html_role == "" and html_location == "" and html_party == ""\
            and html_followers == "" and html_followees == "" and html_tweets == "":
            return "<br /> There is no shared information between {0} and {1}!"\
                       .format(users_data[screen_name_1]["full_name"], users_data[screen_name_2]["full_name"]), 0
        else:
            return html_prev + html_location + html_party + html_role + html_follow_each_other + html_followers + html_followees + html_tweets + ("<br />")*10 + "</center>", 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

def update_all_users_backround():
    try:
        #mProcess = multiprocessing.Process(target=start_update_all_users())
        t = threading.Thread(name='child process', target=start_update_all_users)
        t.start()
        i=0
    except:
        print traceback.format_exc()
        return False

def start_update_all_users():
    file_folder = os.path.join(os.getcwd(), 'static','system')
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    file_path = os.path.join(file_folder, 'update_status.txt')
    update_file = open(file_path, 'w')
    try:
        #we will open a new file in order to save all our logs
        sleeping_time = 60 * 20  # 16minutes
        requests_limit = 150  # the limit is 180 requests
        request_counter = 0
        users_data = ud.get_user_list()
        for user_data in users_data:
            #each user is a request
            if request_counter >= requests_limit:
                request_counter = 0
                update_file.write('sleeping: reaching request limit {0} sleeping for {1} seconds\n'.format(requests_limit, sleeping_time))
                print 'sleeping: reaching request limit {0} sleeping for {1} seconds\n'.format(requests_limit, sleeping_time)
                update_file.flush()
                time.sleep(sleeping_time)

            sn = users_data[user_data]["screen_name"]
            # get last tweet date
            last_date = ud.db_logic.get_last_tweet_date(screen_name=sn)
            update_file.write('update: user {0}\n'.format(sn))
            update_file.flush()
            update_user(screen_name=sn, from_date=last_date)
            update_file.write('finish: user {0}\n'.format(sn))
            update_file.flush()

    except:
        print  traceback.format_exc()
        pass
    finally:
        update_file.write("finish: all users")
        update_file.close()
        finish_file_parh = os.path.join(file_folder,'finished_update_status.txt' )
        if os.path.exists(finish_file_parh):
            os.remove(finish_file_parh)
        os.rename(file_path,finish_file_parh)




def update_user(screen_name, from_date = None):
    '''
    update user info + tweets in db
    :param screen_name:
    :param from_date: date of the last tweet
    :return:
    '''
    #update user info
    upd.update_user_data(screen_name = screen_name)
    if not from_date:
        from_date = ud.db_logic.get_last_tweet_date(screen_name=screen_name)
    #update user tweetes
    user_id = ud.db_logic.get_user_id_by_field(field_name='screen_name', field_value=screen_name)
    #
    upd.update_user_tweet(user_db_id = user_id, screen_name = screen_name, from_date = from_date)


def get_related_tweets(screen_name_1, screen_name_2,number = 20):
    '''
    return user1 and user2 tweets that mentions each other in time line format
    screen_name, Date:tweet text
    Screen_name, Date :tweet text
    :param screen_name_1:
    :param screen_name_2:
    :param number:
    :return:
    '''
    data = ''
    try:
        sorted_lst = []
        shared = fd.get_shared_tweets(screen_name_1, screen_name_2)
        shared_users_tweets, user1_mention2_tweets, user2_mention1_tweets = shared
        user1_mention2_tweets = user1_mention2_tweets[:number]
        user2_mention1_tweets = user2_mention1_tweets[:number]
        user1_mention2_tweets.extend(user2_mention1_tweets)
        try:
            user1_mention2_tweets = sorted(user1_mention2_tweets,key= lambda x:x['date'])
        except:
            pass



        if len(user1_mention2_tweets) > 0:
            return "<div style='background: rgba(0, 0, 0, 0.1);'>" + format_tweet(user1_mention2_tweets, showUser=True) + "</div>"
        else:
            return "<br /> There are no tweets mentioning each other."
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

def get_tweets_shared(screen_name_1, screen_name_2,number = 20):
    '''
    this function generates an html text that gives the number (default=20)
    of shared tweets of the two given screen names.
    :param screen_name_1:
    :param screen_name_2:
    :param num:
    :return:html text as described up, error code
    '''
    data = ''
    try:
        shared = fd.get_shared_tweets(screen_name_1, screen_name_2)
        shared_tweets = shared[0]
        shared_users_tweets, user1_mention2_tweets, user2_mention1_tweets  = shared
        shared_tweets = shared_tweets[0:number]
        try:
            # sort list by date
            shared_tweets = sorted(shared_tweets, key=lambda x: x['date'])
        except:
            pass
        if len(shared_tweets) > 0:
            return "<div style='background: rgba(255, 255, 255, 0.1);'>" + format_tweet(shared_tweets, showUser=True) + "</div>", 0
        else:
            return "There are no tweets mentioning the same person.", 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1


def get_user_data(screen_name):
    '''
    this function generates an html text that gives personal data of the given screen name:
    profile picture, name, role, location and latest user's tweet.
    :param screen_name:
    :return:html text as described up, error code
    '''
    try:
        user_data = ud.get_user_data(screen_name=screen_name)
        #html = "<br /> <img src={}>".format(user_data["profile_picture_url"])
        html = '''
        <!DOCTYPE html>
        <html lang='en'>
        <head>
        <style>
        html, body {
        font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;
        font-size:large;
        }
        </style>
        </head>
        <body>
        <center>
'''
        html += "<br /><a href='https://twitter.com/{}' target='_blank'><img src='https://twitter.com/{}/profile_image?size=original' style='border-radius: 50%;width:150px;height:auto' /></a>".format(screen_name, screen_name)


        html += "<br />{}<br />".format(user_data["full_name"])
        if user_data["role_name"]:
            html += "<br />Is a {} ".format(user_data["role_name"])
        if user_data["location"]:
            html += "<br />From {} ".format(user_data["location"])

        html += "<br />Has {} friends".format(user_data["friends_count"])
        html += "<br />and {} followers".format(user_data["followers_count"])
        last_tweets = ud.get_last_tweets(count=1, screen_name=screen_name)
        #last_tweet = ud.get_last_tweets(count=1, screen_name=screen_name)[0]['tweet']['text']
        last_tweet = format_tweet(last_tweets, 1)
        html += "<br /> <br />Last tweet: {} "\
            .format(str(last_tweet))

        update_search(screen_name)

        return html + "</center></body></html>", 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

def remove_useless_chars(string):
    left = 0
    right = len(string) - 1
    while(string[left] != "_" and not(string[left].isalnum())):
        left += 1
    while(string[right] != "_" and not(string[right].isalnum())):
        right -= 1
    if left < right:
        return string[left:right + 1]
    else:
        return ""

def add_href_to_raw_text(string, target="_blank"):
    string = string.encode('utf-8')
    string_array = string.split(" ")
    for i in range(len(string_array)):
        if string_array[i].startswith("https://") or string_array[i].startswith("http://"):
            string_array[i] = "<a href='{0}' target='{1}'>{2}</a>".format(string_array[i], target, string_array[i])
        elif string_array[i].startswith("#"):
            string_array[i] = "<a href='https://twitter.com/hashtag/{0}' target='{1}'><b>{2}</b></a>".format(remove_useless_chars(string_array[i]), target, string_array[i])
        elif string_array[i].startswith("@"):
            string_array[i] = "<a href='https://twitter.com/{0}' target='{1}'><b>{2}</b></a>".format(remove_useless_chars(string_array[i]), target, string_array[i])
    return " ".join(string_array)

def format_tweet(tweets_list, chop=sys.maxint, showUser=False):

    def string_mod360(string):
        string = str(string)
        sum = 0
        for c in string:
            sum += ord(c)
        return sum % 360

    text = ""
    for i in range(min(len(tweets_list), chop)):
        tweet = tweets_list[i]
        if type(tweet) == dict and "tweet" in tweet:
            tweet = tweet["tweet"]
        color_code = '#ffffff' if not showUser else 'hsla({}, 82%, 82%, 0.5)'.format(string_mod360(tweet["screen_name"]))
        poster = (" {} ({})".format(users_data[tweet["screen_name"]]["real_name"], tweet["screen_name"]) if showUser else "")
        text += "<br /><br /><a href='https://twitter.com/anyuser/status/{0}' target='_blank'>".format(tweet["tweet_id"]) +\
               str(tweet["date"]) + poster +\
               "</a>""<br /><div style='background-color:{};font-size:14px;font-family: Times New Roman;border-radius:5px'><i>".format(color_code) +\
               add_href_to_raw_text(tweet['text']) + "</i></div><br />"
    return text

def get_popular_searches(count = 5):
    '''
    this function generates an html text that shows the most popular searches in our application (default=5),
    and date of update.
    :param count:
    :return:html text as described up, error code
    '''
    try:
        searched_list = sd.get_popular_users(count)
        text = ""
        GOLD, SILVER, BRONZE = '#ffe400', '#c3c7ca', '#c56f50'
        for i in range(len(searched_list)):
            dic = searched_list[i]
            if i in [0,1,2]:
                text += "<font color='{}' title='Last searched on {}'>{} ({})</font> ".format(str_replace(i,"0",GOLD,"1",SILVER,"2",BRONZE), str(dic["last_date"]), dic["full_name"], dic["count"])
            else:
                text += "{0} ({1})".format(dic["full_name"], dic["count"])
        most_followed = sd.get_twitter_popular_users()
        text2 = ""
        if len(most_followed) > 0:
            text2 = "<br /><div style='color: white; text-align: center; font-weight: bold; text-shadow: 1px 1px 2px black, 0 0 25px blue, 0 0 5px darkblue; font-size:large'>Most followed searched:"
            for person in most_followed:
                text2 += "<br /><span title='Last searched on {}'>{} (Followers: {}, Counter: {})</span>".format(person["last_search"], person["name"], person["followers_count"], person["num_of_searches"])
            text2 += "</div>"

        return "<div style='color: white; text-align: center; font-weight: bold; text-shadow: 1px 1px 2px black, 0 0 25px blue, 0 0 5px darkblue; font-size:large'>Most popular searched:<br/ >{}{}<small>Last updated: {}</small></div>".format(text, text2, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

def update_search(screen_name):
    '''
    this function updates a search of a give screen_name in the db, including the date of selection.
    :param screen_name:
    :return:error message in case of error, error code
    '''
    try:
        sd.update_user_search(screen_name,datetime.datetime.now())
        return "", 0
    except:
        print traceback.format_exc()
        return traceback.format_exc(), 1

'''
helper functions
'''
def get_date():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())