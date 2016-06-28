#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-5-26

@author: LiuHao
'''
import sys
import re

def main(argv):
    path = "abc;def;hij;lmn;";
    reg = r'(.*)([^;]?lmn[^;]*)(;)(.*)';
    rep = r'\1\4'
    result = re.sub(reg, rep, path).strip(";")
    
    print(result)

if __name__ == '__main__':
    sys.exit(main(sys.argv))