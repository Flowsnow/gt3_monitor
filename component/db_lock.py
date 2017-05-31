#!/usr/bin/env python  
# encoding: utf-8  

"""
Created on 5/25/17 2:43 PM
@author: Flowsnow
@file: db_lock.py 
@function: db_lock sheet
"""
from fit import FitSheetWrapper
import xlwt
import datetime
from style import STYLE_BODY, STYLE_TITLE, STYLE_HEAD


class DbLock:
    """DbLock sheet"""

    def __init__(self, workbook):
        self._workbook = workbook
        self._name = '数据库长时间锁检查'
        self._sheet = FitSheetWrapper(self._workbook.add_sheet(self._name))
        self._row = 0
        self._seq = 1
        self._length = 15
        self._time = datetime.datetime.now()
        self._handle_head()

    def _row_inc(self):
        self._row += 1

    def _seq_inc(self):
        self._seq += 1

    def _handle_head(self):
        self._sheet.write_merge(self._row, self._row, 0, self._length - 1, '金税三期个人税收系统数据库长时间锁检查', style=STYLE_TITLE)
        self._row_inc()
        self._sheet.write(self._row, 0, '填表人')
        self._sheet.write(self._row, 2, '填表日期')
        self._sheet.write_merge(self._row, self._row, 3, self._length - 1, self._time.strftime('%Y-%m-%d %H:%M:%S'))
        self._row_inc()
        # write column name
        self._sheet.write(self._row, 0, '序号', style=STYLE_HEAD)
        self._sheet.write(self._row, 1, 'DBNAME', style=STYLE_HEAD)
        self._sheet.write(self._row, 2, 'TM', style=STYLE_HEAD)
        self._sheet.write(self._row, 3, 'SID', style=STYLE_HEAD)
        self._sheet.write(self._row, 4, 'SQL_ID', style=STYLE_HEAD)
        self._sheet.write(self._row, 5, 'SQL_CHILD_NUMBER', style=STYLE_HEAD)
        self._sheet.write(self._row, 6, 'PREV_SQL_ID', style=STYLE_HEAD)
        self._sheet.write(self._row, 7, 'XID', style=STYLE_HEAD)
        self._sheet.write(self._row, 8, 'START_TIME', style=STYLE_HEAD)
        self._sheet.write(self._row, 9, 'TYPE', style=STYLE_HEAD)
        self._sheet.write(self._row, 10, 'BLOCK', style=STYLE_HEAD)
        self._sheet.write(self._row, 11, 'CTIME', style=STYLE_HEAD)
        self._sheet.write(self._row, 12, 'EL_SECOND', style=STYLE_HEAD)
        self._sheet.write(self._row, 13, 'PREV_SQL_TEXT', style=STYLE_HEAD)
        self._sheet.write(self._row, 14, 'SQL_TEXT', style=STYLE_HEAD)
        self._row_inc()

    def insert(self, *args):
        self._sheet.write(self._row, 0, self._seq, style=STYLE_BODY)
        for i, arg in enumerate(args):
            self._sheet.write(self._row, i+1, arg, style=STYLE_BODY)
        self._row_inc()
        self._seq_inc()


if __name__ == '__main__':
    import os
    STORE_PATH = '/tmp/excel'
    _workbook = xlwt.Workbook(encoding='utf-8')
    dl = DbLock(_workbook)
    dl.insert(*['1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '3', '3', '3', '3'])
    if not os.path.exists(STORE_PATH):
        os.mkdir(STORE_PATH)
    _workbook.save('{}/个人税收管理系统每日检查_{}.xls'.format(STORE_PATH, datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
