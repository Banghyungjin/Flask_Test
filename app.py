from flask import Flask, render_template, request, redirect, flash, session
from data import Articles
from passlib.hash import sha256_crypt
import pymysql

app = Flask(__name__)

app.secret_key = 'my_secret_key'

app.debug = True
# db 로그인
db = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = '1234',
    db = 'busan'
)

#메인 화면& 로그인
@app.route('/', methods = ['GET', 'POST'])
def index():
    # return "Hello World !"
    if session.get('is_logged') is not None:
        return render_template("index.html", user = session.get('is_logged'))
    elif request.method == "POST":
        db = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            password = '1234',
            db = 'busan'
        )
        cursor = db.cursor()
        sql = 'SELECT password FROM users where username = %s;'
        usid = request.form['Username']
        ps = request.form['psword']
        cursor.execute(sql, usid)
        user = cursor.fetchone()
        if user == None:
            flash("없는 아이디입니다.")
        elif sha256_crypt.verify(ps, user[0]):
            session['is_logged'] = usid
            return render_template("index.html", user = session.get('is_logged'))
        else:
            flash("틀린 비밀번호입니다.")
        return render_template("log_in.html")
    else:
        return render_template("log_in.html")
# 정보화면 - 아직 만드는 중
@app.route('/about')
def about():
    if session.get('is_logged') is not None:
        return render_template("about.html")
    else:
        return render_template("log_in.html")

# 로그아웃 기능
@app.route('/log_out')
def log_out():
    session.clear()
    return render_template("log_in.html")
# db에서 목록 읽어오는 기능
@app.route('/articles', methods = ["GET", "POST"])
def articles():
    if session.get('is_logged') is not None:
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
    else:
        return render_template("log_in.html")
# articles에서 선택한 걸 자세히 표시하는 기능
@app.route('/article/<int:id>') #<id> 를 params 라고 해서 메소드에서 써먹을 수 있다.
def article(id):
    cursor = db.cursor()
    #articles = Articles()
    #article = articles[id - 1]
    sql = 'SELECT * FROM topic WHERE id = {};'.format(id)
    cursor.execute(sql)
    topic = cursor.fetchone()
    return render_template("article.html", article = topic)
# 새로운 article을 추가하는 기능
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
# article을 제거하는 기능
@app.route('/delete/<int:id>', methods = ["POST"])
def delete(id):
    cursor = db.cursor()
    sql_insert = "DELETE FROM topic WHERE id = {};".format(id) 
    cursor.execute(sql_insert)
    db.commit()
    topic = cursor.fetchall()
    #db.close()
    return redirect("/articles")
# article을 수정하는 기능
@app.route('/change_articles/<int:id>', methods = ["GET", "POST"])
def change_articles(id):
    cursor = db.cursor()
    if request.method == "POST":
        desc = request.form['Desc']
        title = request.form['Title']
        author = request.form['Author']
        sql_change = "UPDATE topic SET title = %s, body = %s, author = %s, create_date = NOW() WHERE (id = %s);" 
        val = [title, desc, author, id]
        cursor.execute(sql_change, val)
        db.commit()
        topic = cursor.fetchall()
        return redirect("/articles")
    else:
        cursor = db.cursor()
    sql = 'SELECT * FROM topic WHERE id = {};'.format(id)
    cursor.execute(sql)
    topic = cursor.fetchone()
    return render_template("change_articles.html", article = topic)
# 회원가입 기능
@app.route('/register', methods = ["GET", "POST"])
def register():
    cursor = db.cursor()
    if request.method == "POST":
        name = request.form['Name']
        email = request.form['Email']
        username = request.form['Username']
        psword = sha256_crypt.encrypt(request.form['psword'])
        sql_insert = "INSERT INTO `busan`.`users` (`name`, `email`, `username` , `password`) VALUES (%s, %s, %s, %s);" 
        val = [name, email, username, psword]
        cursor.execute(sql_insert, val)
        db.commit()
        topic = cursor.fetchall()
        #db.close()
        return redirect("/")
    else:
        return render_template("register.html")

# @app.route('/Question')
# def Qeustion():
#     return render_template("Question.html")

if __name__ == '__main__':
    app.run()