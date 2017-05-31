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


def start():
    config = configparser.ConfigParser()
    config.read(filenames='config.ini', encoding='utf-8')
    excel = Excel(config)
    # handle database
    dh = DatabasesHandler(excel, config)
    dh.run()

    # handle files
    fh = FilesHandler(excel, config)
    fh.run()
    excel.save()
    backup(config)


if __name__ == '__main__':
    start()
