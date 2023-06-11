function selected_login_type(login_type) {
  let user = document.getElementById("user_tab");
  let admin = document.getElementById("admin_tab");

  if (login_type == "user") {
    user.setAttribute("class", "selected");
    admin.setAttribute("class", "");
  } else {
    admin.setAttribute("class", "selected");
    user.setAttribute("class", "");
  }
}

function selected_signup_type(login_type) {
  let user = document.getElementById("user_tab_2");
  let admin = document.getElementById("admin_tab_2");

  if (login_type == "user") {
    user.setAttribute("class", "selected");
    admin.setAttribute("class", "");
  } else {
    admin.setAttribute("class", "selected");
    user.setAttribute("class", "");
  }
}

function signup() {

  let name = document.getElementById("name_input").value;
  let email = document.getElementById("email__input").value;
  let password = document.getElementById("password_input").value;

  fetch("/api/user/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      email: email,
      password: password
    }),
  }).then((res) => {
    res.json().then((data) => {
      if(!data["message"]){
        localStorage.removeItem("authentication_type");
        localStorage.removeItem("username");
        localStorage.removeItem("userid");
        localStorage.removeItem("adminname");
        localStorage.removeItem("adminid");
        localStorage.removeItem("token");

        localStorage.setItem("authentication_type" , "user");
        localStorage.setItem("username" , data.username);
        localStorage.setItem("userid" , data.userid);
        localStorage.setItem("token" , data.token);

        // TODO : Sucess message
        console.log(data['username'])
        window.alert("Kindly Note! Your Username is " + data['username'])
        window.location.href = "/dashboard";
      }else{
        window.alert(data["message"]);
      }
    });
  });

}

function signin() {
  let admin = document.getElementById("admin_tab");

  let username = document.getElementById("username_input").value;
  let password = document.getElementById("password_input").value;
  let isAdmin = admin.getAttribute("class");

  let redirecturl = "/dashboard";
  let fetch_url = "/api/user/signin";
  let body = JSON.stringify({
    username: username,
    password: password,
  });

  if (isAdmin == "selected") {
    fetch_url = "/api/admin/signin";
    redirecturl = "/admin/dashboard"; 
    
    body = JSON.stringify({
      adminname: username,
      password: password,
    });
  }
  fetch(fetch_url , {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: body,
    }).then((res) => {
      res.json().then((data) => {
        if(!data["message"]){

          // remove signin data from local storage
          localStorage.removeItem("authentication_type");
          localStorage.removeItem("username");
          localStorage.removeItem("userid");
          localStorage.removeItem("adminname");
          localStorage.removeItem("adminid");
          localStorage.removeItem("token");

          if (isAdmin == "selected") {
            localStorage.setItem("authentication_type" , "admin");
            localStorage.setItem("adminname" , data.adminname);
            localStorage.setItem("adminid" , data.adminid);
          }else{
            localStorage.setItem("authentication_type" , "user");
            localStorage.setItem("username" , data.username);
            localStorage.setItem("userid" , data.userid);
          }
          localStorage.setItem("token" , data.token);

          // TODO : Sucess message
          window.location.href = redirecturl;

        }else{
          window.alert(data["message"]);
        }
      });
  });

}
