#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-06-21

@author: LiuHao
History:
    ver.1.7, svn version 216: first committing.
    ver.1.7, svn version 211: change to use md5.
'''

import sys
import importlib
import argparse
import hashlib

def Main(argv):
    print(importlib.import_module('__main__').__doc__.split("\n")[1]);

    parser = argparse.ArgumentParser(description="description: create password for specific web.");
    parser.add_argument(dest="rawPassword", help="raw password string");

    args = parser.parse_args(argv[1:]);
    rawPassword = args.rawPassword.strip();
    m = hashlib.md5();
    m.update(rawPassword.encode());
    md5Password = m.hexdigest();
    dic = ['*', '{', 'e', '/', '<', 'R', 'f', ']', '5', '&', 
            '1', 'F', 'z', 'O', 'b', 'g', 'A', '+', '9', 'c', 
            'x', '}', 'E', 'h', 'Y', 'J', '#', 'S', 'H', '$', 
            'w', 'V', 'X', '-', ')', '.', 'y', 'W', ':', 'L', 
            ';', 'M', '(', '2', '?', 'i', 'B', 't', '`', '8', 
            'k', 'l', '_', 'q', 'C', '=', 's', 'u', '!', '4', 
            'n', 'D', 'd', 'v', 'o', ',', '6', 'G', '7', 'I', 
            '^', '"', 'j', '3', 'K', "'", '[', 'a', 'm', 'U', 
            '%', '0', '@', '\\', '>', 'p', 'T', '~', 'r', '|', 
            'Z', 'P', 'Q', 'N'];
    output = "";
    for i in range(0, 20, 2):
        index = int(md5Password[i:i+2], 16)
        output = output + dic[index % len(dic)];
        
    print(output);
    return 0;
    
if __name__ == '__main__':
    sys.exit(Main(sys.argv));