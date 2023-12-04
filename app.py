from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route('/about/')
def about():
    return render_template("about.html")


@app.route('/science/')
def science():
    return render_template("science.html")


@app.route('/entertainment/')
def entertainment():
    return render_template("entertainment.html")


@app.route('/neanderthal/')
def neanderthal():
    return render_template("neanderthal.html")


if __name__ == '__main__':
    app.run()
