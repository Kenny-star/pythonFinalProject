
import flask, RPi.GPIO as GPIO, time, datetime, csv, adafruit_dht, board, requests
import logging

import logging

list = []
myHeader = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,' 'image/webp,/;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 ' 'Firefox/93.0'}

dht = adafruit_dht.DHT11(board.D4, use_pulseio=False)

while True:
    try:

        logging.basicConfig(filename='temp.log', filemode='w', format='%(levelname)s %(asctime)s - %(message)s',
                            level=logging.DEBUG)
        logger = logging.getLogger()


        temperature = dht.temperature
        humidity = dht.humidity
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fahrenheit = (temperature * 9 / 5) + 32
        print("Temperature: %-3.1f C" % temperature)
        print("Fahrenheit: %-3.1f F" % fahrenheit)
        print("Humidity: %-3.1f %%" % humidity)

        print("Last valid input: " + timestamp + "\n")

        current_info = {"Temperature": temperature,
                        "Fahrenheit": fahrenheit,
                        "Humidity": humidity,
                        "Timestamp1": timestamp}

        url = "https://webapprouting.herokuapp.com"
        timeout = 5

        try:
            req = requests.get(url, timeout=timeout)
            print("Connected to the Internet")

        except (requests.ConnectionError, requests.Timeout) as exception:
            print("No Internet connection.")

        response = requests.post("https://webapprouting.herokuapp.com/addLogTemp", headers=myHeader, json=current_info)

        print(response)
        list.append(current_info)

        print(list)
        print()

        with open('tempLog.csv', mode='a') as csv_file:
            fieldnames = ['Temperature', 'Fahrenheit', 'Humidity', 'Timestamp1']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writerow({'Temperature': temperature, 'Fahrenheit': fahrenheit,
                             'Humidity': humidity, 'Timestamp1': timestamp})


        logger.info("Successfully stored data")


        time.sleep(10)


    except RuntimeError as error:
        print("A Runtime Error has been encountered: " + error.args[
            0] + "\nThe temperature & humidity reading will re-evaluated after 10 seconds.\n")

        logger.error("A runtime error as occured. The sensor will try again in 10 seconds")


        time.sleep(10)
        continue

    except Exception as error:

        logger.critical("A fatal errror as occured. The sensor will be stopped.")

        dht.exit()
        raise error












