from flask import Flask, render_template


app = Flask(__name__)

app.debug = True

@app.route('/data', methods = ['GET'])
def index():
    # return "Hello World !"
    return render_template("index.html", data = "Bang")

@app.route('/about')
def about():
    return render_template("about.html", hello = "H J Bang")

 



if __name__ == '__main__':
    app.run()