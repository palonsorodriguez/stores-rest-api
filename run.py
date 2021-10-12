from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all() # before first request runs it will run this and create data.db and create all the tables unless they exist already
