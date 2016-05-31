import sys
import os
sys.path.append("../")
from flask import Flask, render_template, request, url_for, send_from_directory
from interface_server_db import *
import traceback


application = Flask(__name__)

'''
# remove old static map
url_map = application.url_map
try:
    for rule in url_map.iter_rules('static'):
        url_map._rules.remove(rule)
except ValueError:
    # no static view was created yet
    pass

# register new; the same view function is used
application.add_url_rule(
    application.static_url_path + '/<path:filename>',
    endpoint='static', view_func=application.send_static_file)
'''
@application.route("/")
def hello():
    #print str(create_tuples("full_name", "party_name"))
    tuples = create_tuples("full_name", "party_name")
    data = ""
    if tuples[1] == 0:
        data = {"params": ["sharon", "yoyo", "fuck off!", "bla bla bla..."],
                "title": "Hello Mates", "users_tuples": create_tuples("full_name", "party_name")[0],
                "select_names": ["screen_name_1", "screen_name_2"], "popular_searches": get_popular_searches()[0]}
    return render_template('index.html', **data)

@application.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@application.route("/bottom", methods = ['GET', 'POST'])
def bottom():
    screen_name_1 = str(request.form['screen_name_1'])
    screen_name_2 = str(request.form['screen_name_2'])
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



@application.route("/top_searches")
def top_searches():
    return get_popular_searches(3)[0]




'''
@application.route("/leftandright", methods = ['GET', 'POST'])
def bottom():
    screen_name = str(request.form['screen_name'])
    return get_user_data(screen_name)
'''

@application.route("/test")
def test():
    return "<h1 style='color:blue'>YOYO!</h1>"


@application.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)

