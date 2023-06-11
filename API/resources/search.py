from flask_restful import Resource

from API.controller.shows import search_show
from API.controller.venue import search_venue

class Search(Resource):
    def get(self , term):
        shows = search_show(term)
        venues = search_venue(term)


        data = {
            "shows": shows,
            "venues": venues
        }
        return data