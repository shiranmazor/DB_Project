from flask import Flask, render_template, request, url_for, send_from_directory
import sys
sys.path.append("../")
from ServerLogic.common import *
from ServerLogic.user_data import *
from ServerLogic.friendship_data import *

application = Flask(__name__, static_url_path = "/templates/static", static_folder = "static")


@application.route("/")
def hello():

    def create_sorted_tuples(*fields):
        users_output = get_user_list()
        keys = [x['screen_name'] for x in users_output]
        result = []
        for user in keys:
            # print user
            # print str(users_data)
            temp = [users_data[user]["screen_name"]]
            for field in fields:
                temp.append(users_output[user][field])
            result.append(temp)
            # print str(temp)
        return sorted(result, key=lambda item: item[1])

    data = {"params": ["sharon", "yoyo", "fuck off!", "bla bla bla..."],
            "title": "Hello Mates", "users_tuples": create_sorted_tuples("real_name", "party"),
            "select_names": ["screen_name_1", "screen_name_2"]}
    return render_template('index.html', **data)

@application.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@application.route("/bottom", methods = ['GET', 'POST'])
def bottom():
    screen_name_1 = str(request.form['screen_name_1'])
    screen_name_2 = str(request.form['screen_name_2'])

    def compare_fields(field):
        return (users_data[screen_name_1][field] == users_data[screen_name_2][field])

    html_pattern = "<br />{0} and {1} are both ".format(users_data[screen_name_1]["real_name"], users_data[screen_name_2]["real_name"])
    html = ""

    if compare_fields("role"):
        html += (html_pattern + users_data[screen_name_1]["role"] + "s")
    if compare_fields("state"):
        html += (html_pattern + "from " + users_data[screen_name_1]["state"])
    if users_data[screen_name_1]["party"] in ("D", "R") and compare_fields("party"):
        html += (html_pattern + str_replace(users_data[screen_name_1]["party"],"R", "Republicans","D", "Democrats"))
    return html

@application.route("/test")
def test():
    return "<h1 style='color:blue'>YOYO!</h1>"


@application.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)

