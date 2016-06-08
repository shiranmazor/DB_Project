import sys
import os
sys.path.append("../")
sys.path.append("flask_egg")
sys.path.append("flask")
sys.path.append("itsdangerous.egg-info")
from flask import Flask, render_template, request, url_for, send_from_directory
from interface_server_db import *
import traceback
import time


application = Flask(__name__)

@application.route("/")
def hello():
    tuples = create_tuples("full_name", "party_name")
    data = ""
    if tuples[1] == 0:
        data = {"title": "Hello Mates", "users_tuples": create_tuples("full_name", "party_name")[0],
                "select_names": ["screen_name_1", "screen_name_2"], "popular_searches": get_popular_searches()[0]}
    return render_template('index.html', **data)

@application.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@application.route("/bottom", methods = ['GET', 'POST'])
def bottom():
    screen_name_1 = str(request.form['screen_name_1'])
    screen_name_2 = str(request.form['screen_name_2'])
    if screen_name_1 == screen_name_2 == 'disabled':
        return ""
    friendship = get_friendship(screen_name_1, screen_name_2)
    if friendship[1] == 0:
        return friendship[0]
    else:
        return "ERROR!" + friendship[0]

@application.route("/person", methods = ['GET', 'POST'])
def person():
    if str(request.form['location']) == "left":
        screen_name = str(request.form['screen_name_1'])
        return get_user_data(screen_name)
    elif str(request.form['location']) == "right":
        screen_name = str(request.form['screen_name_2'])
        return get_user_data(screen_name)


@application.route("/update_all_users")
def update_all_users():
    update_file = os.path.join("static", "system", "update_status.txt")
    if os.path.isfile(update_file):
        create_time = str(time.ctime(os.path.getmtime(update_file)))
        return "<script>alert('Cannot start a DB update. Update is already in progress! Update started in: {}')</script>".format(create_time)
    else:
        #update_all_users_backround()  # commented out - update takes hours
        return ""



@application.route("/top_searches")
def top_searches():
    return get_popular_searches(3)[0] + "<br /><a href='update_all_users' target='dummy'>Click here to update all users</a>"



@application.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":
    if len(sys.argv) == 2:
        host = sys.argv[1]
        application.run(host=host,port=consts.TOMCAT_PORT)
    else:
        application.run(port=consts.TOMCAT_PORT)

