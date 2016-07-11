#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-5-26

@author: LiuHao
'''
import sys
import random

def main(argv):
    dic = [chr(i) for i in range(33, 127)];
    random.shuffle(dic)
    print(dic)

if __name__ == '__main__':
    sys.exit(main(sys.argv))