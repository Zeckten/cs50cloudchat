# cs50cloudchat
#### Video Demo:  <URL HERE>
#### Description:
A portion of this code is taken from or inspired by the tutorials on flask.palletsprojects.com and CS50's Finance.

My project, cs50cloudchat, is an online chatroom hosted at https://cs50cloudchat.herokuapp.com/. To run it locally the SECRET_KEY must be set. It is invite-only to prevent it from being used for unwanted purposes, but anyone with an admin account can create these invites. I have provided an admin account for grading purposes with the username "CS50" and the password "Admin50".

- chat: This folder contains the python package that is cs50cloudchat.
  - static: This folder contains my css files
    - bootstrap.css: This is the Bootswatch Darkly theme for Bootstrap.
    - styles.css: This is my own css.
  - templates: This folder contains the html files for cs50cloudchat.
    - base.html: This file is a base template inspired by the Flask tutorial. It fetches the css files and Bootstrap Javascript and creates a universal navbar  and flashing system.
    - index.html: This file is the homepage of cs50cloudchat. It has a table with all the posts and a form to post to the chat at the bottom.
    - login.html: This file is the login page of cs50cloudchat. It is inspired by the Flask tutorial and my implementation of CS50's Finance.
    - register.html: This file is the register page of cs50cloudchat. It facilitates the creation of users with a valid invite. It is inspired by the flask tutorial and my implementation of CS50's Finance.
    - settings.html: This file is the settings page of cs50cloudchat. It allows users to change their password.
  - __init__.py: This file defines a function that creates the Flask app and tells python to treat the chat folder as a package. It is inspired by the Flask tutorial.
  - app.py: This file runs the homepage and the route to the settings page.
  - auth.py: This file defines the register, login, logout, load_logged_in_user, invite, and change_password routes along with the login_required and admin_required functions. Some of these functions are inspired by the Flask tutorial.
  - db.py: This file defines the get_db, close_db, init_app, and create_invite functions along with the init-db and create-invite commands. Some of these functions are inspired by the Flask tutorial.
  - cloudchat.db: This is the database file that holds all the users, invites, and posts for cs50cloudchat.
  - schema.sql: This file contains the commands to initialize the database with user, invite, and post tables.
- .gitignore: This tells git to ignore my local environment files.
- Procfile: This outlines the commands that Heroku should run on the server. The only command it uses is waitress-serve to initialize the server. I chose to use waitress because it works on Windows and Linux.
- requirements.txt: This file lists all the python packages that need to be installed to run cs50cloudchat.
