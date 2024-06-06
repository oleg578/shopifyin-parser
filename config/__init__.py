import configparser
import os

USER = ''
PASSWORD = ''
HOST = ''
PORT = 3306
DATABASE = ''

CSV_DIR = '/var/tmp/shopifyin'
LOG_PATH = '/var/log/shopifyin.log'

FTP_SERVER = ''
FTP_USER = ''
FTP_PASSWORD = ''


def init():
    global USER
    global PASSWORD
    global HOST
    global PORT
    global DATABASE
    global CSV_DIR
    global LOG_PATH
    global FTP_SERVER
    global FTP_USER
    global FTP_PASSWORD

    conf_dir = os.getenv('CONF_DIR', '/etc/shopifyin')

    conf = configparser.ConfigParser()
    conf.read(str.join('/', [conf_dir, 'config.ini']))

    USER = conf['db']['USER']
    PASSWORD = conf['db']['PASSWORD']
    HOST = conf['db']['HOST']
    PORT = conf['db']['PORT']
    DATABASE = conf['db']['DATABASE']
    CSV_DIR = conf['etc']['CSV_DIR']
    LOG_PATH = conf['etc']['LOG_PATH']
    FTP_SERVER = conf['ftp']['SERVER']
    FTP_USER = conf['ftp']['USER']
    FTP_PASSWORD = conf['ftp']['PASSWORD']
