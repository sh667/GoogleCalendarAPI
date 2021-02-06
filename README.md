# Final Project - Calendar App with user account 

[![Build Status](https://travis-ci.com/nt27web/Calendar-with-login_finalproject.svg?branch=main)](https://travis-ci.com/github/nt27web/Calendar-with-login_finalproject)

## Summary:
* This web application lets registered users to manage their appointments on a calendar.
* The application requires users to register first, providing email id and basic user details alongwith a password.
* Users can then login using the email id and password to go the calendar entries (appointments, meetings, reminders etc.)
* Users can edit/update their details(except email id) as and when they want.
* Upon registration(sign up) users need to confirm their email addresses by providing the OTP sent to their email address supplied during the registration.
    Unless the email id is confirmed, users cannot login to the system.
  
## Installation instructions
### Prerequisites:
* Please make sure port 5000 and 3200 are free in the system it will be installed.
* Please make sure docker is installed and running.

### Steps:
* Download the source code - 
```
git clone https://github.com/nt27web/Calendar-with-login_finalproject.git
  ```
* Go to the coned folder -
```
cd Calendar-with-login_finalproject
  ```
* Build and start the application - 
```
docker-compose up
  ```
* Application should start running with two components -
```
MySql_Database
Flask_App
  ```
* Now open a browser and go to the below url - 
```
http://localhost:5000/
  ```

## Developers:
* Nayana Kumari Thakur - Login, Sign Up, Edit user details, Email confirmation, Email validation ( End to End)
* Sourav - Calendar Entry list, Entry create, edit, delete, display ( End to End)


