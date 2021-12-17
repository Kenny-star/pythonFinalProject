import flask
from flask import request, jsonify, abort
import requests
import connection
from flask import Flask
import mysql.connector
import logging


app = Flask(__name__)
logging.basicConfig(filename='temp.log', filemode='a', format='webApp.py-%(levelname)-%(message)')

@app.route('/', methods=['GET'])
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
