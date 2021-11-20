import configparser
import MySQLdb, mysql, mysql.connector

config = configparser.ConfigParser()
config.read('my.conf')

def connect():
    return mysql.connector.connect(host = config['Client']['host'],
                           user = config['Client']['user'],
                           password = config['Client']['password'],
                           database = config['Client']['database'])

