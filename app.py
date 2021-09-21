from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("main.html")


if __name__ == '__main__':
    app.run()
    app.add_url_rule("/favicon.ico",
                     redirect_to=url_for("static", filename="icons/favicon.ico"))
