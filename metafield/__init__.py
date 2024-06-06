import csv
import logging
import os
import re
import mariadb
import sup


def handle(path):
    logger = logging.getLogger(__name__)
    item = dict()
    item['metafields'] = dict()
    with open(path, encoding='utf-8-sig') as csvfile:
        if not sup.has_header(path):
            return print(f'{path} has no header')
        reader = csv.reader(csvfile, dialect='unix')
        header = []
        site = sup.get_site(path)
        date = sup.get_date(path)
        # clear table before fill
        clear_table(site)
        for row in reader:
            if reader.line_num == 1:
                header.extend(row)
                continue
            for idx, column in enumerate(header):
                if column.startswith('Metafield'):
                    m_name = get_metafield(column)
                    item['metafields'][m_name] = row[idx]
                else:
                    item[column.lower()] = row[idx]
            err = item_save(item, site, date)
            if err:
                logger.error(err)
    try:
        os.remove(path)
    except FileNotFoundError as error:
        return f'{error}'
    except PermissionError as error:
        return f'{error}'
    except OSError as error:
        return f'{error}'


def get_metafield(v):
    v_spl = v.split(' ')
    return re.sub(r'[^a-z0-9]+', '_', v_spl[1].lower())


def item_save(item, site, date):
    insert_query = '''
    INSERT INTO `metafields` 
    (`id`, `site`, `handle`, `metafield_name`, `metafield_value`, `date_added`)
    VALUES (?, ?, ?, ?, ?, ?)
    ON DUPLICATE KEY UPDATE `metafield_value`=?
    '''
    conn = sup.get_db_conn()
    cur = conn.cursor()
    for name, value in item['metafields'].items():
        try:
            cur.execute(insert_query, (item['id'], site, item['handle'], name, value, date, value))
        except mariadb.Error as e:
            return f'{e}'
        except ValueError as ve:
            return f'{item}:\n{ve}'
    conn.commit()
    cur.close()
    conn.close()


def clear_table(site):
    del_query = '''
    DELETE FROM `metafields` WHERE site=?
    '''
    conn = sup.get_db_conn()
    cur = conn.cursor()
    cur.execute(del_query, (site,))
    conn.commit()
    cur.close()
    conn.close()
