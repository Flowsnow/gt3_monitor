#!/usr/bin/env python  
# encoding: utf-8  

"""
Created on 5/25/17 5:17 PM
@author: Flowsnow
@file: disk_busy.py 
@function: 
"""
from fit import FitSheetWrapper
import datetime
from style import STYLE_BODY, STYLE_TITLE, STYLE_HEAD


class DiskBusy:
    """Alert sheet"""

    def __init__(self, workbook):
        self._workbook = workbook
        self._name = '磁盘繁忙程度检查'
        self._sheet = FitSheetWrapper(self._workbook.add_sheet(self._name))
        self._row = 0
        self._seq = 1
        self._length = 7
        self._time = datetime.datetime.now()
        self._handle_head()

    def _row_inc(self):
        self._row += 1

    def _seq_inc(self):
        self._seq += 1

    def _handle_head(self):
        self._sheet.write_merge(self._row, self._row, 0, self._length - 1, '金税三期个人税收系统磁盘繁忙程度检查', style=STYLE_TITLE)
        self._row_inc()
        self._sheet.write(self._row, 0, '填表人')
        self._sheet.write(self._row, 2, '填表日期')
        self._sheet.write_merge(self._row, self._row, 3, self._length - 1, self._time.strftime('%Y-%m-%d %H:%M:%S'))
        self._row_inc()
        # write column name
        self._sheet.write(self._row, 0, '序号', style=STYLE_HEAD)
        self._sheet.write(self._row, 1, '主机IP', style=STYLE_HEAD)
        self._sheet.write(self._row, 2, '磁盘名', style=STYLE_HEAD)
        self._sheet.write(self._row, 3, 'Busy%', style=STYLE_HEAD)
        self._sheet.write(self._row, 4, 'tps', style=STYLE_HEAD)
        self._sheet.write(self._row, 5, 'rd_sec/s', style=STYLE_HEAD)
        self._sheet.write(self._row, 6, 'wr_sec/s', style=STYLE_HEAD)
        self._row_inc()

    def insert(self, *args):
        self._sheet.write(self._row, 0, self._seq, style=STYLE_BODY)
        for i, arg in enumerate(args):
            self._sheet.write(self._row, i+1, arg, style=STYLE_BODY)
        self._row_inc()
        self._seq_inc()
