#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-5-28

@author: LiuHao
'''
import os
import sys
import argparse

def Main(argv):
    parser = argparse.ArgumentParser(description="description: create password for specific web.");
    parser.add_argument(dest="webName", help="set web name");

    args = parser.parse_args(argv[1:]);
    webName = args.webName.strip();
    
    userName = webName + "." + "lh97";
    password = "China.LiuHao.97";
    print("User Name   : " + userName);
    print("Opt Password: " + password);
    os.system("echo " + userName + " " + password + " | clip")

if __name__ == '__main__':
    sys.exit(Main(sys.argv));



