from API.common.database import db
from datetime import datetime

class Shows(db.Model):
    __tablename__ = "showdata"
    showid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    image_url = db.Column(db.String(50))
    rating = db.Column(db.SmallInteger, nullable=False)
    no_of_ratings = db.Column(db.Integer, default=0)
    description = db.Column(db.String(150), nullable=False)
    tags = db.Column(db.String(200))
    release = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

def createShow(name , image_url , description , tags):
    tags = str(tags)
    new_show = Shows(name=name,image_url=image_url,
                rating=40,description=description , tags=tags)
    try:
        db.session.add(new_show)
        db.session.commit()
        data = {
            "showid": new_show.showid,
            "name": name,
            "message": "show created successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }        
    return data

def updateShow(show_id , name , image_url , description , tags):
    tags = str(tags)
    show = db.session.get(Shows, show_id)
    show.name = name
    show.image_url = image_url
    show.description = description
    show.tags = tags
    try:
        db.session.commit()
        data = {
            "showid": show_id,
            "name": name,
            "message": "show updated successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    return data

def addRating(id , new_rating):
    new_rating = int(new_rating)
    show = db.session.get(Shows, id)
    show.rating = new_rating + show.rating * show.no_of_ratings
    show.no_of_ratings += 1
    show.rating = show.rating / show.no_of_ratings
    try:
        db.session.commit()
        data = {
            "showid": id,
            "name": show.name,
            "message": "rating updated successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    return data

def removeRating(id , old_rating):
    show = db.session.get(Shows, id)
    show.rating = show.rating * show.no_of_ratings - old_rating
    show.no_of_ratings -= 1
    try:
        db.session.commit()
        data = {
            "showid": id,
            "name": show.name,
            "message": "rating removed successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    return data

def deleteShow(id):
    show = db.session.get(Shows, id)
    try:
        db.session.delete(show)
        db.session.commit()
        data = {
            "showid": id,
            "name": show.name,
            "message": "show deleted successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    from API.controller.schedule import deleteScheduleByShow
    deleteScheduleByShow(id)
    return data

def fetchShow(id):
    show = db.session.get(Shows, id)
    # remove brackets and single quotes split
    tags = show.tags[1:-1].split(',')
    # replace single quotes 
    tags = [tag.replace("'","").strip() for tag in tags]
    if(show):
        data = {
            "showid": show.showid,
            "name": show.name,
            "image_url": show.image_url,
            "rating": show.rating,
            "no_of_ratings": show.no_of_ratings,
            "description": show.description,
            "tags": tags,
        }
    else:
        data = {
            "error":True,
            "message":"show not found"
        }
    return data

def getShowList(limit=50 , offset=0):
    shows = db.session.query(Shows).limit(limit).offset(offset).all()
    data = []
    for show in shows:
        # remove brackets and single quotes split
        tags = show.tags[1:-1].split(',')
        # replace single quotes 
        tags = [tag.replace("'","").strip() for tag in tags]
        data.append({
            "showid": show.showid,
            "name": show.name,
            "image_url": show.image_url,
            "rating": show.rating,
            "no_of_ratings": show.no_of_ratings,
            "description": show.description,
            "tags": tags,
        })
    return data

def get_first_show_id():
    show = db.session.query(Shows).first()
    return show.showid

def search_show(search_term):
    show = db.session.query(Shows).filter(Shows.name.like('%'+search_term+'%')).first()
    show2 = db.session.query(Shows).filter(Shows.tags.like('%'+search_term+'%')).first()
    show3 = db.session.query(Shows).filter(Shows.description.like('%'+search_term+'%')).first()
    
    show_list = []
    
    if show:
        show_list.append(show)
    if show2:
        show_list.append(show2)
    if show3:
        show_list.append(show3)

    # remove duplicates
    show_list = list(set(show_list))
    data = []
    for show in show_list:
        # remove brackets and single quotes split
        tags = show.tags[1:-1].split(',')
        # replace single quotes 
        tags = [tag.replace("'","").strip() for tag in tags]
        data.append({
            "showid": show.showid,
            "name": show.name,
            "image_url": show.image_url,
            "rating": show.rating,
            "no_of_ratings": show.no_of_ratings,
            "description": show.description,
            "tags": tags,
        })
    return data