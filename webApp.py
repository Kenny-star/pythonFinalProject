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

    temp_data = request.json["Temperature"]
    hum_data = request.json["Humidity"]
    time_data = request.json["Timestamp1"]

    val = (temp_data, hum_data, time_data)

    mycursor.execute(query, val)

    conn.commit()
    mycursor.close()

    conn.close()

    return app.response_class(status=201)


if __name__ == '__main__':
    app.run()
