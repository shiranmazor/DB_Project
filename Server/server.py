from flask import Flask, render_template, request, url_for
import sys
sys.path.append("../")
from ServerLogic.common import *

application = Flask(__name__)


@application.route("/")
def hello():
    data = {"params": ["sharon", "yoyo", "fuck off!", "bla bla bla..."],
            "title": "Hello Mates", "users_tuples": users_data_sorted}
    return render_template('index.html', **data)

@application.route("/bottom", methods = ['GET', 'POST'])
def bottom():
    screen_name_1 = str(request.form['screen_name_1'])
    screen_name_2 = str(request.form['screen_name_2'])
    html_pattern = "<br />{0} and {1} are both ".format(users_data[screen_name_1]["real_name"], users_data[screen_name_2]["real_name"])
    html = ""
    if users_data[screen_name_1]["role"] == users_data[screen_name_2]["role"]:
        html += (html_pattern + users_data[screen_name_1]["role"] + "s")
    if users_data[screen_name_1]["state"] == users_data[screen_name_2]["state"]:
        html += (html_pattern + "from " + users_data[screen_name_1]["state"])
    if len(users_data[screen_name_1]["party"]) == 1 and users_data[screen_name_1]["party"] == users_data[screen_name_2]["party"]:
        html += (html_pattern + users_data[screen_name_1]["party"].replace("R", "Republicans").replace("D", "Democrats"))
    return html

@application.route("/test")
def test():
    return "<h1 style='color:blue'>YOYO!</h1>"


@application.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)

