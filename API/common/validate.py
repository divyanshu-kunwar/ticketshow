from datetime import datetime, timedelta
import time
import jwt
import re

class Validate():    
    
    data = {
        "error" : False,
        "message" : []
    }

    #------------ USER/ADMIN -------------------#

    def validate_name(self , name):
        # name should not be less than 3 characters
        # name should not be more than 20 characters
        # name should not contain any special characters 
        # other than space and _ (underscore) , - (hyphen) , . (dot)
        if len(name) < 3:
            self.data["error"] = True
            self.data["message"].append("Name should not be less than 3 characters")
        if len(name) > 20:
            self.data["error"] = True
            self.data["message"].append("Name should not be more than 20 characters")
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        # match regex
        if regex.search(name) != None:
            self.data["error"] = True
            self.data["message"].append("Name should not contain any special characters")
            
    def validate_email(self , email):
        #regex for email
        regex = re.compile('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,4}$')
        # match regex
        if regex.match(email) == None:
            self.data["error"] = True
            self.data["message"].append("Invalid email")
            
    def validate_username(self , username):
        # username should not be less than 3 characters
        # username should not be more than 20 characters
        # username should not contain any special characters

        if len(username) < 3:
            self.data["error"] = True
            self.data["message"].append("Username should not be less than 3 characters")
        if len(username) > 20:
            self.data["error"] = True
            self.data["message"].append("Username should not be more than 20 characters")
        if not username.isalnum():
            self.data["error"] = True
            self.data["message"].append("Username should not contain special characters")

    def validate_password(self , password):
        # password should not be less than 8 characters
        # password should not be more than 20 characters
        # password should contain at least one number
        # password should contain at least one letter
        # password should contain at least one special character

        if len(password) < 8:
            self.data["error"] = True
            self.data["message"].append("Password should not be less than 8 characters")
        if len(password) > 20:
            self.data["error"] = True
            self.data["message"].append("Password should not be more than 20 characters")

        if password.isalnum():
            self.data["error"] = True
            self.data["message"].append("Password should contain at least one special character")

        if password.isalpha():
            self.data["error"] = True
            self.data["message"].append("Password should contain at least one number and one special character")
        
        if password.isdigit():
            self.data["error"] = True
            self.data["message"].append("Password should contain at least one letter and one special character")
    
    def check_token(self , token):
        # check if the token is valid 
        # check if the token is expired
        # exp = datetime.utcnow() + timedelta(days=7)
        # token = jwt.encode({'username': username, 'exp': exp},
        #  'SECRET_KEY', algorithm='HS256')
        try:
            data = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
            exp = data['exp']
            if exp < time.time():
                self.data["error"] = False
                self.data["message"].append("Token expired already")
            else:
                self.data["error"] = False
                self.data["message"].append("Token valid")
        except:
            print("Invalid token")
            self.data["error"] = True
            self.data["message"].append("Invalid token")
        return data

    def validate_signup(self , name , email , password):
        self.data["message"] = []
        self.data["error"] = False
        self.validate_name(name)
        self.validate_email(email)
        self.validate_password(password)
        return self.data
    
    def validate_signin(self , username , password):
        self.data["message"] = []
        self.data["error"] = False
        self.validate_username(username)
        self.validate_password(password)
        return self.data
    
    def validate_token(self , username , token):
        self.data["message"] = []
        self.data["error"] = False
        self.validate_username(username)
        self.check_token(token)
        return self.data

    def validate_update(self , username , token , name , email):
        self.data["message"] = []
        self.data["error"] = False
        self.validate_username(username)
        self.check_token(token)
        self.validate_name(name)
        self.validate_email(email)
        return self.data
    
    def validate_change_password(self , username , token , old_password , new_password):
        self.data["message"] = []
        self.data["error"] = False
        self.validate_username(username)
        self.check_token(token)
        self.validate_password(old_password)
        self.validate_password(new_password)
        return self.data
    # ------------- Shows ----------------------#
    
    def validate_rating(self , rating):
        if rating < 10 or rating > 50:
            self.data["error"] = True
            self.data["message"].append("Rating should be between 1 and 10")
        return self.data
        
    def validate_show_name(self , show_name):
        # show_name should not be less than 3 characters
        # show_name should not be more than 40 characters
        if len(show_name) < 3:
            self.data["error"] = True
            self.data["message"].append("Show name should not be less than 3 characters")
        if len(show_name) > 40:
            self.data["error"] = True
            self.data["message"].append("Show name should not be more than 40 characters")

    def validate_url(self , url):
        # url should not be less than 3 characters
        # should be url format
        if len(url) < 3:
            self.data["error"] = True
            self.data["message"].append("Url should not be less than 3 characters")

    def validate_description(self , description):
        # description should not be less than 3 characters
        # description should not be more than 1000 characters
        if len(description) < 3:
            self.data["error"] = True
            self.data["message"].append("Show description should not be less than 3 characters")
        if len(description) > 1000:
            self.data["error"] = True
            self.data["message"].append("Show description should not be more than 1000 characters")
    
    def validate_show_tags(self , show_tags):
        # no of tags should not be more than 5
        # each tag should not be less than 2 characters
        # each tag should not be more than 20 characters
        if len(show_tags) > 5:
            self.data["error"] = True
            self.data["message"].append("No of tags should not be more than 5")
        for tag in show_tags:
            if len(tag) < 2:
                self.data["error"] = True
                self.data["message"].append("${tag} is less than 2 characters".format(tag=tag))
            if len(tag) > 20:
                self.data["error"] = True
                self.data["message"].append("${tag} is more than 20 characters".format(tag=tag))
            if(not tag.isalnum()):
                self.data["error"] = True
                self.data["message"].append("${tag} contain special characters".format(tag=tag))

    def validate_show(self , show_name , show_image_url , description , show_tags):
        self.data["message"] = []
        self.data["error"] = False
        self.validate_show_name(show_name)
        self.validate_url(show_image_url)
        self.validate_description(description)
        self.validate_show_tags(show_tags)
        return self.data
    
    def validate_coordinates(self , coordinates):
        # coordinates must be a list of two numbers
        if len(coordinates) != 2:
            self.data["error"] = True
            self.data["message"].append("Coordinates must be a list of two numbers")
        for coordinate in coordinates:
            if not isinstance(coordinate, (int, float)):
                self.data["error"] = True
                self.data["message"].append("Coordinates must be a list of two numbers")
    
    def validate_venue(self , name , city_town , location_desc , coordinates):
        self.data["message"] = []
        self.data["error"] = False
        self.validate_name(name)
        self.validate_name(city_town)
        self.validate_description(location_desc)
        self.validate_coordinates(coordinates)
        return self.data
    
    # ------------- Schedule ----------------------#
    def validate_time(self , start_time , end_time):
        # start_time and end_time should be in datetime format 
        # and start_time should be less than end_time
        # convert string format DD/MM/YYYY/HH/mm to datetime 
        start_time = datetime.strptime(start_time, '%d/%m/%Y/%H/%M')
        end_time = datetime.strptime(end_time, '%d/%m/%Y/%H/%M')
        if start_time > end_time:
            self.data["error"] = True
            self.data["message"].append("Start time should be less than end time")
        else:
            self.data["start_time"] = start_time
            self.data["end_time"] = end_time

    def validate_schedule(self ,venue_id , show_id , language , total_seats , start_time , end_time , price):
        self.data["message"] = []
        self.data["error"] = False
        if(type(venue_id) != int):
            self.data["error"] = True
            self.data["message"].append("Venue id should be an integer")
        if(type(show_id) != int):
            self.data["error"] = True
            self.data["message"].append("show id should be an integer")
        if(type(total_seats) !=int or total_seats < 4):
            self.data["error"] = True
            self.data["message"].append("total seats should be greater than 4")
        if(type(price) != int or price <= 0):
            self.data["error"] = True
            self.data["message"].append("price must be positive")
        self.validate_name(language)
        self.validate_time(start_time , end_time)
        return self.data
    