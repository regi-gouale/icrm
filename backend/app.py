import datetime
import locale
import os
import socket

from flask import Flask, request, jsonify
from flask.wrappers import Response
from flask_mongoengine import MongoEngine


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
    is_star = db.BooleanField(default=False)
    picture = db.ImageField()


class Departments(db.Document):
    name = db.StringField(required=True)
    responsible = db.ReferenceField(Members)


@app.route('/')
def index():
    hostname = socket.gethostname()
    regi = Members(email="rggouale@gmail.com", first_name="regi",
                   last_name="gouale", is_star=True)
    print(regi)
    regi.save()
    member = Members.objects().to_json()
    return Response(member, mimetype="application/json", status=200)


@app.route('/members', methods=["GET"])
def get_all_members():
    data = []
    for member in Members.objects:
        data.append((member.first_name, member.last_name))

    return Response(data, mimetype='application/json', status=200)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
