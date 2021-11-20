import flask, RPi.GPIO as GPIO, time, datetime, csv, adafruit_dht, board, requests

list = []
myHeader = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,' 'image/webp,/;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 ' 'Firefox/93.0'}

dht = adafruit_dht.DHT11(board.D4, use_pulseio=False)

def postToApi(json_obj):
    response = requests.post("'/addLogTemp'", headers=myHeader, data=json_obj)
    while response.status_code != 200:
        response


while True:
    try:

        temperature = dht.temperature
        humidity = dht.humidity
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("Temperature: %-3.1f C" % temperature)
        print("Humidity: %-3.1f %%" % humidity)

        print("Last valid input: " + timestamp + "\n")

        current_info = {'Temperature': temperature,
                        'Humidity': humidity,
                        'Timestamp': timestamp}

        postToApi(current_info)
        list.append(current_info)

        print(list)
        print()

        with open('tempLog.csv', mode='a') as csv_file:
            fieldnames = ['Temperature', 'Humidity', 'Timestamp']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writerow({'Temperature': temperature, 'Humidity': humidity, 'Timestamp': timestamp})

        time.sleep(10)


    except RuntimeError as error:
        print("A Runtime Error has been encountered: " + error.args[
            0] + "\nThe temperature & humidity reading will re-evaluated after 10 seconds.\n")
        time.sleep(10)
        continue

    except Exception as error:
        dht.exit()
        raise error




