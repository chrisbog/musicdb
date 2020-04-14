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

First step is to clone the repository by using the command:

```git clone {gihub repository}```

Create a python3 virtual environment so we can run the new application in and install the requirements:

```buildoutcfg
$ python3 -m venv musicdb-venv
$ source musicdb-venv/bin/activate
(musicdb-venv) $ pip install -r requirements.txt
```

Once the requirements are installed, we have to create the database.   We use the Flask-Migrate application for this.   You can do the following:
```buildoutcfg
(musicdb-venv) $ musicdb chris$ flask db upgrade
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 0cdb2428566d, Initial Database Revision

```

At this point the new database should be installed.   To run the application:

```buildoutcfg
(musicdb-venv) $ python musicdb.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2020-04-14 16:49:28,505-_log            INFO      * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
## Database changes
We are using the Flask-Migrate library to help us migrate the database when changes are made.   To start this right now, you can go into the command line and do the following:

```$ flask db upgrade```

Also when changes occur to the database structure, you can create the migration tables:

``` flask db migrate - m "comment"```

This function will create the migration scripts.   Then once the migration scripts are create, you can run:

```$ flask db upgrade```


