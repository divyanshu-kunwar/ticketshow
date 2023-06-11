import matplotlib.pyplot as plt
import plotly.express as px

def renderGraph(data):
    print("Rendering graph...")

    language = []
    tags = {

    }

    seats = {
        "name": [],
        "booked_seats" : [],
        "total_seats" :[],
        "rating" : []
    }

    show_lang_book_percentage={
        
    }

    for key in data:

        seats['name'].append(data[key]['name'][0:12])
        seats['rating'].append(data[key]['rating']/10)
        for tag in data[key]['tags']:
            if tag in tags:
                tags[tag] += 1
            else:
                tags[tag] = 1

        booked_ = 0
        total_ = 0
        for schedule in data[key]['schedules']:
            booked_ += schedule['booked_seats']
            total_ += schedule['total_seats']
        seats['booked_seats'].append(booked_)
        seats['total_seats'].append(total_)



    fig =px.bar(seats, x="name", y="rating", template="plotly_dark")
    fig.update_layout(title="Rating Of Shows", xaxis_title="Name", yaxis_title="Rating")
    fig.write_html("static/rating.html" , include_plotlyjs='cdn')

    # a pie chart of tags 
    fig = px.pie(values=tags.values(), names=tags.keys(), template="plotly_dark")
    fig.update_layout(title="Tags Of Shows", xaxis_title="Name", yaxis_title="Rating")
    fig.write_html("static/tags.html" , include_plotlyjs='cdn')

    # a stacked bar chart booked seats vs total seats vs name
    fig = px.bar(seats, x="name", y=["booked_seats", "total_seats"], barmode="stack", template="plotly_dark")
    fig.write_html("static/booked_seats.html" , include_plotlyjs='cdn')


