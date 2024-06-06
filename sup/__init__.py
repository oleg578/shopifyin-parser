import csv
import os
import mariadb
import config


def get_dialect(path):
    with open(path, encoding='utf-8-sig') as file:
        dialect = csv.Sniffer().sniff(file.read(2048))
        return dialect


def has_header(path):
    with open(path, encoding='utf-8-sig') as file:
        return csv.Sniffer().has_header(file.read(2048))


def get_site(fname):
    base_name = os.path.basename(fname)
    return base_name.split('_')[1]


def get_date(fname):
    base_name = os.path.basename(fname).split('.')[0]
    bn_split = base_name.split('_')
    return bn_split[len(bn_split) - 1]


def get_db_conn():
    conn = mariadb.connect(
        user=config.USER,
        password=config.PASSWORD,
        host=config.HOST,
        port=int(config.PORT),
        database=config.DATABASE
    )
    return conn
