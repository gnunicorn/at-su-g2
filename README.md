
# README

## Setup

Run this to create the initial setup:

 virtualenv .
 source bin/activate
 (v)$ pip install -r requirements
 (v)$ alembic upgrade head

Please make sure to run all commands prefixed "(v)$" from within the virtual environment .

## Dev-Server

The following will start the dev app server on port 5000:

 (v)$ python app.py


## Updating

Please run the following after each pull from within your virtualenv

  (v)$ pip install -r requirements.txt
  (v)$ alembic upgrade head

## Cheat Sheet:

 - to make alembic generate a new revision from the model(s) you created run `alembic revision --auto`
 

## Understanding the infrastructure

We are using:
 * Flask for Web Handling: http://flask.pocoo.org/
 * SQLAlchemy for Database Access: http://docs.sqlalchemy.org/en/rel_0_8/
 * Alembic for Database migrations: https://alembic.readthedocs.org/en/latest/index.html
 * Twitter Bootstrap as UI-Framework: http://getbootstrap.com/
 * with jQuery for Interaction: http://api.jquery.com/