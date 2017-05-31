#!/usr/bin/env python  
# encoding: utf-8  

"""
Created on 5/26/17 1:19 PM
@author: Flowsnow
@file: excel.py
@function: 
"""
from tablespace import Tablespace
from db_lock import DbLock
from archive import Archive
from memory import Memory
from cpu import CPU
from disk_use import DiskUse
from disk_busy import DiskBusy
from alert import Alert
from ogg import OGG
import xlwt
import datetime
import os


class Excel:
    def __init__(self, cfg):
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.tablespace_sheet = Tablespace(self.workbook)
        self.db_lock_sheet = DbLock(self.workbook)
        self.archive_sheet = Archive(self.workbook)
        self.cpu_sheet = CPU(self.workbook)
        self.memory_sheet = Memory(self.workbook)
        self.disk_use_sheet = DiskUse(self.workbook)
        self.disk_busy_sheet = DiskBusy(self.workbook)
        self.alert_sheet = Alert(self.workbook)
        self.ogg_sheet = OGG(self.workbook)
        self.cfg = cfg

    def save(self):
        path = self.cfg.get('basic', 'store_path')
        if not os.path.exists(path):
            os.mkdir(path)
        self.workbook.save('{}/个人税收管理系统每日检查_{}.xls'.format(path, datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
