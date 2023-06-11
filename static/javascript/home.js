window.addEventListener("load", function () {

  let current_position = 1;
  let direction = 1;
  setInterval(() => {
    // increase the position and then do reverse
    current_position += direction;
    if (current_position == 3) {
      direction = -1;
    } else if (current_position == 1) {
      direction = 1;
    }

    change_feedback(current_position);
  }, 7000);

  // check if there is data in local storage
  let data = localStorage.getItem("data")
  if(data){
    // if data is present then redirect to dashboard
    // window.location.href = "/dashboard"
  }

});

function change_feedback(position) {
    let element1 = document.querySelector(".feedbacks[data-position='1']");
    let element2 = document.querySelector(".feedbacks[data-position='2']");
    let element3 = document.querySelector(".feedbacks[data-position='3']");

    let element1_control = document.querySelector(
      "#feedback_slide_control div:nth-child(1)"
    );
    let element2_control = document.querySelector(
      "#feedback_slide_control div:nth-child(2)"
    );
    let element3_control = document.querySelector(
      "#feedback_slide_control div:nth-child(3)"
    );

    if (position == 1) {
      element1.style.left = "0%";
      element1.style.position = "relative";
      element1.style.opacity = "1";
      element1_control.setAttribute("data-active", "true");

      element2.style.left = "110%";
      element2.style.position = "absolute";
      element2.style.opacity = "0";
      element2_control.setAttribute("data-active", "false");

      element3.style.left = "220%";
      element3.style.position = "absolute";
      element3.style.opacity = "0";
      element3_control.setAttribute("data-active", "false");
    } else if (position == 2) {
      element1.style.left = "-110%";
      element1.style.position = "absolute";
      element1.style.opacity = "0";
      element1_control.setAttribute("data-active", "false");

      element2.style.left = "0%";
      element2.style.position = "relative";
      element2.style.opacity = "1";
      element2_control.setAttribute("data-active", "true");

      element3.style.left = "110%";
      element3.style.position = "absolute";
      element3.style.opacity = "0";
      element3_control.setAttribute("data-active", "false");
    } else {
      element1.style.left = "-220%";
      element1.style.position = "absolute";
      element1.style.opacity = "0";
      element1_control.setAttribute("data-active", "false");

      element2.style.left = "-110%";
      element2.style.position = "absolute";
      element2.style.opacity = "0";
      element2_control.setAttribute("data-active", "false");

      element3.style.left = "0%";
      element3.style.position = "relative";
      element3.style.opacity = "1";
      element3_control.setAttribute("data-active", "true");
    }
}