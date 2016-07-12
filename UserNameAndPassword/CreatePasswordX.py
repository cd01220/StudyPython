#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-07-10

@author: LiuHao
History:
    ver.1.7, svn version 216: first committing.
    ver.1.7, svn version 211: change to use md5.
    ver.1.8, svn version 223: in order to support cli cascade, change rawPassword as a optional parameter.
             refer to CreatePasswordX.cmd for cli cascade.
'''

import sys
import argparse
import hashlib

def Main(argv):
    parser = argparse.ArgumentParser(description="description: create password for specific web.");
    parser.add_argument("-r", "--raw", dest="rawPassword", action="store",  
                        help="raw password string", default="");

    args = parser.parse_args(argv[1:]);
    if args.rawPassword == "":
        rawPassword = input("");
    else:
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