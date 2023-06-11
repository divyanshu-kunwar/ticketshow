from API.common.database import db

class Filters(db.Model):
    __tablename__ = "filters"
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(30), nullable=False)
    tagtype = db.Column(db.String(30), nullable=False)

def getFilters():
    # in ascending order of tagname
    filters = db.session.query(Filters).order_by(Filters.tagname.asc()).all()
    data = []
    for filter in filters:
        data.append({
            "id": filter.id,
            "tagname": filter.tagname,
            "tagtype": filter.tagtype
        })
    return data

def addFilters(tagname , tagtype):
    new_filter = Filters(tagname=tagname,tagtype=tagtype)
    try:
        db.session.add(new_filter)
        db.session.commit()
        data = {
            "id": new_filter.id,
            "tagname": tagname,
            "tagtype": tagtype,
            "message": "filter created successfully"
        }
    except:
        data = {
            "error":True,
            "message":"something went wrong"
        }
    return data

def deleteFilter(id):
    filter = db.session.query(Filters).filter_by(id=id).first()
    if filter:
        try:
            db.session.delete(filter)
            db.session.commit()
            data = {
                "message":"filter deleted successfully"
            }
        except:
            data = {
                "error":True,
                "message":"something went wrong"
            }
    else:
        data = {
            "error":True,
            "message":"filter not found"
        }
    return data
