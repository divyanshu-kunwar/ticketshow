# APP-Dev-1-Project
Ticket Show is a web platform to book ticket for shows in cinema hall near you. This webapp is a bit of experiment with design and simplicity as a project for Modern App Development-1 course.
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