import csv
import datetime
import locale
import os
import socket

from flask import Flask, request, jsonify
from flask.wrappers import Response
from flask_mongoengine import MongoEngine, sessions


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': os.environ['MONGODB_HOST'],
    'username': os.environ['MONGODB_USERNAME'],
    'password': os.environ['MONGODB_PASSWORD'],
    'db': 'webapp'
}
db = MongoEngine()

db.init_app(app)


class Members(db.Document):
    email = db.StringField(required=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=80)
    sex = db.BooleanField(default=True)    # False -> Male; True -> Female
    is_star = db.BooleanField(default=False)
    telephone = db.StringField()
    birthdate = db.DateTimeField()
    address = db.StringField()
    # picture = db.ImageField(collection_name="images")


class Departments(db.Document):
    name = db.StringField(required=True)
    responsible = db.ReferenceField(Members)


class Services(db.Document):
    member = db.ReferenceField(Members)
    department = db.ReferenceField(Departments)


class Tickets(db.Document):
    name = db.StringField(required=True)


class Events(db.Document):
    name = db.StringField(required=True)
    available_tickets = db.ListField()


class Sessions(db.Document):
    event = db.ReferenceField(Events)
    session_start = db.DateTimeField()
    session_end = db.DateTimeField()


class Participations(db.Document):
    participant = db.ReferenceField(Members)
    session = db.ReferenceField(Sessions)
    ticket = db.ReferenceField(Tickets)
    last_update = db.DateTimeField()
    is_present = db.BooleanField(default=False)
    presence_date = db.DateTimeField()


class Leaders(db.Document):
    pass


@app.route('/')
def index():
    add_member_in_database(
        email="rggouale@gmail.com",
        first_name="regi",
        last_name="gouale",
        sex=False, is_star=True
    )
    member = Members.objects().to_json()
    return Response(member, mimetype="application/json", status=200)


@app.route('/members', methods=["GET"])
def get_all_members():
    data = {}
    i = 0
    for member in Members.objects:
        print(member.first_name, member.last_name)
        data[f"{i}"] = member.to_json()
        i += 1

    return Response(data, mimetype="application/json", status=200)


@app.route('/delete_members')
def delete_all_members():
    number_of_deletions = Members.objects().delete()
    return jsonify(number_of_deletions)


def add_member_in_database(email: str, first_name: str, last_name: str, sex: bool = True, is_star: bool = False, telephone: str = '', birthdate: datetime = None, address: str = ''):
    count_persons = Members.objects(
        email=email, first_name=first_name, last_name=last_name).count()
    print(count_persons)
    if count_persons == 0:
        Members(email=email, first_name=first_name, last_name=last_name, sex=sex,
                is_star=is_star, telephone=telephone, birthdate=birthdate, address=address).save()
    return jsonify(f"Membre inscrit avec succès !")


def import_members_from_csv(filename: str):
    # check if the file exists
    if not os.path.isfile(filename):
        return FileNotFoundError(
            f"{filename} does not exist !"
        )
    members = {}

    # read file
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        


def create_department(name: str, responsible_fisrtname: str, responsible_lastname: str):
    pass


def add_star_in_department(firstname: str, last_name: str, department: str):
    pass

def registration_on_event_waiting_list(email, first_name, last_name, ticket):
    # check that user can register
    # register member in waiting list
    # sent notification to registered member
    # return OK
    pass

def establishment_member_confirmation_worship_list(registrered_list, waiting_list, number_of_available_seats, rotate):
    # remove already registrered members from list
    # split waiting list in two (confirmed and waiting)
    # register confirmed list
    # notify confirmed
    # notify waitings
    pass

def confirm_worship_participation(email, ticket):
    # check that email is in confirmed list
    # register member in the event list
    # sent email to user
    pass

def star_registration(email, first_name, last_name, department):
    # check that the department can register star in the event
    # check that number of stars is not raised
    # register the star
    # Notify star and department responsible
    pass

def cancel_event_participation(email, first_name, last_name, ticket):
    # check that user is in worship list
    # cancel the user
    # notify the user
    # insert in the confirmed list the first person in waiting list
    # notify the inserted user
    pass

def leaders_registration(email, first_name, last_name):
    # check that leader is not already registered
    # register the leader in worship list
    # notify the leader
    pass

def special_ask_from_leaders(leader_first_name, leader_last_name, email, first_name, last_name):
    # check that user is not already in worship list
    # check that the number leader special ask in not reached
    # register the User
    # notify the user
    # notify the leader
    pass

def child_registration(parent, child):
    pass

def validate_presence(member):
    pass

def notify_absence(list_of_absents):
    pass

def email_notification():
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
