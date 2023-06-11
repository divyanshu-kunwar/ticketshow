window.addEventListener('resize', function() {
    measure();
});

window.addEventListener('load', function() {
    loadtheme();
    measure();

});

function measure(){
    document.getElementById('measure').innerHTML = window.innerWidth + 'px X ' + window.innerHeight + 'px'; 

    let navheight = document.getElementById('navbar').offsetHeight;
    // add 20px to the height of the navbar by changing to int
    navheight = parseInt(navheight) + 40;
    document.getElementsByTagName('body')[0].style.marginTop = navheight+ 'px';

}

function loadtheme(){
    if(localStorage.getItem('theme') == 'dark'){
        document.getElementById('themeBtn').setAttribute('src', '/static/media/dark_icon.svg'); 
        document.getElementById('light_css').setAttribute('rel' , 'stylesheet alternate');  
        document.getElementById('dark_css').setAttribute('rel' , 'stylesheet');  
    }
    else{
        document.getElementById('themeBtn').setAttribute('src', '/static/media/light_icon.svg');
        document.getElementById('light_css').setAttribute('rel' , 'stylesheet');  
        document.getElementById('dark_css').setAttribute('rel' , 'stylesheet alternate');  
    }
}

function changetheme(){

    if(localStorage.getItem('theme') == 'dark'){
        localStorage.setItem('theme', 'light');
    }
    else{
        localStorage.setItem('theme', 'dark');
    }
    loadtheme();
}

function showPrompt(url){
    //  show a prompt asking for the user if they really want to delete
    let prompt = confirm('Are you sure you want to delete this?');
    admin_name = localStorage.getItem('adminname');
    token = localStorage.getItem('token');
    if(prompt){
        console.log('deleting');

        fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'admin_name': admin_name,
                'token': token
            })
        }).then(function(response){
            return response.json();
        }).then(function(data){
            console.log(data);
            window.alert(data['message']);
            window.location.href = '/admin/dashboard'
        });
    
    }
}

function logout(){
    localStorage.clear();
    window.location.href = '/';
    localStorage.setItem('theme', 'dark');
}


function checkAdmin(){
    if(localStorage.getItem('adminid') == null){
        window.location.href = '/';
    }
}

function checkUser(){
    if(localStorage.getItem('userid') == null){
        window.location.href = '/';
    }
}

search_input = document.getElementById("search_input");



let search_term = document.getElementById("search_term");
search_input.addEventListener("keyup", function(){
    let search_value = search_input.value;
    search_term.innerHTML = "Search result for " + search_value;
    document.getElementById("search_popup").style.display="block";
    if(search_value == ""){
        search_term.innerHTML = "";
        document.getElementById("search_popup").style.display="none";
    }else{
        
        // fetch result from 
        fetch(`/api/search/${search_value}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(function(response){
            return response.json();
        }).then(function(data){
        document.getElementById("search_res").innerHTML = "";
            

            // console.log(data.shows);
            // console.log(data.venues);

            if(data.shows){
                data.shows.forEach(element => {
                    console.log(element);
                    /*
                    description: 
                    image_url: 
                    name:
                    no_of_ratings:
                    rating:
                    showid:
                    tags:
                    */

                    let html = `
                    <a href="/show_detail/${element.showid}">
                        <div class="show_res">
                            <div class="name">${element.name}</div>
                            <div class="desc">${element.description.substring(0,100)}</div>
                            <img class="image" src="${element.image_url}" />
                        </div>
                     </a>
                    `
                    document.getElementById("search_res").innerHTML += html;

                });
            }

            if(data.venues){
                data.venues.forEach(element => {
                    console.log(element);

                    /*
                    name
                    city_town
                    coordinates
                    location_desc
                    no_of_rating
                    rating
                    venueid
                    */

                    let html = `
                    <a href="/venue_detail/${element.venueid}">
                        <div class="venue_res">
                        <div class="name">${element.name}</div>
                        <div class="city">${element.city_town}</div>
                        <div class="desc">${element.location_desc.substring(0,100)}</div>
                        </div>
                    </a>`

                    document.getElementById("search_res").innerHTML += html;


                });
            }
        });

    }
    
});