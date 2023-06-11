from flask_restful import Resource , request
from API.controller.admin import fetchAdmin
from API.controller.user import fetchUser
from API.controller.venue import createVenue , updateVenue , getVenue , deleteVenue 
from API.controller.venue import getVenuesList
from API.common.validate import Validate

class Venue(Resource):
    def get(self , id):
        return getVenue(id)

    def post(self):
        data = request.get_json()
        admin_name = data['admin_name']
        token = data['token']
        validation_data = Validate().validate_token(admin_name , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now fetch admin information
        admin_data = fetchAdmin(admin_name , token)
        if(admin_data["error"]==True):
            # return error status and message = admin_data.message
            return {
                "message":admin_data["message"]
            }
        # admin data fetched successfully now create venue
        name = data['name']
        city_town = data['city_town']
        location_desc = data['location_desc']
        coordinates = data['coordinates']
        validation_data = Validate().validate_venue(name , city_town , location_desc , coordinates)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        coordinates = str(coordinates).replace("[" , "").replace("]" , "")
        # data validated successfully now create venue
        return createVenue(name , city_town , location_desc , coordinates)

    def put(self):
        data = request.get_json()
        admin_name = data['admin_name']
        token = data['token']
        validation_data = Validate().validate_token(admin_name , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now fetch admin information
        admin_data = fetchAdmin(admin_name , token)
        if(admin_data["error"]==True):
            # return error status and message = admin_data.message
            return {
                "message":admin_data["message"]
            }
        # admin data fetched successfully now create venue
        venue_id = data['venue_id']
        name = data['name']
        city_town = data['city_town']
        location_desc = data['location_desc']
        coordinates = data['coordinates']
        validation_data = Validate().validate_venue(name , city_town , location_desc , coordinates)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        coordinates = str(coordinates).replace("[" , "").replace("]" , "")
        # data validated successfully now create venue
        return updateVenue(venue_id , name , city_town , location_desc , coordinates)

    def delete(self):
        data = request.get_json()
        admin_name = data['admin_name']
        token = data['token']
        validation_data = Validate().validate_token(admin_name , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now fetch admin information
        admin_data = fetchAdmin(admin_name , token)
        if(admin_data["error"]==True):
            # return error status and message = admin_data.message
            return {
                "message":admin_data["message"]
            }
        # admin data fetched successfully now create venue
        venue_id = request.args.get('id')        
        return deleteVenue(venue_id)

class VenueList(Resource):
    def get(self):
        data = request.get_json()
        if "limit" not in data:
            limit = 10
        else:
            limit = data['limit']

        if "offset" not in data:
            offset = 0
        else:
            offset = data['offset']
        return getVenuesList(limit , offset)
    
