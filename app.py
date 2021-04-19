from flask import Flask, render_template
from data import Articles


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
    articles = Articles()
    #print(articles[0]['title'])
    return render_template("articles.html", articles = articles)

@app.route('/article/<int:id>') #<id> 를 params 라고 해서 메소드에서 써먹을 수 있다.
def article(id):
    articles = Articles()
    article = articles[id - 1]
    return render_template("article.html", article = article)
    

@app.route('/Question')
def Qeustion():
    return render_template("Question.html")


if __name__ == '__main__':
    app.run()