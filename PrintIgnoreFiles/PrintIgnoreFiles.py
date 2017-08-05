#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-6-14
@author: LiuHao

History:
    ver.1.5, svn version 176:  add ignore files "*-odb.cxx, *-odb.hxx, *-odb.ixx", which are generated by odb.exe.
    ver.1.5, svn version 177:  add ignore files "*-odb.sql", which are generated by odb.exe.
'''
import sys

def Main(argv):
    ignoreFolders = ["*.svn", ".git", ".metadata", ".settings",
                     ".svn", "Debug", "__pycache__", "build", "ipch"];
    ignoreFiles = ["*-odb.cpp", "*-odb.cxx", "*-odb.h", "*-odb.hxx", "*-odb.ixx", "*-odb.sql", "*.a", "*.al", "*.aps", "*.bz2",
                   "*.git", "*.gz", "*.ilk", "*.la", "*.ldb", "*.lo", "*.o", "*.obj",
                   "*.opensdf", "*.pch", "*.pdb", "*.pyc", "*.pyo", "*.rej", "*.res", "*.sdf",
                   "*.so.[0-9]*", "*.suo", "*.svn", "*.tlog", "*.user", "*.vcxproj.user",
                   "*.zip", "*_i.c", "*_i.h", ".DS_Store", ".libs", ".project", ".pydevproject", "desktop.ini",
                   "~*.doc", "~*.docx"
                   ];

    ignoreFolders.sort();
    ignoreFiles.sort();

    print("Folders (for Beyond Compare):");
    for i in ignoreFolders:
        print(i);

    print();
    print("Files (for Beyond Compare)  :");
    for i in ignoreFiles:
        print(i);

    print();
    print("Folders + Files (for Svn): ");

    for i in ignoreFolders + ignoreFiles:
        print(i, end=" ");

if __name__ == '__main__':
    sys.exit(Main(sys.argv));