import flask
from flask import request, jsonify, abort
import requests
import connection
from flask import Flask


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    conn = connection.connect()
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
    return jsonify(json_array_data)


@app.route('/addLogTemp', methods=['POST'])
def add_Log_Temp():
    conn = connection.connect()
    mycursor = conn.cursor()
    query = "INSERT INTO final (Temperature, Humidity, Timestamp1) VALUES (%s, %s, %s);"
    query2 = "INSERT INTO piunit (pi_valuecelsius, pi_valuefahrenheit) VALUES (%s);"
    query3 = "INSERT INTO pival (value_temp, value_hum, timestamp_) VALUES (%s, %s, %s);"
    query4 = "INSERT INTO summary (pi_value) VALUES (%s);"

    temp_data = request.json["Temperature"]
    fah_data = request.json["Fahrenheit"]
    hum_data = request.json["Humidity"]
    time_data = request.json["Timestamp1"]

    val = (temp_data, hum_data, time_data)
    val2 = (temp_data, fah_data)
    val3 = (temp_data, hum_data, time_data)
    val4 = temp_data

    mycursor.execute(query, val)
    mycursor.execute(query2, val2)
    mycursor.execute(query3, val3)
    mycursor.execute(query4, val4)

    conn.commit()
    mycursor.close()

    conn.close()

    return app.response_class(status=201)


if __name__ == '__main__':
    app.run()
