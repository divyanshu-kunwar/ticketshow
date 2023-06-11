from flask_restful import Resource , request
from API.controller.user import fetchUser
from API.common.validate import Validate
from API.controller.booking import createBooking , getBooking , deleteBooking, getBookingByUser
from API.controller.booking import addShowRating , addVenueRating , removeShowRating , removeVenueRating
from API.controller.schedule import getSchedule
from API.controller.shows import fetchShow
from API.controller.venue import getVenue


class Booking(Resource):
    def get(self):
        data = request.get_json()
        booking_id = data['booking_id']
        return getBooking(booking_id)

    def post(self):
        data = request.get_json()
        user_name = data['user_name']
        token = data['token']
        validation_data = Validate().validate_token(user_name , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now fetch user information
        user_data = fetchUser(user_name , token)
        if(user_data["error"]==True):
            # return error status and message = user_data.message
            return {
                "message":user_data["message"]
            }
        # user data fetched successfully now create booking
        schedule_id = data['schedule_id']
        no_of_seats = data['no_of_seats']
        return createBooking(user_data["userid"] , schedule_id , no_of_seats)
    
    def delete(self):
        data = request.get_json()
        user_name = data['user_name']
        token = data['token']
        validation_data = Validate().validate_token(user_name , token)
        if(validation_data["error"] == True):
            # return error status and message = validation_data.message
            return {
                "message":validation_data["message"]
            }
        # data validated successfully now fetch user information
        user_data = fetchUser(user_name , token)
        if(user_data["error"]==True):
            # return error status and message = user_data.message
            return {
                "message":user_data["message"]
            }
        # user data fetched successfully now delete booking
        booking_id = data['booking_id']
        return deleteBooking(user_data["userid"] ,booking_id)

class BookingById(Resource):
    def get(self , id):
        bookings =  getBookingByUser(id)
        schedule_booking_list = []

        for booking in bookings:
            schedule = getSchedule(booking['schedule_id'])
            print(schedule)
            # get venue name
            venue = getVenue(schedule['venue_id'])
            # get show name
            show = fetchShow(schedule['show_id'])
            schedule_booking_list.append({
                "schedule":schedule,
                "booking":booking,
                "venue":venue,
                "show":show
            })

        return {
            "message":"success",
            "data":schedule_booking_list
        } 

class Rating(Resource):
    def post(self , booking_id , venue_id , rating):
        rating = int(rating)*10
        return addVenueRating(booking_id , rating , venue_id)

    def delete(self , booking_id , venue_id):
        return removeVenueRating(booking_id , venue_id)
    
    def post(self , booking_id , show_id , rating):
        rating = int(rating)*10
        return addShowRating(booking_id , rating , show_id)
    
    def delete(self , booking_id , show_id):
        return removeShowRating(booking_id , show_id)
                
