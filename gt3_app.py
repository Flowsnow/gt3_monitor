#!/usr/bin/env python  
# encoding: utf-8  

"""
Created on 5/25/17 10:32 AM
@author: Flowsnow
@file: gt3_app.py
@function: application entry
"""
from service.handle import FilesHandler, DatabasesHandler
from component.excel import Excel
import configparser
from service.backup import backup
import logging
import datetime


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s',
                    filename='gt3_app.log', filemode='a')


def start():
    try:
        logging.info('========================================================')
        logging.info('TIMESTAMP: {}'.format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        config = configparser.ConfigParser()
        config.read(filenames='config.ini', encoding='utf-8')
        excel = Excel(config)

        # handle database
        logging.info('starting to handle database items')
        dh = DatabasesHandler(excel, config)
        dh.run()
        logging.info('handle database items finished')

        # handle files
        logging.info('starting to handle all ip.log file')
        fh = FilesHandler(excel, config)
        fh.run()
        logging.info('handle all ip.log finished')

        logging.info('starting to save excel')
        excel.save()
        logging.info('save excel finished')

        backup(config)
    except Exception as e:
        logging.exception(e)
        raise e


if __name__ == '__main__':
    start()
