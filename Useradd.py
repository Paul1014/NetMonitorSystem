from app import db
from app import User

def add_admin():
    db.create_all()
    user = User(username="admin", password="admin")
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    print("Create admin account")
    add_admin()