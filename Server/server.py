from flask import Flask, render_template, request, url_for, send_from_directory
import sys
sys.path.append("../")
import ServerLogic.user_data as ud
from ServerLogic.friendship_data import *
import traceback

application = Flask(__name__, static_url_path = "/templates/static", static_folder = "static")
users_data = ud.get_user_list()

@application.route("/")
def hello():

    def create_tuples(*fields):
        try:
            keys = [x['screen_name'] for x in users_data]
            result = []
            for user in users_data:
                # print user
                # print str(users_data)
                temp = [user["screen_name"]]
                for field in fields:
                    temp.append(user[field])
                result.append(temp)
                # print str(temp)
            return sorted(result, key=lambda item: item[1])
        except:
            print traceback.format_exc()

    print str(create_tuples("full_name", "party_name"))
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

    def compare_fields(field):
        return (users_data[screen_name_1][field] == users_data[screen_name_2][field])

    html = ""
    if compare_fields("full_name"):
        html = "<br />You chose to compare the same person!"
        return html
    else:
        html_pattern = "<br />{0} and {1} are both ".format(users_data[screen_name_1]["full_name"],
                                                            users_data[screen_name_2]["full_name"])

    if compare_fields("role"):
        html += (html_pattern + users_data[screen_name_1]["role"] + "s")
    if compare_fields("state"):
        html += (html_pattern + "from " + users_data[screen_name_1]["state"])
    if users_data[screen_name_1]["party_name"] in ("D", "R") and compare_fields("party_name"):
        html += (html_pattern + str_replace(users_data[screen_name_1]["party_name"],"R", "Republicans","D", "Democrats"))
    return html

@application.route("/test")
def test():
    return "<h1 style='color:blue'>YOYO!</h1>"


@application.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)

