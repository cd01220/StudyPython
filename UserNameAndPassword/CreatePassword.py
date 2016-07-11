#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-06-21

@author: LiuHao
History:
    ver.1.7, svn version 214: change filename from CreateCodeNumber.py to CreatePassword.py.
'''

import sys
import importlib
import argparse

def Main(argv):
    print(importlib.import_module('__main__').__doc__.split("\n")[1]);

    parser = argparse.ArgumentParser(description="description: create password for specific web.");
    parser.add_argument(dest="webName", help="set web name");

    args = parser.parse_args(argv[1:]);
    webName = args.webName.strip();
    if (len(webName) < 3):
        parser.print_help();
        print("web name must have at lest 3 chars!");
        return 1;
        
    output = "";
    for i in range(0, 3):
        output = output + format(ord(webName[i]), "02x");

    output = list(output);
    output[1], output[2] = output[2], output[1];
    output = "".join(output);
    print(webName + "." + webName[0].capitalize() + output);
    return 0;
    
if __name__ == '__main__':
    sys.exit(Main(sys.argv));