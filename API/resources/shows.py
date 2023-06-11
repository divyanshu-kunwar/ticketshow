from flask_restful import Resource , request
from API.controller.shows import createShow , updateShow , deleteShow
from API.controller.shows import fetchShow  , getShowList
from API.controller.admin import fetchAdmin
from API.controller.user import fetchUser
from API.common.validate import Validate

class Shows(Resource):
    def get(self , id):
        return fetchShow(id)

    def post(self):
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
        admin_data = fetchAdmin(adminname , token)
        if(admin_data["error"]==True):
            # return error status and message = admin_data.message
            return {
                "message":admin_data["message"]
            }
        # admin data fetched successfully now create show
        show_name = data['name']
        show_image_url = data['image']
        show_description = data['description']
        show_tags = data['tags']
        validation_data = Validate().validate_show(show_name , show_image_url , show_description , show_tags)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now create show
        return createShow(show_name , show_image_url  , show_description , show_tags)

    def put(self):
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
        admin_data = fetchAdmin(adminname , token)
        if(admin_data["error"]==True):
            # return error status and message = admin_data.message
            return {
                "message":admin_data["message"]
            }
        # admin data fetched successfully now create show
        show_id = data['showid']
        show_name = data['name']
        show_image_url = data['image']
        show_description = data['description']
        show_tags = data['tags']
        validation_data = Validate().validate_show(show_name , show_image_url , show_description , show_tags)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now create show
        return updateShow(show_id , show_name , show_image_url  , show_description , show_tags)
        return {'shows': 'put'}

    def delete(self):
        data = request.get_json()
        adminname = data['admin_name']
        token = data['token']
        validation_data = Validate().validate_token(adminname , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now fetch admin information
        admin_data = fetchAdmin(adminname , token)
        if(admin_data["error"]==True):
            # return error status and message = admin_data.message
            return {
                "message":admin_data["message"]
            }
        # admin data fetched successfully now create show
        show_id = request.args.get('id')
        return deleteShow(show_id)

class ShowList(Resource):
    def get(self):
        data = request.get_json()
        if "limit" in data:
            limit = data['limit']
        else:
            limit = 25
        
        if "offset" in data:
            offset = data['offset']
        else:
            offset = 0
        return getShowList(limit , offset)
