#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
'''
Created on 2016-06-21

@author: LiuHao
History:

Example: SetEnvVariableSubstring.py PATH D:\GreenSoftware D:\GreenSoft
'''

import os
import sys
import importlib
import argparse
import re

def Main(argv):
    print(importlib.import_module('__main__').__doc__.split("\n")[1]);

    parser = argparse.ArgumentParser(description="description: update environment sub string.");
    parser.add_argument("-d", "--debug", dest="isDebug", action="store_true", help="is debug");
    parser.add_argument(dest="variableName", help="environment variable name");
    parser.add_argument(dest="oldValue", help="old value");
    parser.add_argument(dest="newValue", help="new value");

    args = parser.parse_args(argv[1:])
    if len(args.oldValue) == 0:
        # use a guid to avoid repetition.
        args.oldValue = "02471ec5-95d3-48dc-9533-666271262e06"; 

    #remove obsolete string from environment variable string
    envString = "";
    if args.variableName in os.environ:
        envString = os.environ[args.variableName].strip(";");        
    #use repr() to convert a string into raw string.
    reg = r'(.*)([^;]?' + repr(args.oldValue).strip("'") + r'[^;]*)(;)(.*)';
    rep = r'\1\4'
    if len(args.newValue) == 0:
        envString = re.sub(reg, rep, envString + ";").strip(";");
    else:
        envString = args.newValue + ";" + re.sub(reg, rep, envString + ";").strip(";");
    envString = envString.strip(";");
    os.environ[args.variableName] = envString; #for unit test.

    #add home/bin into envString environment
    cmd = 'setx /m ' + args.variableName + ' "' + envString + '"';
    if args.isDebug:
        print(cmd);
    else:
        os.system(cmd);

if __name__ == '__main__':
    sys.exit(Main(sys.argv));