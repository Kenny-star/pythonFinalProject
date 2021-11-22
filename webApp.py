from flask import request, jsonify, abort
import requests
import connection
from flask import Flask


myHeader = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,' 'image/webp,/;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 ' 'Firefox/93.0',
            'Content-Type': 'application/json'}

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

    r = request.get_json()
    temp_data = r["Temperature"]
    hum_data = r["Humidity"]
    time_data = r["Timestamp1"]

    val = (temp_data, hum_data, time_data)

    mycursor.execute(query, val)

    conn.commit()
    mycursor.close()

    conn.close()

    return app.response_class(status=201)


if __name__ == '__main__':
    app.run()
