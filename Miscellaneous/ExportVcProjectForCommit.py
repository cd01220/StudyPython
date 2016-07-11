#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-

import os
import sys
import shutil

def Main(argv):
    projectName = "Gs9330"
    projectDir  = "D:\Project\Project.VisualStudio2012\Gs9330"
    oldSlnNmae = "Gs9330.sln"
    newSlnNmae = "Gs9330NoUnit.sln"
    
    tempDir = "D:/Temp/" + projectName
    if os.path.exists(tempDir):
        shutil.rmtree(tempDir)
    
    os.system("svn export " + projectDir + " " + tempDir)
    os.chdir("D:/Temp/" + projectName)
    
    if os.path.exists("VcUnitTestProject"):
        shutil.rmtree("VcUnitTestProject")
    if os.path.exists("UnitTestCodes"):
        shutil.rmtree("UnitTestCodes")
    if os.path.exists("Documents"):
        shutil.rmtree("Documents")
    os.remove("ReadMe.txt")
    os.remove(oldSlnNmae)
    os.rename(newSlnNmae, oldSlnNmae)

if __name__ == '__main__':
    sys.exit(Main(sys.argv))







