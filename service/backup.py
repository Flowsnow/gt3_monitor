#!/usr/bin/env python  
# encoding: utf-8  

"""
Created on 5/31/17 12:02 PM
@author: Flowsnow
@file: backup.py 
@function: backup data file
"""
import os
import shutil
import configparser
import datetime


def backup(config):
    data_path = config.get('basic', 'data_path')
    os.chdir('{}/bak'.format(data_path))
    for f in os.listdir('.'):
        os.remove(f)
    os.chdir('{}/file'.format(data_path))
    for f in os.listdir('.'):
        shutil.move(f, '{}/bak'.format(data_path))


def error_backup(config):
    data_path = config.get('basic', 'data_path')
    current_bak_path = '{}/bak_{}'.format(data_path, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    if not os.path.exists(current_bak_path):
        os.mkdir(current_bak_path)
    os.chdir('{}/file'.format(data_path))
    for f in os.listdir('.'):
        shutil.move(f, current_bak_path)


if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read(filenames='../config.ini', encoding='utf-8')
    backup(cfg)
