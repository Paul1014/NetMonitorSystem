from flask import Flask
from flask import render_template,redirect,url_for,request

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))   


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['user_id']
    password = request.form['password']
    if username == "paul" and password == "Skills39!":
        return "login"
    else:
        return render_template('login_failed.html')


app.run(host='0.0.0.0', debug=True)