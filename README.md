# APP-Dev-1-Project
Ticket Show is a web platform to book ticket (similar to BookMyShow) for booking shows in cinema nearest you. This webapp is a bit of experiment with design and simplicity as a project for Modern App Development-1 course.
## See Live at [https://ts.div.nerlex.com](https://ts.div.nerlex.com)
![image](https://github.com/KUNWAR-DIVYANSHU/ticketshow/assets/68821907/4e08ff7a-7560-4b19-b5d7-a3e8deb8bddc)

Video Demo at YouTube - [@kunwar_divyanshu](https://youtu.be/_XLosw7jAI0)
## create a virtual environment
    
    ```bash
    python3 -m venv venv
    ```

## activate the virtual environment

    ```bash
    source venv/bin/activate
    ```

## install the required packages

    ```bash
    pip install -r requirements.txt
    ```

    or on window simply run the bat file `install.bat`

## run the app

    ```bash
    python app.py
    ```

    or on window simply run the bat file `run.bat`

## Authentication 
+ For user 
    `username : user2893
    password : 1234abc@`

or create your own by sign up

+ For admin
    `adminname : admin1474
    password : 1234abc@`
    `adminname : admin4681
    password : 1234abc@`
    `adminname : admin6955
    password : 1234abc@`

or create your own by using API POST request at /admin/signup
body must contain 

```json
{
    "name":"admin",
    "email":"admin@gmail.com",
    "password":"1234abc@"
}
```


## Directory
+ API - API endpoints
  + Common - common utilities for API
  + Controller - Model and Controller classes
  + Resources - API classes
+ Data
+ static
+ templates - HTML templates
+ app.py
