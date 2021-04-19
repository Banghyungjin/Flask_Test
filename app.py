from flask import Flask, render_template


app = Flask(__name__)

app.debug = True

@app.route('/', methods = ['GET'])
def index():
    # return "Hello World !"
    return render_template("index.html", data = "Bang")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/articles')
def articles():
    return render_template("articles.html")

@app.route('/Question')
def Qeustion():
    return render_template("Question.html")


if __name__ == '__main__':
    app.run()