from flask import Flask, render_template, request, url_for, send_from_directory
import sys
sys.path.append("../")
from interface_server_db import *
import traceback


application = Flask(__name__, static_url_path = "/templates/static", static_folder = "/static")

@application.route("/")
def hello():
    #print str(create_tuples("full_name", "party_name"))
    data = {"params": ["sharon", "yoyo", "fuck off!", "bla bla bla..."],
            "title": "Hello Mates", "users_tuples": create_tuples("full_name", "party_name"),
            "select_names": ["screen_name_1", "screen_name_2"]}
    return render_template('index.html', **data)

@application.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@application.route("/bottom", methods = ['GET', 'POST'])
def bottom():
    screen_name_1 = str(request.form['screen_name_1'])
    screen_name_2 = str(request.form['screen_name_2'])
    return get_friendship(screen_name_1, screen_name_2)

@application.route("/leftandright", methods = ['GET', 'POST'])
def bottom():
    screen_name = str(request.form['screen_name'])
    return get_user_data(screen_name)

@application.route("/test")
def test():
    return "<h1 style='color:blue'>YOYO!</h1>"


@application.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)

