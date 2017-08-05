#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-08-23

@author: LiuHao
History:
    ver.2.1, svn version 311->312: new created.    
'''

import os.path
import sys
import fnmatch
import shutil
import argparse

def FindFiles(path, mode):
    for root, _, files in os.walk(path):
        for file in fnmatch.filter(files, mode):
            yield os.path.join(root, file)

def DeleteFiles(dir):
    ignoreFiles = ["*.a", "*.ilk", "*.o", "*.obj", "*.pdb", "*.sdf"]
    for i in ignoreFiles:
        for file in FindFiles(dir, i):
            os.remove(file);
 
def Main(argv):
    parser = argparse.ArgumentParser(description="description: Analysis bitcoin market information.");
    parser.add_argument("-d", "--dir", dest="dir", action="store", type=str,
                        help="set the directory.", default="");
    args = parser.parse_args(argv[1:]);
    if args.dir == "":
        dir = input("Directory: ");
    else:
        dir = args.dir;
    DeleteFiles(dir);  

if __name__ == '__main__':
    sys.exit(Main(sys.argv));


