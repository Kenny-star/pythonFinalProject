from flask import Flask
from flask import request, jsonify, abort, make_response
import requests
import connection
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import datetime
import jwt
import os
from functools import wraps
import mysql.connector
import logging



app = Flask(__name__)
logging.basicConfig(filename='temp.log', filemode='a', format='webApp.py-%(levelname)-%(message)')

app.config.get('SECRET_KEY')
users = {}
items = {}

class User:
      def __init__(self, public_id, name, password, admin):
        self.public_id = public_id
        self.name = name
        self.password = password
        self.admin = admin

        id = 0
        public_id = 0
        name = ''
        password = ''
        admin = False


class Item:
    id = 0


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Acess Denied, Token Missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = None

            for u in users.values():
                if u.public_id == data['public_id']:
                    current_user = u

        except Exception as ex:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorator


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    users[new_user.name] = new_user

    return jsonify({'message': 'User created successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Auth info not provided', 401, {'WWW-Authenticate': 'Login required!"'})

    user = users.get(auth.username)

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config.get('SECRET_KEY'), algorithm='HS256')
        return jsonify({'token': token})

    return make_response('Auth info incorrect', 401, {'WWW-Authenticate': 'Login required!"'})


@app.route('/', methods=['GET'])
@token_required
def home():
    try:
        conn = connection.connect()
        logging.info("Connected to database successfully")

    except mysql.connector.Error as e:
        logging.critical("Cannot connect to the database")


    mycursor = conn.cursor()
    query = "SELECT * FROM final"
    mycursor.execute(query)

    result = mycursor.fetchall()
    row_headers = [x[0] for x in mycursor.description]

    json_array_data = []
    for r in result:
        json_array_data.append(dict(zip(row_headers, r)))

    mycursor.close()
    conn.close()
    logging.info("Successfully Displayed the data on the web service")
    return jsonify(json_array_data)

    if len(result) ==0:
        logging.error("There are no readings in the database")
        abort(404)

    if not request.json:
        logging.error("JSON body was not provided")
        abort(400)


@app.route('/addLogTemp', methods=['POST'])
@token_required
def add_Log_Temp():
    try:
        conn = connection.connect()
        logging.info("Connected to database successfully")

    except mysql.connector.Error as e:
        logging.critical("Cannot connect to the database")


    mycursor = conn.cursor()
    query = "INSERT INTO final (Temperature, Humidity, Timestamp1) VALUES (%s, %s, %s);"
    query2 = "INSERT INTO piunit (pi_valuecelsius, pi_valuefahrenheit) VALUES (%s, %s);"
    query3 = "INSERT INTO pival (value_temp, value_hum, timestamp_) VALUES (%s, %s, %s);"
    query4 = "INSERT INTO summary (pi_value, valueid, unitid) VALUES (%s, %s, %s);"

    temp_data = request.json["Temperature"]
    fah_data = request.json["Fahrenheit"]
    hum_data = request.json["Humidity"]
    time_data = request.json["Timestamp1"]

    val = (temp_data, hum_data, time_data)
    val2 = (temp_data, fah_data)
    val3 = (temp_data, hum_data, time_data)

    mycursor.execute(query, val)
    mycursor.execute(query2, val2)
    conn.commit()
    value_id = mycursor.lastrowid
    mycursor.execute(query3, val3)
    conn.commit()
    unit_id = mycursor.lastrowid

    val4 = (temp_data, value_id, unit_id)
    mycursor.execute(query4, val4)
    conn.commit()

    mycursor.close()

    conn.close()
    logging.info("Successfully posted readings")

    return app.response_class(status=201)

    if not request.json:
        logging.error("JSON body was not provided")
        abort(400)


if __name__ == '__main__':
    app.run()
