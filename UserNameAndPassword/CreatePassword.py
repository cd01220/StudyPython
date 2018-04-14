#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
'''
Created on 2016-06-21

@author: LiuHao
History:
    ver.1.7, svn version 214: change filename from CreateCodeNumber.py to CreatePassword.py.
    ver.1.8, svn version 223: in order to support cli cascade, change webName as a optional parameter.
             refer to CreatePasswordX.cmd for cli cascade.
'''

import sys
import argparse

def Main(argv):
    parser = argparse.ArgumentParser(description="description: create password for specific web.");
    parser.add_argument("-w", "--web", dest="webName", action="store", 
                        help="set web name", default="");

    args = parser.parse_args(argv[1:]);
    if args.webName == "":
        webName = input("").strip();
    else:
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