#!/usr/bin/env python  
# encoding: utf-8  

"""
Created on 5/25/17 5:03 PM
@author: Flowsnow
@file: ogg.py 
@function: ogg sheet
"""
from fit import FitSheetWrapper
import datetime
from style import STYLE_TITLE, STYLE_HEAD, STYLE_BODY


class OGG:
    """Alert sheet"""

    def __init__(self, workbook):
        self._workbook = workbook
        self._name = 'ogg运行状态检查'
        self._sheet = FitSheetWrapper(self._workbook.add_sheet(self._name))
        self._row = 0
        self._seq = 1
        self._length = 8
        self._time = datetime.datetime.now()
        self._handle_head()

    def _row_inc(self):
        self._row += 1

    def _seq_inc(self):
        self._seq += 1

    def _handle_head(self):
        self._sheet.write_merge(self._row, self._row, 0, self._length - 1, '金税三期个人税收系统ogg运行状态检查', style=STYLE_TITLE)
        self._row_inc()
        self._sheet.write(self._row, 0, '填表人')
        self._sheet.write(self._row, 2, '填表日期')
        self._sheet.write_merge(self._row, self._row, 3, self._length - 1, self._time.strftime('%Y-%m-%d %H:%M:%S'))
        self._row_inc()
        # write column name
        self._sheet.write(self._row, 0, '序号', style=STYLE_HEAD)
        self._sheet.write(self._row, 1, 'ip地址', style=STYLE_HEAD)
        self._sheet.write(self._row, 2, '进程类型', style=STYLE_HEAD)
        self._sheet.write(self._row, 3, '进程状态', style=STYLE_HEAD)
        self._sheet.write(self._row, 4, '进程名称', style=STYLE_HEAD)
        self._sheet.write(self._row, 5, 'Lag延时', style=STYLE_HEAD)
        self._sheet.write(self._row, 6, 'Time延时', style=STYLE_HEAD)
        self._sheet.write(self._row, 7, '异常时信息', style=STYLE_HEAD)
        self._row_inc()

    def insert(self, *args):
        self._sheet.write(self._row, 0, self._seq, style=STYLE_BODY)
        for i, arg in enumerate(args):
            self._sheet.write(self._row, i+1, arg, style=STYLE_BODY)
        self._row_inc()
        self._seq_inc()
