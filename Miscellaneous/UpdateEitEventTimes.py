#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-

import glob

srcStr="2016-08-"
dstStr="2017-08-"

for file in glob.glob("*_eit_*.xml"):
    lines = open(file, "r").readlines()
    lineNumber = len(lines) - 1
    for i in range(lineNumber):
        if srcStr in lines[i]:
            lines[i]=lines[i].replace(srcStr,dstStr)
    open(file, "w").writelines(lines)

