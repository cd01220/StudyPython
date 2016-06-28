#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-

import os.path
import sys
import fnmatch
import shutil

def FindFiles(path, mode):
    for root, _, files in os.walk(path):
        for file in fnmatch.filter(files, mode):
            yield file, os.path.join(root, file)

def Main(argv):
    if os.path.exists("Temp"):
        shutil.rmtree("Temp");
    
    os.mkdir("Temp");
    for file, pathFile in FindFiles(".\\StudyVc", "*.cpp"):
        targetFile = os.path.join(".\\Temp", file);
        shutil.copyfile(pathFile, targetFile);
    
    for file, pathFile in FindFiles(".\\StudyVc", "*.h"):
        targetFile = os.path.join(".\\Temp", file);
        shutil.copyfile(pathFile, targetFile);

if __name__ == '__main__':
    sys.exit(Main(sys.argv));


