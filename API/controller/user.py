import random
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash , check_password_hash

from API.common.database import db

class User(db.Model):
    __tablename__ = "userdata"
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True , nullable=False)
    name= db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30) , unique=True , nullable=False)
    password = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(256) , nullable=False)

def getUniqueUsername(name):
    # remove spaces or _ or - or . from the name
    name = name.replace(" " , "").replace("_","").replace("-","").replace("." , "")
    # append a random 4-digit number to make it unique
    new_name = name + str(random.randint(1000, 9999))
    # check if new username already exists in User class
    user = User.query.filter_by(username=new_name).first()
    # if new username already exists, keep generating new usernames until a unique one is found
    while user:
        new_name = name + str(random.randint(1000, 9999))
        user = User.query.filter_by(username=new_name).first()
    return new_name

def signup(username , email , name , password):
    hashed_password = generate_password_hash(password)
    # append data to the table
    exp = datetime.utcnow() + timedelta(days=7)
    token = jwt.encode({'username': username, 'exp': exp}, 'SECRET_KEY', algorithm='HS256')
    new_user = User(username=username, email=email, name=name, password=hashed_password , token=token)
    try:
        db.session.add(new_user)
        db.session.commit()
        data = {
            "userid": new_user.userid,
            "username": username,
            "token": token
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }        
    return data

def signin(username , password):
    # Query the database for the user with the provided username
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and if the provided password matches the stored password hash
    if user and check_password_hash(user.password, password):
        # Login successful
        # Generate a token with an expiration date
        exp = datetime.utcnow() + timedelta(days=7)
        token = jwt.encode({'username': username, 'exp': exp}, 'SECRET_KEY', algorithm='HS256')
        # update token in database
        user.token = token
        db.session.commit()
        data = {
            "userid": user.userid,
            "username": username,
            "token": token
        }
    else:
        # Login failed
        data = {
            "error":True,
            "message":" Wrong Username Or Password "
        }
    return data

def signout(username , token):
    # Query the database for the user with the provided username
    user = User.query.filter_by(username=username).first()
    if user:
        # update token in database
        user.token = ""
        db.session.commit()
        data = {
            "message":"Logged Out Successfully"
        }
    else:
        data = {
            "error":True,
            "message":"Wrong Username Or Token"
        }
    return data

def fetchUser(username , token):
    user = User.query.filter_by(username=username).first()
    if user and user.token == token:
        data = {
            "error":False,
            "userid": user.userid,
            "username": user.username,
            "name": user.name,
            "email": user.email
        }
    else:
        data = {
            "error":True,
            "message":"Wrong Username Or Token"
        }
    return data

def updateUser(username , token , name , email):
    user = User.query.filter_by(username=username).first()
    if user and user.token == token:
        user.name = name
        user.email = email
        db.session.commit()
        data = {
            "userid": user.userid,
            "username": user.username,
            "name": user.name,
            "email": user.email
        }
    else:
        data = {
            "error":True,
            "message":"Wrong Username Or Token"
        }
    return data

def deleteUser(username , token):
    user = User.query.filter_by(username=username).first()
    if user and user.token == token:
        db.session.delete(user)
        db.session.commit()
        # TODO : also delete all the bookings
        data = {
            "message":"User Deleted Successfully"
        }
    else:
        data = {
            "error":True,
            "message":"Wrong Username Or Token"
        }
    return data

def changePassword(username , token , old_password , new_password):
    user = User.query.filter_by(username=username).first()
    if user and user.token == token and check_password_hash(user.password, old_password):
        user.password = generate_password_hash(new_password)
        db.session.commit()
        data = {
            "message":"Password Changed Successfully"
        }
    else:
        data = {
            "error":True,
            "message":"Wrong Credential"
        }
    return data

def getPublicInfo(id):
    user = User.query.filter_by(userid=id).first()
    if user:
        data = {
            "userid": user.userid,
            "username": user.username,
            "name": user.name,
            "email": user.email
        }
    else:
        data = {
            "error":True,
            "message":"User Not Found"
        }
    return data