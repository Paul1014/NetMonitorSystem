from flask import Flask
from flask import render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_login import  UserMixin, LoginManager, login_required, current_user, login_user, logout_user
from net_tool import Connect_SSH, cisco_snmp, linux_snmp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Netmonitor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'Skills39'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager = LoginManager(app)



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
    DeviceTypes = db.Column(db.String(80), nullable=False)
    login_username = db.Column(db.String(80))
    login_password = db.Column(db.String(80))
    
    
    def __init__(self, name, IP, DeviceTypes, login_username, login_password):
        self.name = name
        self.IP = IP
        self.DeviceTypes = DeviceTypes
        self.login_username = login_username
        self.login_password = login_password
        
    def __repr__(self):
        return '<Devices %r>'% self.name

class UserAuth(UserMixin):
    pass

@login_manager.user_loader
def load_user(userid):
    user = UserAuth()
    user.id = userid
    return user

@app.route('/')
def index():
    return redirect(url_for('login'))   


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_active:
        return redirect(url_for('dashboard'))
    else:
        if request.method == 'GET':
            return render_template('login.html',failinfo=" ")
        else:
            username = request.form['username']
            password = request.form['password']
            try:
                DB_user = User.query.filter_by(username=username).first()
                if password == DB_user.password :
                    user = UserAuth()
                    user.id = username
                    login_user(user)
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('login.html', failinfo="Password is not correct! Try again.")
            except:
                return render_template('login.html', failinfo="Cannot found this Username, plz check.")
            


@app.route('/logout')  
def logout():
    logout_user()  
    return redirect(url_for('login'))



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_active:
        devices = Devices.query.all()
        return render_template('dashboard.html',devices=devices)
    else:
        return redirect(url_for('login')) 


@app.route('/device_add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add_form.html',status=" ")
    else:
        name = request.form['DeviceName']
        IP = request.form['IP']
        username = request.form['username']
        password = request.form['password']       
        device_type = request.form['devicestype']
        testssh = request.form['testconnect']

        if testssh == "yes":
            if Connect_SSH(IP,username,password):
                pass
            else:
                 return render_template('add_form.html',status="The SSH session cannot established")

        if IP == "" or name == "":
            return render_template('add_form.html',status="Some filed is not filled, plz check!")
        else:
            db.create_all()
            try:
                New_Device = Devices(name, IP, device_type, username, password)
                db.session.add(New_Device)
                db.session.commit()
            except:
                return render_template('add_form.html',status="Devices is existed")

            return render_template('add_form.html',status="Add success")
        
@app.route('/device/<id>')
def devices_status(id):
    device = Devices.query.filter_by(device_id=id).first()
    print(device.DeviceTypes)
    if device.DeviceTypes == "Cisco":
        snmpinfo = cisco_snmp(device.IP,"paulsnmp")
    else:
        snmpinfo = linux_snmp(device.IP,"public")

    return render_template('device_cisco.html', snmp_info=snmpinfo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
