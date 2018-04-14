#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
'''
Created on 2016-07-11

@author: LiuHao
History:
    ver.1.7, svn version 220: first committing.
    ver.1.8, svn version 223: in order to support cli cascade, change strLength as a optional parameter.
             refer to CreatePasswordX.cmd for cli cascade.
'''

import sys
import argparse
import random

def Main(argv):
    parser = argparse.ArgumentParser(description="description: create password for specific web.");
    parser.add_argument("-l", "--length", dest="strLength", action="store", 
                        help="random string length", type=int, default=0);
    args = parser.parse_args(argv[1:]);
    if args.strLength == 0:
        inputStr = input("");
        strLength = int(inputStr);
    else:
        strLength = args.strLength;
    
    dic = [chr(i) for i in range(33, 127)];
    random.shuffle(dic)
    print("".join(dic[0:strLength]));
    return 0;
    
if __name__ == '__main__':
    sys.exit(Main(sys.argv));