from flask_restful import Resource , request
from flask import render_template
class Servepage(Resource):
    def get(self):
        return render_template("home.html" ,  title="Ticket Show")