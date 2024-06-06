import csv
import logging
import re
import mariadb
import sup
import os


def handle(path):
    logger = logging.getLogger(__name__)
    item = dict()
    with open(path, encoding='utf-8-sig') as csvfile:
        has_header = sup.has_header(path)
        if not has_header:
            return print(f'{path} has no header')
        reader = csv.reader(csvfile, dialect='unix')
        header = []
        site = sup.get_site(path)
        date = sup.get_date(path)
        # clear table before fill
        clear_table(site)
        for row in reader:
            if reader.line_num == 1:
                h = map(lambda x: re.sub(r'[^a-z0-9]+', '_', x.lower()), row)
                header.extend(h)
                continue
            for idx, column in enumerate(header):
                item[column] = row[idx]
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


def item_save(item, site, date):
    insert_query = '''
    INSERT INTO `collections`
    (`id`, `site`, `handle`, `title`, 
    `image_width`, `image_height`, `image_alt_text`, `top_row`, 
    `product_id`, `product_handle`, `product_position`, `products_count`, 
    date_added) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    conn = sup.get_db_conn()
    cur = conn.cursor()
    try:
        cur.execute(insert_query, (item['id'], site, item['handle'], item['title'],
                                   int(item['image_width'] or 0), int(item['image_height'] or 0),
                                   item['image_alt_text'], bool(item['top_row'] or False),
                                   item['product_id'], item['product_handle'],
                                   int(item['product_position'] or 0),
                                   int(item['products_count'] or 0),
                                   date))
    except mariadb.Error as e:
        return f'{e}'
    except ValueError as ve:
        return f'{item}:\n{ve}'
    conn.commit()
    cur.close()
    conn.close()


def clear_table(site):
    del_query = '''
    DELETE FROM `collections` WHERE site=?
    '''
    conn = sup.get_db_conn()
    cur = conn.cursor()
    cur.execute(del_query, (site,))
    conn.commit()
    cur.close()
    conn.close()
