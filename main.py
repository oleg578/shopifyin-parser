import ftplib
import logging
import os
import sys
import collection
import config
import metafield
import product

if __name__ != '__main__':
    sys.exit(os.EX_USAGE)


def get_files_from_ftp(ftp_server, user_name, user_pass, user_path, dest_dir):
    try:
        ftp = ftplib.FTP(ftp_server)
    except ftplib.all_errors as error:
        return error
    else:
        try:
            ftp.login(user_name, user_pass)
        except ftplib.all_errors as error:
            return error
        try:
            ftp.cwd(user_path)
        except ftplib.all_errors as error:
            return error
        try:
            file_list = ftp.nlst()
        except ftplib.all_errors as error:
            return error
        else:
            for file_name in file_list:
                local_file_path = f"{dest_dir}/{file_name}"
                with open(local_file_path, "wb") as local_file:
                    ftp.retrbinary("RETR " + file_name, local_file.write)
    ftp.quit()


def delete_file_from_ftp(ftp_server, user_name, user_pass, user_path, file_name):
    try:
        ftp = ftplib.FTP(ftp_server)
    except ftplib.all_errors as error:
        return error
    else:
        try:
            ftp.login(user_name, user_pass)
        except ftplib.all_errors as error:
            return error
        try:
            ftp.cwd(user_path)
        except ftplib.all_errors as error:
            return error
        try:
            ftp.delete(file_name)
        except ftplib.all_errors as error:
            return error
    ftp.quit()


def detect_file_type(file_path):
    fn = os.path.basename(file_path).lower()
    if fn.startswith('collections'):
        return 'collection'
    elif fn.startswith('metafields'):
        return 'metafields'
    elif fn.startswith('products'):
        return 'products'
    else:
        return 'unknown'


def main():
    config.init()
    logging.basicConfig(filename=config.LOG_PATH)
    logger = logging.getLogger('main')
    err = get_files_from_ftp(
        config.FTP_SERVER,
        config.FTP_USER,
        config.FTP_PASSWORD,
        "/",
        config.CSV_DIR)
    if err:
        logging.error(err)

    csv_files = [file for file in os.listdir(config.CSV_DIR) if file.endswith('.csv')]
    for inf in csv_files:
        f_type = detect_file_type(inf)
        if f_type == 'collection':
            err = collection.handle(os.path.join(config.CSV_DIR, inf))
            if err:
                logger.error(err)
            else:
                logger.info(f'{inf} is processed')
                err = delete_file_from_ftp(config.FTP_SERVER,
                                           config.FTP_USER,
                                           config.FTP_PASSWORD,
                                           "/", inf)
                if err:
                    logger.error(err)
        elif f_type == 'metafields':
            err = metafield.handle(os.path.join(config.CSV_DIR, inf))
            if err:
                logger.error(err)
            else:
                err = delete_file_from_ftp(config.FTP_SERVER,
                                           config.FTP_USER,
                                           config.FTP_PASSWORD,
                                           "/", inf)
                if err:
                    logger.error(err)
        elif f_type == 'products':
            err = product.handle(os.path.join(config.CSV_DIR, inf))
            if err:
                logger.error(err)
            else:
                err = delete_file_from_ftp(config.FTP_SERVER,
                                           config.FTP_USER,
                                           config.FTP_PASSWORD,
                                           "/", inf)
                if err:
                    logger.error(err)
        else:
            print(f'{inf} is unknown')


if __name__ == '__main__':
    main()
