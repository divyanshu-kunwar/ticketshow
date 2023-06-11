from flask_restful import Resource , request
from API.common.validate import Validate
from API.controller.admin import getUniqueAdminname , signup , signin , signout , fetchAdmin , updateAdmin , deleteAdmin
from API.controller.admin import changePassword

class Admin(Resource):
    def get(self):
        data = request.get_json()
        adminname = data['adminname']
        token = data['token']
        validation_data = Validate().validate_token(adminname , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now fetch admin information
        return fetchAdmin(adminname , token)

    def put(self):
        data = request.get_json()
        adminname = data['adminname']
        token = data['token']
        name = data['name']
        email = data['email']
        validation_data = Validate().validate_update(adminname , token , name , email)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now update admin information
        return updateAdmin(adminname , token , name , email)

    def delete(self):
        data = request.get_json()
        adminname = data['adminname']
        token = data['token']
        validation_data = Validate().validate_token(adminname , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now delete admin information
        return deleteAdmin(adminname , token)

class AdminSignin(Resource):
    def post(self):
        data = request.get_json()
        adminname = data['adminname']
        password = data['password']
        validation_data = Validate().validate_signin(adminname , password)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        else:
            data = signin(adminname , password)
        return data

class AdminSignup(Resource):
    def post(self):
        # get the admin data from the request
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
        # get a unique adminname from database by triming spaces in name
        # and suffix with some number
        adminname = getUniqueAdminname(name)
        data = signup(adminname , email, name, password)
        return data

class AdminSignout(Resource):
    def get(self):
        data  = request.get_json()
        adminname = data['adminname']
        token = data['token']
        validation_data = Validate().validate_token(adminname , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        return signout(adminname , token)

class AdminChangePassword(Resource):
    def put(self):
        data = request.get_json()
        adminname = data['adminname']
        token = data['token']
        old_password = data['old_password']
        new_password = data['new_password']
        validation_data = Validate().validate_change_password(adminname , token , old_password , new_password)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        return changePassword(adminname , token , old_password , new_password)