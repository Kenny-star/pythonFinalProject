import logging
import configparser
import mysql.connector
import MySQLdb, mysql, mysql.connector

config = configparser.ConfigParser()
config.read('my.conf')

logging.basicConfig(filename='temp.log', filemode='a', format='connection.py-%(levelname)-%(message)')

def connect():

    try:

        return mysql.connector.connect(host = config['Client']['host'],
                           user = config['Client']['user'],
                           password = config['Client']['password'],
                           database = config['Client']['database'])
        logging.info("Successfully connected to the database.")

    except mysql.connector.Error as e:
        logging.critical("Cannot connect to the database")

