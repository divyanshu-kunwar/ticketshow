from flask_restful import Resource , request
from API.controller.schedule import createSchedule , updateSchedule , getSchedule , deleteSchedule, searchSchedule
from API.controller.schedule import getShowAndScheduleByVenue , getVenueAndScheduleByShow
from API.common.validate import Validate
from API.controller.admin import fetchAdmin

class Schedule(Resource):
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
        # admin data fetched successfully now create schedule
        venue_id = data['venue_id']
        show_id = data['show_id']
        language = data['language']
        total_seats = data['total_seats']
        start_time = data['start_time']
        end_time = data['end_time']
        price = data['price']
        validation_data = Validate().validate_schedule(venue_id , show_id , language , total_seats , start_time , end_time , price)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # start_time and end_time is in format dd/mm/YYYY/hh/MM
        start_time = validation_data["start_time"]
        end_time = validation_data["end_time"]

        # schedule data validated successfully now create schedule
        schedule_data = createSchedule(venue_id , show_id , language , total_seats , start_time , end_time , price)
        return schedule_data

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
        # admin data fetched successfully now create schedule
        schedule_id = data['schedule_id']
        venue_id = data['venue_id']
        show_id = data['show_id']
        language = data['language']
        total_seats = data['total_seats']
        start_time = data['start_time']
        end_time = data['end_time']
        price = data['price']
        validation_data = Validate().validate_schedule(venue_id , show_id , language , total_seats , start_time , end_time , price)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # start_time and end_time is in format dd/mm/YYYY/hh/MM
        start_time = validation_data["start_time"]
        end_time = validation_data["end_time"]
        # schedule data validated successfully now create schedule
        schedule_data = updateSchedule(schedule_id , venue_id , show_id , language , total_seats , start_time , end_time , price)
        return schedule_data

    def get(self):
        data = request.get_json()
        schedule_id = data['schedule_id']
        return getSchedule(schedule_id)
    
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
        # admin data fetched successfully now delete schedule
        schedule_id = request.args.get('id')
        return deleteSchedule(schedule_id)

class ScheduleSearch(Resource):
    def get(self):
        data = request.get_json()
        # searchSchedule(language=None , tags=None , city_town=None , rating=None , date=None , limits=25)
        if "language" in data:
            language = data["language"]
        else:
            language = None

        if "tags" in data:
            tags = data["tags"]
        else:
            tags = None
        
        if "city_town" in data:
            city_town = data["city_town"]
        else:
            city_town = None
        
        if "rating" in data:
            rating = data["rating"]
        else:
            rating = None
        
        if "date" in data:
            date = data["date"]
        else:
            date = None
        
        if "limits" in data:
            limits = data["limits"]
        else:
            limits = 25
        
        return searchSchedule(language , tags , city_town , rating , date , limits)

class ScheduleVenue(Resource):
    def get(self , id):
        return getShowAndScheduleByVenue(id)
    
class ScheduleShow(Resource):
    def get(self , id):
        return getVenueAndScheduleByShow(id)