let name_input = document.getElementById("name")
let user_email_input = document.getElementById("user_email")

user_id = localStorage.getItem("userid")
user_name = localStorage.getItem("username")
token = localStorage.getItem("token")
user_email = ""
name_ = ""

window.addEventListener("DOMContentLoaded" , ()=>{
    
    fetch(`/api/user/${user_id}`,{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: user_name,
            token: token
        })
    }).then((res)=>{
        res.json().then((data)=>{
            if(!data["message"]){
                console.log(data)
                name_input.value = data.name
                user_email_input.value = data.email
                user_name = data.username
                user_email = data.email
                name_ = data.name
            }else{
                // TODO : Error message
                window.alert(data["message"])
            }
        })
    })

})

name_input.addEventListener("change" , ()=>{
    if (name_input.value != name_ || user_email_input.value != user_email){
        document.getElementById("update_profile").classList.remove("disabledBtn")
    }else{
        document.getElementById("update_profile").classList.add("disabledBtn")
    }
})

user_email_input.addEventListener("change" , ()=>{
    if (name_input.value != name_ || user_email_input.value != user_email){
        document.getElementById("update_profile").classList.remove("disabledBtn")
    }else{
        document.getElementById("update_profile").classList.add("disabledBtn")
    }
})

document.getElementById("update_profile").addEventListener("click" , ()=>{
    if (name_input.value != name_ || user_email_input.value != user_email){
        fetch(`/api/user`,{
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name_input.value,
                username: user_name,
                email: user_email_input.value,
                token: token
            })
        }).then((res)=>{
            res.json().then((data)=>{
                if(!data["message"]){
                    // TODO : Success message
                    window.alert("Profile updated successfully")
                    window.location.href = "/profile"
                }else{
                    // TODO : Error message
                    window.alert(data["message"])
                }
            })
        })
    }
})

curr_password_input = document.getElementById("curr_password")
new_password_input = document.getElementById("new_password")

curr_password_input.addEventListener("change" , ()=>{
    if (curr_password_input.value != "" && new_password_input.value != ""){
        document.getElementById("change_passsword").classList.remove("disabledBtn")
    }else{
        document.getElementById("change_passsword").classList.add("disabledBtn")
    }
})

new_password_input.addEventListener("change" , ()=>{
    if (curr_password_input.value != "" && new_password_input.value != ""){
        document.getElementById("change_passsword").classList.remove("disabledBtn")
    }else{
        document.getElementById("change_passsword").classList.add("disabledBtn")
    }
})

document.getElementById("change_passsword").addEventListener("click" , ()=>{
    if (curr_password_input.value != "" && new_password_input.value != ""){
        fetch(`/api/user/change_password`,{
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: user_name,
                old_password: curr_password_input.value,
                new_password: new_password_input.value,
                token: token
            })
        }).then((res)=>{
            res.json().then((data)=>{
                if(!data["message"]){
                    // TODO : Success message
                    window.alert("Password changed successfully")
                    window.location.href = "/profile"
                }else{
                    // TODO : Error message
                    window.alert(data["message"])
                }
            })
        })
    }
})


window.addEventListener("DOMContentLoaded" , ()=>{
    // get all the bookings of the user
    
    userid = localStorage.getItem("userid")
    fetch("/api/user/booking/"+user_id , {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
        
    }).then((res)=>{
        res.json().then((data)=>{
            if(data["message"]=='success'){
                data.data.forEach(element => {
                    console.log(element)
                    // element.booking
                    // element.schedule
                    // element.show
                    // element.venue

                    // create a card for each booking
                    let html =`
                    <div class="booked_shows_info">
                        <div class="ticket_info">
                        <div class="details">
                        <div class="booking_id">Booking Id : <span>
                        ${element.venue.city_town.substring(0,3).toUpperCase()}
                        ${element.venue.venueid}${element.show.showid}${element.schedule.scheduleid}
                        ${element.booking.userid}${element.booking.bookingid+23}
                        </span>
                        </div>
                        <div class="qr_code">
                            <img src="static/media/qr_code.svg" alt=""></div>
                        </div>
                        <div class="quantity">
                            <div class="quantity_number"><span>
                            ${element.booking.no_of_seats}</span>
                             Tickets</div>
                        </div>
                    </div>
                    <div class="show_info">
                        <div>
                            <div class="name"><span>
                            ${element.show.name}
                            </span></div>
                            <div class="info"><span>
                            ${element.schedule.language}
                            </span></div>
                            <div class="venue">
                            <span>
                            ${element.venue.name}:${element.venue.city_town}
                             </span>
                            </div>
                        </div>
                        <div class="event_show_image">
                                <img src="${element.show.image_url}" alt="">
                        </div>
                    </div>

                    <div class="date_container">
                        ${element.schedule.start_time}
                    </div>

                    <div class="feedback" 
                    onclick="Rating(${element.booking.bookingid},${element.show.showid},${element.venue.venueid},${element.booking.show_rating},${element.booking.venue_rating})">
                    Rate Show And Venue
                    </div>


                    <div class="left_punch punch"></div>
                    <div class="right_punch punch"></div>
            </div>
                    `
                    document.getElementById("profile_container_right").innerHTML += html
                });
            }
        })
    })
})

function Rating(bookingid , showid , venueid, show_rating, venue_rating){
    document.getElementById("bookingid").innerHTML = bookingid;
    document.getElementById("showid").innerHTML = showid;
    document.getElementById("venueid").innerHTML = venueid;
    document.getElementById("show_rating").innerHTML = show_rating;
    document.getElementById("venue_rating").innerHTML = venue_rating;
    document.getElementById("RatingContainer").style.display = "flex";
}

function closeRating(){
    document.getElementById("RatingContainer").style.display = "none";
}

function setRating(){
    let bookingid = document.getElementById("bookingid").innerHTML;
    let showid = document.getElementById("showid").innerHTML;
    let venueid = document.getElementById("venueid").innerHTML;
    let show_rating = document.getElementById("show_rating").innerHTML;
    let venue_rating = document.getElementById("venue_rating").innerHTML;
    
    /*
    
    "/api/rating/<string:rating>/book/<string:booking_id>/show/<string:show_id>" ,
    "/api/rating/<string:rating>/book/<string:booking_id>/venue/<string:venue_id>",
    "/api/remove_rating/book/<string:booking_id>/show/<string:show_id>",
    "/api/remove_rating/book/<string:booking_id>/venue/<string:venue_id>"

    if rating is null just add the rating 
    else remove first and then add the rating

    */

    let new_show_rating = 0;
    let new_venue_rating = 0;

    document.getElementsByName("rateshow").forEach((element)=>{
        if(element.checked){
            new_show_rating = element.value;
        }
    })

    console.log("new show rating is " , new_show_rating)

    document.getElementsByName("ratevenue").forEach((element)=>{
        if(element.checked){
            new_venue_rating = element.value;
        }
    })

    console.log("new venue rating is " , new_venue_rating)

    fetch("/api/rating/"+new_show_rating+"/book/"+bookingid+"/show/"+showid , {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res)=>{
        res.json().then((data)=>{
            console.log("show rating added")
            console.log(data)
        })
    })

    fetch("/api/rating/"+new_venue_rating+"/book/"+bookingid+"/venue/"+venueid , {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    }).then((res)=>{
        res.json().then((data)=>{
            console.log(data)
            console.log("venue rating added")

        })
    })


    closeRating();
    window.alert("Rating Added Successfully");
    window.location.reload();


}