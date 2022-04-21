import random

from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@localhost:5432/store"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#lancement
@app.route("/user", methods = ["POST", "GET"])
def users():
    if request.method == "GET":
        result = User.query.all()
        users = []
        for row in result:
            user = {
                "id" : row.id,
                "firstname" : row.firstname,
                "lastname" : row.lastname,
                "age" : row.age,
                "email" : row.email,
                "job" : row.job
            }
            users.append(user)
        return jsonify(users)

    if request.method == "POST":
        data = request.json
        new_user = User(
            data["firstname"],
            data["lastname"],
            data["age"],
            data["email"],
            data["job"]
        )
        db.session.add(new_user)
        db.session.commit()
        return Response(status=200)

#class User et Application
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    job = db.Column(db.String(100))
    applications = db.relationship('Application')

    def __init__(self, firstname, lastname, age, email, job):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.email = email
        self.job = job

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    lastconnection = db.Column(db.Date)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, appname, username, lastconnnection):
        self.appname = appname
        self.username = username
        self.lastconnection = lastconnnection

#fonction Populate qui va remplir les tables
#1) exemple
def populate_table():
    new_user = User("Sabrine", "Thibert", 23, "sabrine.thibert@esme.fr", "Student")
    db.session.add(new_user)
    db.session.commit()

#2) Populate avec la librairie Faker
from faker import Faker
import random
from datetime import date
fake = Faker()

def populate():
    for n in range(0, 1000):
        #create all fake fields for users
        new_user = User(fake.first_name(), fake.last_name(), random.randint(0, 100), fake.email(), fake.job())
        #create all fake fields for app
        apps = ["Facebook", "Instagram", "Twitter", "Pinterest"]
        nb_app = 4
        applications = []
        for app_n in range(0, nb_app):
            app = Application(apps[app_n], fake.user_name(), date.today())
            applications.append(app)
        new_user.applications = applications
        db.session.add(new_user)
    db.session.commit()

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    populate_table()
    populate()
    app.run(host="0.0.0.0", port=8080, debug=True)