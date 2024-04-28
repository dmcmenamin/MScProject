# MSc Project - DynaPoint

![img.png](img.png)

This repository contains the code for DynaPoint - which is the MSc project of Darren McMenamin.
A Student at Queen's University Belfast. 

It was submitted in partial fulfilment of the requirements for the degree of 
Masters of Science in Software Development.


## Problem Statement
 > Design a system that not only simplifies the process of creating PowerPoint presentations based on limited or 
 > extensive user inputs but also harnesses the power of the ChatGPT API. Whether users provide minimal data or an 
 > abundance, your system, designed using Python, will interactively gather requirements through a chatbot or form. 
 > Leveraging ChatGPT, it will then intelligently fill in gaps, generating both structure and content to produce 
 > polished and engaging presentations
 > 

## Steps to run the application
 - [ ] Clone the repository
 - [ ] Install the required dependencies
 - [ ] Update the configuration file
 - [ ] Setting up the database
 - [ ] Running the application
 - [ ] Making a user an admin


## Clone the repository
Clone the repository to your local machine using the following command:
``` git clone http://github.com/darrenmcmenamin/MScProject.git```

## Installation
To install the required dependencies, run the following command:
``` pip install -r requirements.txt```

## Update the configuration file
Update the configuration file with the required values. 
The configuration file is located at ```configs\config.py```
Ensure that the following values are set:

1. ```MAIL_SERVER``` - The mail server to use for sending emails.
2. ```MAIL_PORT``` - The port to use for sending emails.
3. ```MAIL_USE_TLS``` - Whether to use TLS for sending emails.
4. ```MAIL_USE_SSL``` - Whether to use SSL for sending emails.
5. ```MAIL_USERNAME``` - The username for the email server.
6. ```MAIL_PASSWORD``` - The password for the email server.
7. ```MAIL_DEFAULT_SENDER``` - The default sender for emails.

## Setting up the database
- The application makes use of MariaDB as the database.
- Please download XAMPP from [here](https://www.apachefriends.org/index.html) and install it.
- Install version 3.3.0
- Once installed, start the Apache and MySQL services.
- Go to the phpMyAdmin page by visiting [http://localhost/phpmyadmin](http://localhost/phpmyadmin)
- Create a new database called ```dynamicpowerpoint```
- From the support folder, import the ```dynamicpowerpoint.sql``` file into the database.
- This will create the required tables for the application.
- Update the ```sqlalchemy_database_uri``` in the configuration file with the correct values.

## Running the application
To run the application, run the following command:
```flask run```

The application will be available at [http://localhost:5000](http://localhost:5000)

## Admin User
- Once the application is running, go to the Sign-Up page and create a new user.
- Once the user is created, 
  - Go to the phpMyAdmin page and update the ```user_is_admin``` column in the ```user_information``` table to 1.