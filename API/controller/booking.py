from API.common.database import db
from API.controller.schedule import addBooking, removeBooking , getAvailableSeats

class Booking(db.Model):
    __tablename__ = "bookingdata"
    bookingid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False )
    no_of_seats = db.Column(db.SmallInteger, nullable=False)
    schedule_id = db.Column(db.Integer, nullable=False)
    venue_rating = db.Column(db.SmallInteger, nullable=True)
    show_rating = db.Column(db.SmallInteger, nullable=True)

def createBooking(userid , schedule_id , no_of_seats):
    # create booking only if seats are available
    if getAvailableSeats(schedule_id) > int(no_of_seats):
        new_booking = Booking(userid=userid,no_of_seats=no_of_seats,schedule_id=schedule_id)
        try:
            db.session.add(new_booking)
            db.session.commit()
            data = {
                "bookingid": new_booking.bookingid,
                "message": "booking created successfully"
            }
            addBooking(schedule_id , int(no_of_seats))
        except:
            data = {
                "error":True,
                "message":"something went wrong"
            }
    else:
        data = {
            "error":True,
            "message":"no seats available"
        }
    return data

def deleteBooking(userid , booking_id):
    booking = db.session.get(Booking, booking_id)
    if booking.userid == userid:
        try:
            db.session.delete(booking)
            db.session.commit()
            data = {
                "message": "booking deleted successfully"
            }
            removeBooking(booking.schedule_id , booking.no_of_seats)
        except:
            data = {
                "error":True,
                "message":"something went wrong"
            }
    else:
        data = {
            "error":True,
            "message":"user not authorized"
        }
    return data

def getBooking(booking_id):
    booking = db.session.get(Booking, booking_id)
    if booking:
        data = {
            "bookingid": booking.bookingid,
            "userid": booking.userid,
            "no_of_seats": booking.no_of_seats,
            "schedule_id": booking.schedule_id
        }
    else:
        data = {
            "error":True,
            "message":"booking not found"
        }
    return data

def deleteBookingBySchedule(schedule_id):
    try:
        db.session.query(Booking).filter(Booking.schedule_id == schedule_id).delete()
        db.session.commit()
        data = {
            "message": "booking deleted successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    return data

def getBookingByUser(userid):
    bookings = db.session.query(Booking).filter(Booking.userid == userid).all()
    if bookings:
        data = []
        for booking in bookings:
            data.append({
                "bookingid": booking.bookingid,
                "userid": booking.userid,
                "no_of_seats": booking.no_of_seats,
                "schedule_id": booking.schedule_id,
                "venue_rating": booking.venue_rating,
                "show_rating": booking.show_rating
            })
    else:
        data = {
            "error":True,
            "message":"booking not found"
        }
    return data

def addVenueRating(booking_id , rating , venue_id):
    booking = db.session.get(Booking, booking_id)
    if booking:
        booking.venue_rating = rating
        db.session.commit()
        data = {
            "message": "venue rating added successfully"
        }
    else:
        data = {
            "error":True,
            "message":"booking not found"
        }
    # update venue rating
    from API.controller.venue import addRating
    addRating(venue_id , rating)
    return data

def removeVenueRating(booking_id , venue_id):
    booking = db.session.get(Booking, booking_id)
    old_rating = booking.venue_rating
    if booking:
        booking.venue_rating = None
        db.session.commit()
        data = {
            "message": "venue rating removed successfully"
        }
    else:
        data = {
            "error":True,
            "message":"booking not found"
        }

    # update venue rating
    from API.controller.venue import removeRating
    removeRating(venue_id , old_rating)
    return data

def addShowRating(booking_id ,rating, show_id):
    booking = db.session.get(Booking, booking_id)
    if booking:
        booking.show_rating = rating
        db.session.commit()
        data = {
            "message": "show rating added successfully"
        }
    else:
        data = {
            "error":True,
            "message":"booking not found"
        }

    # update show rating
    from API.controller.shows import addRating
    addRating(show_id , rating)
    return data

def removeShowRating(booking_id , show_id):
    booking = db.session.get(Booking, booking_id)
    old_rating = booking.show_rating
    if booking:
        booking.show_rating = None
        db.session.commit()
        data = {
            "message": "show rating removed successfully"
        }
    else:
        data = {
            "error":True,
            "message":"booking not found"
        }

    # update show rating
    from API.controller.shows import removeRating
    removeRating(show_id , old_rating)
    return data
