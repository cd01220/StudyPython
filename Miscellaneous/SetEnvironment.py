#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-06-21

@author: LiuHao
History:
    ver.1.6, svn version 191->192: change to use regular express to do string operation.
    ver.2.0, svn version 245->246: add parameter "-a", to add new value to existed evn.
             example, to add a directory into PATH:
             C:\\> SetEnvironment.py -a PATH "C:\\Program Files\\Python33\\Scripts"
'''

import os
import sys
import importlib
import argparse
import re

def Main(argv):
    print(importlib.import_module('__main__').__doc__.split("\n")[1]);

    parser = argparse.ArgumentParser(description="description: create password for specific web.");
    parser.add_argument("-a", "--append", dest="isAppend", action="store_true", help="is append");
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

    #calculate new envName.
    if args.isAppend:
        if args.envName in os.environ:
            oldValue = os.environ[args.envName].strip(";");
            if args.envValue + ";" in oldValue + ";":
                envValue = oldValue;
            else:
                envValue = args.envValue + ";" + oldValue;
        else:
            envValue = args.envValue;
    else:
        envValue = args.envValue;
    #set home environment.
    os.environ[args.envName] = envValue; #for unit test.
    cmd = 'setx /m ' + args.envName + ' "' + envValue + '"';
    if args.isDebug:
        print(cmd);
    else:
        os.system(cmd);

if __name__ == '__main__':
    sys.exit(Main(sys.argv));