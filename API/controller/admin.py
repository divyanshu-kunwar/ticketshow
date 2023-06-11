import random
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash , check_password_hash

from API.common.database import db

class Admin(db.Model):
    __tablename__ = "admindata"
    adminid = db.Column(db.Integer, primary_key=True)
    adminname = db.Column(db.String(30), unique=True , nullable=False)
    name= db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30) , unique=True , nullable=False)
    password = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(256) , nullable=False)

def getUniqueAdminname(name):
    # remove spaces or _ or - or . from the name
    name = name.replace(" " , "").replace("_","").replace("-","").replace("." , "")
    # append a random 4-digit number to make it unique
    new_name = name + str(random.randint(1000, 9999))
    # check if new adminname already exists in Admin class
    admin = Admin.query.filter_by(adminname=new_name).first()
    # if new adminname already exists, keep generating new adminnames until a unique one is found
    while admin:
        new_name = name + str(random.randint(1000, 9999))
        admin = Admin.query.filter_by(adminname=new_name).first()
    return new_name

def signup(adminname , email , name , password):
    hashed_password = generate_password_hash(password)
    # append data to the table
    exp = datetime.utcnow() + timedelta(days=7)
    token = jwt.encode({'adminname': adminname, 'exp': exp}, 'SECRET_KEY', algorithm='HS256')
    new_admin = Admin(adminname=adminname, email=email, name=name, password=hashed_password , token=token)
    try:
        db.session.add(new_admin)
        db.session.commit()
        data = {
            "adminid": new_admin.adminid,
            "adminname": adminname,
            "token": token
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }        
    return data

def signin(adminname , password):
    # Query the database for the admin with the provided adminname
    admin = Admin.query.filter_by(adminname=adminname).first()

    # Check if the admin exists and if the provided password matches the stored password hash
    if admin and check_password_hash(admin.password, password):
        # Login successful
        # Generate a token with an expiration date
        exp = datetime.utcnow() + timedelta(days=7)
        token = jwt.encode({'adminname': adminname, 'exp': exp}, 'SECRET_KEY', algorithm='HS256')
        # update token in database
        admin.token = token
        db.session.commit()
        data = {
            "adminid": admin.adminid,
            "adminname": adminname,
            "token": token
        }
    else:
        # Login failed
        data = {
            "error":True,
            "message":" Wrong Adminname Or Password "
        }
    return data

def signout(adminname , token):
    # Query the database for the admin with the provided adminname
    admin = Admin.query.filter_by(adminname=adminname).first()
    if admin:
        # update token in database
        admin.token = ""
        db.session.commit()
        data = {
            "message":"Logged Out Successfully"
        }
    else:
        data = {
            "error":True,
            "message":"Wrong Adminname Or Token"
        }
    return data

def fetchAdmin(adminname , token):
    admin = Admin.query.filter_by(adminname=adminname).first()
    if admin and admin.token == token:
        data = {
            "error":False,
            "adminid": admin.adminid,
            "adminname": admin.adminname,
            "name": admin.name,
            "email": admin.email
        }
    else:
        data = {
            "error":True,
            "message":"Wrong Adminname Or Token"
        }
    return data

def updateAdmin(adminname , token , name , email):
    admin = Admin.query.filter_by(adminname=adminname).first()
    if admin and admin.token == token:
        admin.name = name
        admin.email = email
        db.session.commit()
        data = {
            "adminid": admin.adminid,
            "adminname": admin.adminname,
            "name": admin.name,
            "email": admin.email
        }
    else:
        data = {
            "error":True,
            "message":"Wrong Adminname Or Token"
        }
    return data

def deleteAdmin(adminname , token):
    admin = Admin.query.filter_by(adminname=adminname).first()
    if admin and admin.token == token:
        db.session.delete(admin)
        db.session.commit()
        # TODO : also delete all the bookings
        data = {
            "message":"Admin Deleted Successfully"
        }
    else:
        data = {
            "error":True,
            "message":"Wrong Adminname Or Token"
        }
    return data

def changePassword(adminname , token , old_password , new_password):
    admin = Admin.query.filter_by(adminname=adminname).first()
    if admin and admin.token == token and check_password_hash(admin.password, old_password):
        admin.password = generate_password_hash(new_password)
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