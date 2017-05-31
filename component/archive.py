#!/usr/bin/env python  
# encoding: utf-8  

"""
Created on 5/25/17 2:18 PM
@author: Flowsnow
@file: archive.py 
@function: archive sheet
"""
from fit import FitSheetWrapper
import datetime
from style import STYLE_BODY, STYLE_TITLE, STYLE_HEAD


class Archive:
    """archive sheet"""

    def __init__(self, workbook):
        self._workbook = workbook
        self._name = '归档情况检查'
        self._sheet = FitSheetWrapper(self._workbook.add_sheet(self._name))
        self._row = 0
        self._seq = 1
        self._length = 6
        self._time = datetime.datetime.now()
        self._handle_head()

    def _row_inc(self):
        self._row += 1

    def _seq_inc(self):
        self._seq += 1

    def _handle_head(self):
        self._sheet.write_merge(self._row, self._row, 0, self._length - 1, '金税三期个人税收系统归档情况检查', style=STYLE_TITLE)
        self._row_inc()
        self._sheet.write(self._row, 0, '填表人')
        self._sheet.write(self._row, 2, '填表日期')
        self._sheet.write_merge(self._row, self._row, 3, self._length - 1, self._time.strftime('%Y-%m-%d %H:%M:%S'))
        self._row_inc()
        # write column name
        self._sheet.write(self._row, 0, '序号', style=STYLE_HEAD)
        self._sheet.write(self._row, 1, '数据库', style=STYLE_HEAD)
        self._sheet.write(self._row, 2, '是否归档', style=STYLE_HEAD)
        self._sheet.write(self._row, 3, '总空间', style=STYLE_HEAD)
        self._sheet.write(self._row, 4, '已经空间', style=STYLE_HEAD)
        self._sheet.write(self._row, 5, '剩余空间', style=STYLE_HEAD)
        self._row_inc()

    def insert(self, *args):
        self._sheet.write(self._row, 0, self._seq, style=STYLE_BODY)
        for i, arg in enumerate(args):
            self._sheet.write(self._row, i+1, arg, style=STYLE_BODY)
        self._row_inc()
        self._seq_inc()
