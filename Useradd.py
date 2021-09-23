from app import db
from app import User
import getpass 
def add_user(username,password):
    db.create_all()
    try:
        user = User(username=username, password=password)
    except:
        print("Add User has error")
    db.session.add(user)
    db.session.commit()

user = input("Enter your Username:")
passwd = getpass.getpass("Enter your password:")

add_user(user,passwd)
