#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
@author: LiuHao
@precondition: 
  1. openssl, version 0.9.8h
    c:\\Users\\LiuHao\\Temp>openssl version
    OpenSSL 0.9.8h 28 May 2008
  2. gnupg, version 2.0.30
    C:\\Users\\LiuHao\\Temp>gpg --version
    gpg (GnuPG) 2.0.30 (Gpg4win 2.3.2)
    libgcrypt 1.6.5
@note: 
    to restore the original file, use cipher as a temp file:
    1 gpg --output cipher -d dst
    2 openssl enc -des3 -salt -d -in cipher -out src -pass pass:xxxxxx
@change:
    ver.1.9, svn version 236: first created.
    ver.1.9, svn version 238: first available version.
    ver.1.9, svn version 239: fix bug, program crash when dst file do not exist.
'''

import os
import sys
import argparse

def Main(argv):
    parser = argparse.ArgumentParser(description="description: encode and copy my private files.");
    parser.add_argument(dest="src", help="set src file name");
    parser.add_argument(dest="dst", help="set dst file name");
    parser.add_argument(dest="password", help="set openssl password");
    parser.add_argument(dest="gnupguid", help="set gnupg user id");
    
    args = parser.parse_args(argv[1:]);
    if os.path.exists(args.dst):
        os.remove(args.dst);
    
    #1 encrypt with openssl command.
    cmd = "openssl enc -des3 -salt -e -in {0} -out {1} -pass pass:{2}";
    cmd = cmd.format(args.src, "cipher", args.password);
    os.system(cmd);

    #2 encrypt with gnupg.
    cmd = "gpg --output {0} --recipient {1} --encrypt {2}";
    cmd = cmd.format(args.dst, args.gnupguid, "cipher");
    os.system(cmd);
    
    #delete temp file.
    os.remove("cipher");
    
if __name__ == '__main__':
    sys.exit(Main(sys.argv));