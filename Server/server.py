from flask import Flask, render_template, request, url_for

application = Flask(__name__)


@application.route("/")
def hello():
    data = {"params": ["sharon", "yoyo", "fuck off!", "bla bla bla..."],
            "title": "Hello Mates"}
    return render_template('index.html', **data)


@application.route("/test")
def test():
    return "<h1 style='color:blue'>YOYO!</h1>"


@application.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000)

