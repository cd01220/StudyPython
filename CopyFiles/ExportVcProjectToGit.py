#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import shutil
import zipfile

def Main(argv):
    parser = argparse.ArgumentParser(description="description: export src dir to dst dir, then zip with password.");    
    parser.add_argument(dest="srcDir", help="src directory");
    parser.add_argument(dest="dstDir", help="dst directory");    

    args = parser.parse_args(argv[1:]);
    if os.path.exists(args.dstDir):
        shutil.rmtree(args.dstDir);
    
    os.system("svn export " + args.srcDir + " " + args.dstDir);
    filelist = [];
    for root, _, files in os.walk(args.dstDir):
        for name in files:
            filelist.append(os.path.join(root, name));            
        
    zf = zipfile.ZipFile(os.path.join(args.dstDir + ".zip"), "w", zipfile.zlib.DEFLATED);
    for tar in filelist:        
        arcname = tar[len(args.dstDir):]
        zf.write(tar,arcname)         
    zf.close()
    
if __name__ == '__main__':
    sys.exit(Main(sys.argv));







