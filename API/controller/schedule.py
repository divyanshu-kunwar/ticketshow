from API.common.database import db
from API.controller.shows import fetchShow
from API.controller.venue import getVenue
from datetime import datetime

# select
from sqlalchemy import select

class Schedule(db.Model):
    __tablename__ = "scheduledata"
    scheduleid = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(20), nullable=False)
    total_seats = db.Column(db.SmallInteger, nullable=False)
    booked_seats = db.Column(db.SmallInteger, default=0)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.SmallInteger, nullable=False)

def createSchedule(venue_id , show_id , language , total_seats , start_time , end_time , price):
    new_schedule = Schedule(venue_id=venue_id,show_id=show_id,
                language=language,total_seats=total_seats,start_time=start_time,end_time=end_time , price=price)
    try:
        db.session.add(new_schedule)
        db.session.commit()
        data = {
            "scheduleid": new_schedule.scheduleid,
            "message": "schedule created successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }        
    return data

def updateSchedule(schedule_id , venue_id , show_id , language , total_seats , start_time , end_time , price):
    schedule = db.session.get(Schedule, schedule_id)
    schedule.venue_id = venue_id
    schedule.show_id = show_id
    schedule.language = language
    schedule.total_seats = total_seats
    schedule.start_time = start_time
    schedule.end_time = end_time
    schedule.price = price
    try:
        db.session.commit()
        data = {
            "scheduleid": schedule_id,
            "message": "schedule updated successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    return data

def deleteSchedule(schedule_id):
    schedule = db.session.get(Schedule, schedule_id)
    try:
        db.session.delete(schedule)
        db.session.commit()
        data = {
            "scheduleid": schedule_id,
            "message": "schedule deleted successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    from API.controller.booking import deleteBookingBySchedule
    deleteBookingBySchedule(schedule_id)
    return data

def getSchedule(schedule_id):
    schedule = db.session.get(Schedule, schedule_id)
    data = {
        "scheduleid": schedule.scheduleid,
        "venue_id": schedule.venue_id,
        "show_id": schedule.show_id,
        "language": schedule.language,
        "total_seats": schedule.total_seats,
        "booked_seats": schedule.booked_seats,
        "start_time": str(schedule.start_time),
        "end_time": str(schedule.end_time),
        "price": schedule.price
    }
    return data

def searchSchedule(language=None , tags=None , city_town=None , rating=1 , date=None , limits=100 , unique = False):
    # print(language , tags , city_town , rating , date , limits)
    # find schedule with given language and date 
    # get city_town from venue table
    # get tags and rating from show table
    # return list of shows
    
    if language is not None or date is not None:
        # query schedule by date and time 
        if language != None and date!= None:
            # change date in dd/mm/yyyy to datetime
            date = datetime.strptime(date, '%d/%m/%Y')
            # language can be a list of languages use or operation to query
            query = db.select(Schedule).where(Schedule.language.in_(language)).where(Schedule.start_time >= date)
            schedules = db.session.execute(query).all()
        elif language != None:
            query = db.select(Schedule).where(Schedule.language.in_(language))
            schedules = db.session.execute(query).all()
        elif date != None:
            date = datetime.strptime(date, '%d/%m/%Y')
            query = db.select(Schedule).where(Schedule.start_time >= date)
            schedules = db.session.execute(query).all()
    else:
        # select all schedules
        query = db.select(Schedule)
        schedules = db.session.execute(query).all()
    
    # get all venue given in schedule and filter by city_town
    schedule_venue_list = []
    for schedule in schedules:
        schedule = schedule[0]
        venue = getVenue(schedule.venue_id)
        if city_town != None:
            if venue["city_town"] == city_town:
                schedule_venue_list.append([
                    {
                        "scheduleid": schedule.scheduleid,
                        "venue_id": schedule.venue_id,
                        "show_id": schedule.show_id,
                        "language": schedule.language,
                        "total_seats": schedule.total_seats,
                        "booked_seats": schedule.booked_seats,
                        "start_time": str(schedule.start_time),
                        "end_time": str(schedule.end_time),
                        "price": schedule.price
                    }
                     , venue])
        else:
            schedule_venue_list.append([{
                "scheduleid": schedule.scheduleid,
                "venue_id": schedule.venue_id,
                "show_id": schedule.show_id,
                "language": schedule.language,
                "total_seats": schedule.total_seats,
                "booked_seats": schedule.booked_seats,
                "start_time": str(schedule.start_time),
                "end_time": str(schedule.end_time),
                "price": schedule.price
            } , venue])

    
    # get all shows given in schedule and filter by tags and rating
    schedule_venue_show_list = []
    for schedule_venue in schedule_venue_list:
        schedule = schedule_venue[0]
        venue = schedule_venue[1]
        shows = fetchShow(schedule["show_id"])
        schedule_venue_show_list.append([schedule , venue , shows])
    
    # filter by tags and rating
    # remove if any of tag in show is not in tags list
    if tags != None:
        new_schedule_venue_show_list = []
        for schedule , venue , show in schedule_venue_show_list:
            if set(tags).intersection(set(show["tags"])):
                new_schedule_venue_show_list.append((schedule , venue , show))
        schedule_venue_show_list = new_schedule_venue_show_list
    
    # remove if rating is less than given rating
    if rating != None:
        new_schedule_venue_show_list = []
        for schedule , venue , show in schedule_venue_show_list:
            if show["rating"] >= int(rating)*10:
                new_schedule_venue_show_list.append((schedule , venue , show))
        schedule_venue_show_list = new_schedule_venue_show_list

        if unique:
            # remove duplicates show id
            show_id = []
            new_schedule_venue_show_list = []
            for schedule , venue , show in schedule_venue_show_list:
                if show["showid"] not in show_id:
                    show_id.append(show["showid"])
                    new_schedule_venue_show_list.append((schedule , venue , show))
            schedule_venue_show_list = new_schedule_venue_show_list
        if(len(schedule_venue_show_list) > limits):
            schedule_venue_show_list = schedule_venue_show_list[:limits]
    
    return schedule_venue_show_list

def getVenueAndScheduleByShow(show_id):
    # get all schedules for given show
    query = db.select(Schedule).where(Schedule.show_id == show_id)
    schedules = db.session.execute(query).all()
    # get all venue given in schedule and filter by city_town
    schedule_venue_dict = {
    }
    for schedule in schedules:
        schedule = schedule[0]
        venue = getVenue(schedule.venue_id)
        # group venue id wise
        if not venue["venueid"] in schedule_venue_dict:
            schedule_venue_dict[venue["venueid"]] = {
                "venueid": venue["venueid"],
                "name": venue["name"],
                "city_town": venue["city_town"],
                "location_desc": venue["location_desc"],
                "coordinates": venue["coordinates"],
                "rating": venue["rating"],
                "no_of_rating": venue["no_of_rating"],
                "schedules": []
            }
        schedule_venue_dict[venue["venueid"]]["schedules"].append({
            "scheduleid": schedule.scheduleid,
            "venue_id": schedule.venue_id,
            "show_id": schedule.show_id,
            "language": schedule.language,
            "total_seats": schedule.total_seats,
            "booked_seats": schedule.booked_seats,
            "start_time": str(schedule.start_time),
            "duration": str(schedule.end_time - schedule.start_time).split(":")[0] + " Hrs " 
            + str(schedule.end_time - schedule.start_time).split(":")[1] + " mins ",
            "price": schedule.price
        })
    return schedule_venue_dict

def getShowAndScheduleByVenue(venue_id):
    # get all schedules for given show
    query = db.select(Schedule).where(Schedule.venue_id == venue_id)
    schedules = db.session.execute(query).all()
    # get all venue given in schedule and filter by city_town
    schedule_show_dict = {
    }
    for schedule in schedules:
        schedule = schedule[0]
        show = fetchShow(schedule.show_id)
        # group venue id wise
        if not show["showid"] in schedule_show_dict:
            schedule_show_dict[show["showid"]] = {
                "showid": show["showid"],
                "name": show["name"],
                "rating": show["rating"],
                "no_of_ratings": show["no_of_ratings"],
                "tags": show["tags"],
                "description": show["description"],
                "image_url": show["image_url"],
                "schedules": []
            }
        schedule_show_dict[show["showid"]]["schedules"].append({
            "scheduleid": schedule.scheduleid,
            "venue_id": schedule.venue_id,
            "show_id": schedule.show_id,
            "language": schedule.language,
            "total_seats": schedule.total_seats,
            "booked_seats": schedule.booked_seats,
            "start_time": str(schedule.start_time),
            "duration": str(schedule.end_time - schedule.start_time).split(":")[0] + " Hrs " 
            + str(schedule.end_time - schedule.start_time).split(":")[1] + " mins ",
            "price": schedule.price
        })
    return schedule_show_dict

def addBooking(schedule_id , seats):
    schedule = db.session.get(Schedule, schedule_id)
    schedule.booked_seats += seats
    db.session.commit()

def removeBooking(schedule_id , seats):
    schedule = db.session.get(Schedule, schedule_id)
    schedule.booked_seats -= seats
    db.session.commit()

def deleteScheduleByVenue(venue_id):
    query = db.select(Schedule).where(Schedule.venue_id == venue_id)
    schedules = db.session.execute(query).all()
    for schedule in schedules:
        schedule = schedule[0]
        db.session.delete(schedule)
    db.session.commit()

def deleteScheduleByShow(show_id):
    query = db.select(Schedule).where(Schedule.show_id == show_id)
    schedules = db.session.execute(query).all()
    for schedule in schedules:
        schedule = schedule[0]
        db.session.delete(schedule)
    db.session.commit()

def getAvailableSeats(schedule_id):
    schedule = db.session.get(Schedule, schedule_id)
    return schedule.total_seats - schedule.booked_seats