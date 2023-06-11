from flask_restful import Resource , request
from API.common.validate import Validate
from API.controller.user import getUniqueUsername , signup , signin , signout , fetchUser , updateUser , deleteUser
from API.controller.user import changePassword , getPublicInfo

class User(Resource):
    def post(self , id):
        data = request.get_json()
        username = data['username']
        token = data['token']
        validation_data = Validate().validate_token(username , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now fetch user information
        return fetchUser(username , token)
    
    def get(self , id):
        # get public data if exist
        return getPublicInfo(id)


    def put(self):
        data = request.get_json()
        username = data['username']
        token = data['token']
        name = data['name']
        email = data['email']
        validation_data = Validate().validate_update(username , token , name , email)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now update user information
        return updateUser(username , token , name , email)

    def delete(self):
        data = request.get_json()
        username = data['username']
        token = data['token']
        validation_data = Validate().validate_token(username , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now delete user information
        return deleteUser(username , token)

class UserSignin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        validation_data = Validate().validate_signin(username , password)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        else:
            data = signin(username , password)
        return data

class UserSignup(Resource):
    def post(self):
        # get the user data from the request
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']

        validation_data = Validate().validate_signup(name , email , password)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # get a unique username from database by triming spaces in name
        # and suffix with some number
        username = getUniqueUsername(name)
        data = signup(username , email , name , password)
        return data

class UserSignout(Resource):
    def get(self):
        data  = request.get_json()
        username = data['username']
        token = data['token']
        validation_data = Validate().validate_token(username , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        return signout(username , token)

class UserChangePassword(Resource):
    def put(self):
        data = request.get_json()
        username = data['username']
        token = data['token']
        old_password = data['old_password']
        new_password = data['new_password']
        validation_data = Validate().validate_change_password(username , token , old_password , new_password)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        return changePassword(username , token , old_password , new_password)