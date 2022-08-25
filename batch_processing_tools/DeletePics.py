#!/usr/bin/env python3
# encoding: utf-8
# coding style: pep8
# ====================================================
#   Copyright (C)2020 All rights reserved.
#
#   Author        : Bo Wu
#   Email         : wubo.cs@gmail.com
#   File Name     : DeletePics.py
#   Last Modified : 2020-04-05 00:39
#   Describe      : 
#
# ====================================================

import sys
import os
import datetime

cur_dir = os.path.dirname(os.path.abspath(__file__))

def main():
    today = datetime.date.today().strftime('%Y%m%d')
    # yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y%m%d')
    # daybefore = (datetime.date.today() + datetime.timedelta(days=-2)).strftime('%Y%m%d')
    timelist = [today]
    data_path = os.path.join(cur_dir, '../newDetect/savePics')
    for parent, dirnames, filenames in os.walk(data_path):
        for fname in filenames:
            d = fname.split('_')[0]
            if d not in timelist:
                os.remove(os.path.join(parent, fname))
    data_path = os.path.join(cur_dir, '../VisionPackage/test')
    for parent, dirnames, filenames in os.walk(data_path):
        for fname in filenames:
            os.remove(os.path.join(parent, fname))
    
    data_path = os.path.join(cur_dir, '../newDetect/log_files')
    for parent, dirnames, filenames in os.walk(data_path):
        for fname in filenames:
            n, ext = os.path.splitext(fname)
            if ext == '.log':
                os.remove(os.path.join(parent, fname))

    data_path = os.path.join(cur_dir, '../VisionPackage/mask_file')
    for parent, dirnames, filenames in os.walk(data_path):
        for fname in filenames:
            n, ext = os.path.splitext(fname)
            if ext == '.log':
                os.remove(os.path.join(parent, fname))

if __name__ == '__main__':
    main()
