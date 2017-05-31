#!/usr/bin/env python  
# encoding: utf-8  

"""
Created on 5/31/17 9:44 AM
@author: Flowsnow
@file: style.py 
@function: excel style when writing
"""
import xlwt


STYLE_TITLE = xlwt.easyxf('font: bold on;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                          pattern: pattern solid, fore_color gold;\
                          alignment: horizontal center')

STYLE_HEAD = xlwt.easyxf('font: bold on;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                         pattern : pattern solid, fore_color blue;')

STYLE_BODY = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white;')
