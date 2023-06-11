console.log("dashboard.js loaded");
function closeSidebar() {
    filter_icon.src = '/static/media/filter.svg'
    style.width = '30px'
    filter.style.top = '1.5%'
    filter.style.right = '10%'
}
function openSidebar() {
    filter_icon.src = src;
    style.width = '60px'
    filter.style.top = '.3%'
    filter.style.right = '8%'
}


let sidebar_open = false;
let src = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4NCjxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNMTYuMzUzNSAxNS42NDY1TDIxIDExTDIxLjcwNzEgMTEuNzA3MUwxNy4wNjA2IDE2LjM1MzZMMjEuNzA3MSAyMUwyMSAyMS43MDcxTDE2LjM1MzUgMTcuMDYwN0wxMS43MDcxIDIxLjcwNzFMMTEgMjFMMTUuNjQ2NCAxNi4zNTM2TDExIDExLjcwNzJMMTEuNzA3MSAxMS4wMDAxTDE2LjM1MzUgMTUuNjQ2NVoiIGZpbGw9ImJsYWNrIiBmaWxsLW9wYWNpdHk9IjAuOCIvPg0KPC9zdmc+DQo="
let filter = document.querySelector(".filter");
let filter_icon = document.querySelector(".filtor_icon");
let sidebar = document.getElementById("sidebar");
let apply_btn = document.querySelector(".bordered_btn")
let style = filter_icon.style;



filter_icon.addEventListener("click", function () {
    sidebar.classList.toggle('show')
    sidebar_open = !sidebar_open;

    if (sidebar_open) openSidebar()
    else closeSidebar()
});

apply_btn.addEventListener("click", () => {
    console.log("Apply button clicked");
    sidebar.classList.toggle('show')
    sidebar_open = !sidebar_open;

    closeSidebar()
    submitFilter()
})

function switch_tab(tabno){
    if(tabno === 0){
        show_cards = document.getElementsByClassName("show_cards")
        for (let i = 0; i < show_cards.length; i++) {
            show_cards[i].style.display = "block";
        }
        venue_cards = document.getElementsByClassName("venue_cards")
        for (let i = 0; i < venue_cards.length; i++) {
            venue_cards[i].style.display = "none";
        }
        document.getElementById("sidebar").style.display = "flex";

    }else{
        show_cards = document.getElementsByClassName("show_cards")
        for (let i = 0; i < show_cards.length; i++) {
            show_cards[i].style.display = "none";
        }
        venue_cards = document.getElementsByClassName("venue_cards")
        for (let i = 0; i < venue_cards.length; i++) {
            venue_cards[i].style.display = "block";
        }  
        document.getElementById("sidebar").style.display = "none";

    }
    document.getElementById("showtab").classList.toggle("selected")
    document.getElementById("theatretab").classList.toggle("selected")
}

function submitFilter(){
    console.log("Submit button clicked");
    let location = document.getElementById("city").value;
    let rating = document.getElementsByName("rate");
    for (let i = 0; i < rating.length; i++) {
        if (rating[i].checked) {
            rating = rating[i].value;
            break;
        }
    
        if(i == rating.length - 1){
            rating = 0;
        }
    }


    let language = document.getElementsByName("language");
    language_list = []
    for (let i = 0; i < language.length; i++) {
        if (language[i].checked) {
            language_list.push(language[i].value);
        }
    }    


    let tags = document.getElementsByName("tag");
    tags_list = []
    for (let i = 0; i < tags.length; i++) {
        if (tags[i].checked) {
            tags_list.push(tags[i].value);
        }
    }

    let data = {
        "location": location,
        "rating": rating,
        "language": language_list,
        "tags": tags_list
    }
    console.log(data);

    // if rating is not a number
    rating = rating.toString();
    console.log(rating);

    language_list = language_list.toString();
    console.log(language_list);

    tags_list = tags_list.toString();
    console.log(tags_list);


    str = "/dashboard/?location=" 
    + location + "&rating=" + rating + "&language=" + language_list +
     "&tags=" + tags_list;

    console.log(str);

    window.location.href = str;

}