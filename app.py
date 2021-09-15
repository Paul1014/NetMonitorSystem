from flask import Flask
from flask import render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Netmonitor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "User"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>'% self.username


class Devices(db.Model):
    __tablename__ = "Devices"
    device_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    IP = db.Column(db.String(80), nullable=False)
    login_username = db.Column(db.String(80))
    login_password = db.Column(db.String(80))
    
    def __init__(self, name, IP, login_username, login_password):
        self.name = name
        self.IP = IP
        self.login_username = login_username
        self.login_password = login_password

    def __repr__(self):
        return '<Devices %r>'% self.name

@app.route('/')
def index():
    return redirect(url_for('login'))   


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',failinfo=" ")
    username = request.form['username']
    password = request.form['password']
    DB_user = User.query.filter_by(username="admin").first()

    if username == DB_user.username and password == DB_user.password :
        return redirect(url_for('login'))
    else:
        return render_template('login.html', failinfo="Login failed! Try again.")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
