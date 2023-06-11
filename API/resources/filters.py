from flask_restful import Resource , request
from API.controller.filters import getFilters, addFilters , deleteFilter

class Filters(Resource):
    def get(self):
        return getFilters()
    
    def post(self):
        tag_type_list = ["language" , "tags" , "city"]
        data = request.get_json()
        tagname = data["tagname"]
        tagtype = data["tagtype"]
        if tagtype not in tag_type_list:
            return {
                "error":True ,
                "message":"tagtype must be one of the following: {}".format(tag_type_list)
            }        
        return addFilters(tagname , tagtype)
    
    def delete(self , id):
        return deleteFilter(id)