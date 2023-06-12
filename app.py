import os
from flask import Flask , render_template , request
from flask_restful import Api
from datetime import datetime

from API.resources.user import User , UserSignin , UserSignup , UserSignout , UserChangePassword
from API.resources.admin import Admin , AdminSignin , AdminSignup , AdminSignout , AdminChangePassword
from API.resources.shows import Shows , ShowList 
from API.resources.venue import Venue , VenueList
from API.resources.booking import Booking , BookingById , Rating
from API.resources.schedule import Schedule , ScheduleSearch
from API.resources.schedule import ScheduleShow , ScheduleVenue
from API.resources.filters import Filters
from API.resources.search import Search

from API.controller.schedule import searchSchedule , getVenueAndScheduleByShow , getShowAndScheduleByVenue, getSchedule
from API.controller.filters import getFilters
from API.controller.shows import fetchShow , getShowList , get_first_show_id
from API.controller.venue import getVenue , getVenuesList , get_first_venue_id

from API.common.database import db
from API.common.Graph import renderGraph

app = Flask(__name__)
api = Api(app)

current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(current_dir , './Data/data2.sqlite3')

db.init_app(app)
app.app_context().push()

# --------------------------------- /api/user ---------------------------------
api.add_resource(User , "/api/user" , "/api/user/<string:id>")
api.add_resource(UserSignin , "/api/user/signin")
api.add_resource(UserSignup , "/api/user/signup")
api.add_resource(UserSignout , "/api/user/signout")
api.add_resource(UserChangePassword , "/api/user/change_password")

# --------------------------------- /api/admin ---------------------------------
api.add_resource(Admin , "/api/admin" , "/api/admin/<string:id>")
api.add_resource(AdminSignin , "/api/admin/signin")
api.add_resource(AdminSignup , "/api/admin/signup")
api.add_resource(AdminSignout , "/api/admin/signout")
api.add_resource(AdminChangePassword , "/api/admin/change_password")


# --------------------------------- /api/shows -----------------------------------
api.add_resource(Shows , "/api/shows/" , "/api/shows/<string:id>")
api.add_resource(ShowList , "/api/show/list")

# --------------------------------- /api/venue -----------------------------------
api.add_resource(Venue , "/api/venue/")
api.add_resource(VenueList , "/api/venue/list")

# --------------------------------- /api/schedule ---------------------------------
api.add_resource(Schedule , "/api/schedule/" , "/api/schedule/<string:id>" , "/api/schedule/show/<string:showid>")
api.add_resource(ScheduleShow , "/api/schedule/show/<string:id>")
api.add_resource(ScheduleVenue , "/api/schedule/venue/<string:id>")

# --------------------------------- /api/booking ---------------------------------
api.add_resource(Booking , "/api/booking" , "/api/booking/<string:id>" , "/api/booking/user/<string:userid>")
api.add_resource(BookingById , "/api/user/booking/<string:id>")
api.add_resource(Rating, 
"/api/rating/<string:rating>/book/<string:booking_id>/show/<string:show_id>" ,
"/api/rating/<string:rating>/book/<string:booking_id>/venue/<string:venue_id>",
"/api/remove_rating/book/<string:booking_id>/show/<string:show_id>",
"/api/remove_rating/book/<string:booking_id>/venue/<string:venue_id>"
)
# --------------------------------- /api/search ---------------------------------
api.add_resource(ScheduleSearch , "/api/search/schedule") 
api.add_resource(Search , "/api/search/<string:term>") 

# -------------------------------- /api/filters ---------------------------------
api.add_resource(Filters , "/api/filters/" , "/api/filters/<string:id>")


# -------------------------- serve static files ---------------------------------
@app.route("/" , methods=["GET"])
def index():
    data = searchSchedule(limits=6 , unique=True)
    return render_template("home.html" ,
         title="Home - Ticket Show" , data = data)

@app.route("/signin" , methods=["GET"])
def signin():
    return render_template("signin.html" ,
         title="Signin - Ticket Show")

@app.route("/signup" , methods=["GET"])
def signup():
    return render_template("signup.html" ,
         title="Signup - Ticket Show")


@app.route("/dashboard/" , methods=["GET"])
def dashboard2():
    location = request.args.get("location") or None
    language = request.args.get("language") or None
    language = language.split(",") if language else None
    tags = request.args.get("tags") or None
    tags = tags.split(",") if tags else None
    rating = request.args.get("rating") or None

    print("location" , location)
    print("language" , language)
    print("tags" , tags)
    print("rating" , rating)

    data = searchSchedule(city_town=location , language=language , tags=tags , rating=rating)
    
    filter_data = getFilters()
    language = []
    city = []
    tags = []
    for i in filter_data:
        if i["tagtype"] == "language":
            language.append(i["tagname"])
        elif i["tagtype"] == "city":
            city.append(i["tagname"])
        elif i["tagtype"] == "tags":
            tags.append(i["tagname"])
    filter_data = {
        "language":language ,
        "city":city ,
        "tags":tags
    }
    shows = []
    venue = []
    schedule = []
    for elem in data:
        if elem[2] not in shows:
            shows.append(elem[2])
        if elem[1] not in venue:
            venue.append(elem[1])
        if elem[0] not in schedule:
            schedule.append(elem[0])
    data = {
        "shows":shows ,
        "venue":venue ,
        "schedule":schedule
    }

    return render_template("dashboard.html" ,
            title="Dashboard - Ticket Show" ,
                filter_data=filter_data,
                data=data)


@app.route("/show_detail/<string:id>" , methods=["GET"])
def show_detail(id):
    show = fetchShow(id)
    schedule_detail = getVenueAndScheduleByShow(id)
    return render_template("shows_detail.html" ,
         title="Show Details - Ticket Show" , show=show
         , schedule=schedule_detail)

@app.route("/venue_detail/<string:id>" , methods=["GET"])
def venue_detail(id):
    venue = getVenue(id)
    show = getShowAndScheduleByVenue(id)
    return render_template("venue_detail.html" ,
         title="Venue Details - Ticket Show"
         , venue=venue , show=show )

@app.route("/profile" , methods=["GET"])
def user_profile():
    return render_template("user_profile.html" ,
         title="User Profile - Ticket Show")

@app.route("/admin/dashboard/" , methods=["GET"])
def admin_dashboard():
    default_venue_id = get_first_venue_id()
    if default_venue_id != None:
        venue_id = request.args.get("id") or default_venue_id
        venue_all = getVenuesList()
        venue_selected = getShowAndScheduleByVenue(venue_id)
        return render_template("venue(admin).html" ,
            title="Admin Dashboard - Ticket Show" , 
            venue_all=venue_all,  shows=venue_selected , 
            selected_venue=int(venue_id))
    else:
        return render_template("venue(admin).html" ,
            title="Admin Dashboard - Ticket Show" ,
            venue_all=[],  shows=[] , selected_venue=None)

@app.route("/admin/shows/" , methods=["GET"])
def admin_show_detail():
    show_all = getShowList()
    return render_template("show(admin).html" ,
         title="Shows - Ticket Show" ,
         shows=show_all)

@app.route("/admin/show/edit/<string:id>" , methods=["GET"])
def admin_edit_show(id):
    show = fetchShow(id)
    tags = getFilters()
    # remove all the tags which are not tags
    tags = [i for i in tags if i["tagtype"] == "tags"]
    return render_template("admin_edit_show.html" ,
         title="Edit Show - Ticket Show" , 
         show=show , tags=tags)

@app.route("/admin/venue/edit/<string:id>" , methods=["GET"])
def admin_edit_venue(id):
    venue = getVenue(id)
    tags = getFilters()
    # remove all the tags which are not city
    cities = [i for i in tags if i["tagtype"] == "city"]
    return render_template("admin_edit_venue.html" ,
         title="Edit Venue - Ticket Show" , venue=venue,
         cities=cities)

@app.route("/admin/show/add/" , methods=["GET"])
def admin_create_show():
    tags = getFilters()
    # remove all the tags which are not tags
    tags = [i for i in tags if i["tagtype"] == "tags"]
    return render_template("admin_create_show.html" ,
         title="Create Show - Ticket Show"
         ,tags=tags)

@app.route("/admin/venue/add/" , methods=["GET"])
def admin_create_venue():
    tags = getFilters()
    # remove all the tags which are not city
    cities = [i for i in tags if i["tagtype"] == "city"]
    return render_template("admin_create_venue.html" ,
         title="Create Venue - Ticket Show"
         ,cities=cities)

@app.route("/admin/schedule/add/" , methods=["GET"])
def admin_create_schedule():
    # get all languages
    tags = getFilters()
    # remove all the tags which are not language
    languages = [i for i in tags if i["tagtype"] == "language"]
    default_venue_id = get_first_venue_id()
    venue_id = request.args.get("id") or default_venue_id
    shows = getShowList()
    venue_detail = getVenue(venue_id)
    return render_template("admin_create_schedule.html" ,
            title="Create Schedule - Ticket Show" , shows=shows,
             venue_detail=venue_detail , languages=languages)

@app.route("/book/new/<string:id>" , methods=["GET"])
def bookticket(id):
    schedule = getSchedule(id)
    venue = getVenue(schedule["venue_id"])
    show = fetchShow(schedule["show_id"])
    return render_template(
        "book_ticket.html" , 
        schedule=schedule , 
        venue=venue , show=show)

@app.route("/admin/venue/summary/" , methods=["GET"])
def admin_summary():
    venue_id = request.args.get("id") or get_first_venue_id()
    venue_detail = getVenue(venue_id)
    show = getShowAndScheduleByVenue(venue_id)

    # render html 
    renderGraph(show)

    return render_template("admin_summary.html" ,
            title="Summary - Ticket Show" , 
            venue_detail=venue_detail,
            show=show)

@app.route("/admin/schedule/edit/<string:id>" , methods=["GET"])
def admin_edit_schedule(id):
    schedule = getSchedule(id)
    venue_detail = getVenue(schedule["venue_id"])
    show = fetchShow(schedule["show_id"])
    # convert start_time to datetime from string
    start_time_ = datetime.strptime(schedule["start_time"] , "%Y-%m-%d %H:%M:%S")
    end_time_ = datetime.strptime(schedule["end_time"] , "%Y-%m-%d %H:%M:%S")
    schedule["duration"] = int((end_time_ - start_time_).seconds / 60)
    tags = getFilters()
    # remove all the tags which are not language
    languages = [i for i in tags if i["tagtype"] == "language"]
    return render_template("admin_edit_schedule.html" ,
            title="Edit Schedule - Ticket Show" , 
            schedule=schedule , venue_detail=venue_detail , show=show,
            languages=languages)


# if __name__ == "__main__":
#     app.run(debug=True)
