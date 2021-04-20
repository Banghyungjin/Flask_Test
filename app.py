from flask import Flask, render_template, request, redirect
from data import Articles
import pymysql

app = Flask(__name__)

app.debug = True

db = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '1234',
    db = 'busan'
)



@app.route('/', methods = ['GET'])
def index():
    # return "Hello World !"
    return render_template("index.html", data = "Bang")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/articles')
def articles():
    db = pymysql.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = '1234',
        db = 'busan'
    )
    cursor = db.cursor()
    sql = 'SELECT * FROM topic'
    cursor.execute(sql)
    topics = cursor.fetchall()
    #articles = Articles()
    #print(articles[0]['title'])
    return render_template("articles.html", articles = topics)

@app.route('/article/<int:id>') #<id> 를 params 라고 해서 메소드에서 써먹을 수 있다.
def article(id):
    cursor = db.cursor()
    #articles = Articles()
    #article = articles[id - 1]
    sql = 'SELECT * FROM topic WHERE id = {};'.format(id)
    cursor.execute(sql)
    topic = cursor.fetchone()
    return render_template("article.html", article = topic)

@app.route('/add_articles', methods = ["GET", "POST"])
def add_articles():
    cursor = db.cursor()
    if request.method == "POST":
        desc = request.form['Desc']
        title = request.form['Title']
        author = request.form['Author']
        sql_insert = "INSERT INTO `busan`.`topic` (`title`, `body`, `author`) VALUES (%s, %s, %s);" 
        val = [title, desc, author]
        cursor.execute(sql_insert, val)
        db.commit()
        topic = cursor.fetchall()
        #db.close()
        return redirect("/articles")
    else:
        return render_template("add_articles.html")

@app.route('/delete/<int:id>', methods = ["POST"])
def delete(id):
    cursor = db.cursor()
    sql_insert = "DELETE FROM topic WHERE id = {};".format(id) 
    
    cursor.execute(sql_insert)
    db.commit()
    topic = cursor.fetchall()
    #db.close()
    return redirect("/articles")

@app.route('/Question')
def Qeustion():
    return render_template("Question.html")

if __name__ == '__main__':
    app.run()