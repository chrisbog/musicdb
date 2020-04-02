# Music Database

## Description
When I first started with database programming, I created a recording database using Microsoft Access.   This application is starting to get very old especially when Access is not supported on a Mac.    Once I started doing Python programming, I looked at this as an option to convert the Microsoft Access Database over to python.   It also gave me the opportunity to learn a bunch of new libraries and plugins.

## References
This project was based on a few references that I borrowed code and ideas from.   These references are located below:

https://www.blog.pythonlibrary.org/2017/12/12/flask-101-adding-a-database/

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

## Requirements
This application has been written in Python 3.7 and must use Python 3.7.   There are several libraries that aren't compatible with previous versions!

* Flask
* flask-sqlalchemy
* flask-migrate
* wtforms

## Setup
We are using the Flask-Migrate library to help us migrate the database when changes are made.   To start this right now, you can go into the command line and do the following:

```$ flask db upgrade```

Also when changes occur to the database structure, you can create the migration tables:

``` flask db migrate - m "comment"```

This function will create the migration scripts.   Then once the migration scripts are create, you can run:

```$ flask db upgrade```


