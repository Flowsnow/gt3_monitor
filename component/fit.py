#!/usr/bin/env python  
# -*- coding: utf-8 -*-

"""
Created on 5/27/17 2:49 PM
@author: Flowsnow
@file: fit.py
@function: excel width fit
"""
import string
import sys
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s',
                    filename='gt3_app.log', filemode='a')

class FitSheetWrapper(object):
    """Try to fit columns to max size of any entry.
    To use, wrap this around a worksheet returned from the
    workbook's add_sheet method, like follows:

        sheet = FitSheetWrapper(book.add_sheet(sheet_name))

    The worksheet interface remains the same: this is a drop-in wrapper
    for auto-sizing columns.
    """
    def __init__(self, sheet):
        self.sheet = sheet
        self.widths = {}

    @staticmethod
    def get_width(label):
        reload(sys)
        sys.setdefaultencoding('utf-8')  # to solve ascii encoding error in str()
        chinese_cnt = 0
        upper_cnt = 0
        for i in str(label):
            if i not in string.printable:  # printable = digits + letters + punctuation + whitespace
                # chinese is unprintable, every chinese character has 3 unprintable unit
                chinese_cnt += 1
            if i.isupper():
                upper_cnt += 1
        # adjust the width , when containing of chinese character or upper character
        chinese_width = chinese_cnt / 3 * 2
        upper_width = upper_cnt * 1.5
        other_width = len(str(label)) - chinese_cnt - upper_cnt
        width = chinese_width + upper_width + other_width
        width = int((1 + width) * 256)
        return width if width < 65535 else 65535

    def write(self, r, c, label='', *args, **kwargs):
        try:
            self.sheet.write(r, c, label, *args, **kwargs)
            width = self.get_width(label)
        except UnicodeDecodeError:
            logging.warning('UnicodeDecodeError : {}'.format(label))
            new_label = label.decode('utf-8', 'replace').encode('utf-8')
            self.sheet.write(r, c, new_label, *args, **kwargs)
            width = self.get_width(new_label)
        if width > self.widths.get(c, 0):
            self.widths[c] = width
            self.sheet.col(c).width = width

    # 当一个类定义了__getattr__方法时，如果访问不存在的成员，会调用__getattr__方法:除了write方法外其他的都是用sheet原始的方法
    def __getattr__(self, item):
        return getattr(self.sheet, item)
