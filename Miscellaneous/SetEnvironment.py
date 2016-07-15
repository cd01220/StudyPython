#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-06-21

@author: LiuHao
History:
    ver.1.6, svn version 191->192: change to use regular express to do string operation.
'''

import os
import sys
import importlib
import argparse
import re

def Main(argv):
    print(importlib.import_module('__main__').__doc__.split("\n")[1]);

    parser = argparse.ArgumentParser(description="description: create password for specific web.");
    parser.add_argument("-b", "--bin", dest="binSubDirectory", action="store", help="bin sub-directory", default="");
    parser.add_argument("-d", "--debug", dest="isDebug", action="store_true", help="is debug");
    parser.add_argument(dest="envName", help="set environment name");
    parser.add_argument(dest="envValue", help="set environment value");

    args = parser.parse_args(argv[1:])

    if len(args.binSubDirectory) != 0:
        #remove obsolete string from path environment
        path = os.environ["PATH"].strip(";");
        oldValue = "" if args.envName not in os.environ else os.environ[args.envName];
        #use repr() to convert a string into raw string.
        reg = r'(.*)([^;]?' + repr(oldValue).strip("'") + r'[^;]*)(;)(.*)';
        rep = r'\1\4'
        path = os.path.join(args.envValue, args.binSubDirectory) + ";" \
             + re.sub(reg, rep, path + ";").strip(";");
        os.environ["PATH"] = path; #for unit test.

        #add home/bin into path environment
        cmd = 'setx /m PATH "' + path + '"';
        if args.isDebug:
            print(cmd);
        else:
            os.system(cmd);

    #set home environment.
    os.environ[args.envName] = args.envValue; #for unit test.
    cmd = 'setx /m ' + args.envName + ' "' + args.envValue + '"';
    if args.isDebug:
        print(cmd);
    else:
        os.system(cmd);

if __name__ == '__main__':
    sys.exit(Main(sys.argv));