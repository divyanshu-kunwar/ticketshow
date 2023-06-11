from API.common.database import db

class Venue(db.Model):
    __tablename__ = "venuedata"
    venueid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    city_town = db.Column(db.String(20), nullable=False)
    location_desc = db.Column(db.String(50), nullable=False)
    coordinates = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)
    no_of_rating = db.Column(db.SmallInteger, default=0)

def createVenue(name , city_town , location_desc , coordinates):
    new_venue = Venue(name=name,city_town=city_town,
                location_desc=location_desc,coordinates=coordinates,rating=40)
    try:
        db.session.add(new_venue)
        db.session.commit()
        data = {
            "venueid": new_venue.venueid,
            "name": name,
            "message": "venue created successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }        
    return data

def updateVenue(venue_id , name , city_town , location_desc , coordinates):
    venue = db.session.get(Venue, venue_id)
    venue.name = name
    venue.city_town = city_town
    venue.location_desc = location_desc
    venue.coordinates = coordinates
    try:
        db.session.commit()
        data = {
            "venueid": venue_id,
            "name": name,
            "message": "venue updated successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    return data

def deleteVenue(venue_id):
    venue = db.session.get(Venue, venue_id)
    try:
        db.session.delete(venue)
        db.session.commit()
        data = {
            "venueid": venue_id,
            "message": "venue deleted successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    # delete related data from other tables
    from API.controller.schedule import deleteScheduleByVenue
    deleteScheduleByVenue(venue_id)
    return data

def addRating(id , new_rating):
    venue = db.session.get(Venue, id)
    venue.rating = new_rating + venue.rating * venue.no_of_rating
    venue.no_of_rating += 1
    venue.rating = venue.rating / venue.no_of_rating
    try:
        db.session.commit()
        data = {
            "venueid": id,
            "message": "venue rating updated successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    return data

def removeRating(id , old_rating):
    venue = db.session.get(Venue, id)
    venue.rating = venue.rating * venue.no_of_rating - old_rating
    venue.no_of_rating -= 1
    venue.rating = venue.rating / venue.no_of_rating
    try:
        db.session.commit()
        data = {
            "venueid": id,
            "message": "venue rating updated successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    return data

def getVenue(venue_id):
    venue = db.session.get(Venue, venue_id)
    data = {
        "venueid": venue.venueid,
        "name": venue.name,
        "city_town": venue.city_town,
        "location_desc": venue.location_desc,
        "coordinates": venue.coordinates,
        "rating": venue.rating,
        "no_of_rating": venue.no_of_rating
    }
    return data

def getVenuesList(limit=25 , offset=0):
    venues = Venue.query.limit(limit).offset(offset).all()
    data = []
    for venue in venues:
        data.append({
            "venueid": venue.venueid,
            "name": venue.name,
            "city_town": venue.city_town,
            "location_desc": venue.location_desc,
            "coordinates": venue.coordinates,
            "rating": venue.rating,
            "no_of_rating": venue.no_of_rating
        })
    return data

def get_first_venue_id():
    venue = Venue.query.first()
    if venue:
        return venue.venueid
    else:
        return None
    

def search_venue(search_term):
    venues = db.session.query(Venue).filter(Venue.name.like('%'+search_term+'%')).all()
    venue2 = db.session.query(Venue).filter(Venue.city_town.like('%'+search_term+'%')).all()
    venue3 = db.session.query(Venue).filter(Venue.location_desc.like('%'+search_term+'%')).all()

    data = {}
    for venue in venues:
        data[venue.venueid] = {
            "venueid": venue.venueid,
            "name": venue.name,
            "city_town": venue.city_town,
            "location_desc": venue.location_desc,
            "coordinates": venue.coordinates,
            "rating": venue.rating,
            "no_of_rating": venue.no_of_rating
        }
    for venue in venue2:
        data[venue.venueid] = {
            "venueid": venue.venueid,
            "name": venue.name,
            "city_town": venue.city_town,
            "location_desc": venue.location_desc,
            "coordinates": venue.coordinates,
            "rating": venue.rating,
            "no_of_rating": venue.no_of_rating
        }
    for venue in venue3:
        data[venue.venueid] = {
            "venueid": venue.venueid,
            "name": venue.name,
            "city_town": venue.city_town,
            "location_desc": venue.location_desc,
            "coordinates": venue.coordinates,
            "rating": venue.rating,
            "no_of_rating": venue.no_of_rating
        }

    # convert dict to list
    data = list(data.values())
    return data