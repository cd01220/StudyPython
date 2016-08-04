#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-06-21

@author: LiuHao
History:
    ver.2.0, svn version 247: first committing.
'''

import os
import sys
import filecmp
import unittest
import CopyCipherFile

class TestCopyCipherFile(unittest.TestCase):
    def setUp(self):
        self.password = "123456";
        self.uid = "anonymous";
        self.srcFile = "src.txt";
        self.gpgFile = "dst.gpg";
        self.opensslFile = "openssl.bin";
        self.cmpFile = "cmp.txt";
            
    def test_SimpleTextFile(self):
        #0 prepare
        if os.path.exists(self.srcFile):
            os.remove(self.srcFile);
        if os.path.exists(self.gpgFile):
            os.remove(self.gpgFile);
        if os.path.exists(self.opensslFile):
            os.remove(self.opensslFile);
        if os.path.exists(self.cmpFile):
            os.remove(self.cmpFile);
        
        txt = open(self.srcFile, "w");
        txt.write("0123456789");
        txt.close();
        argv = [sys.argv[0], self.srcFile, self.gpgFile, self.password, self.uid];
        CopyCipherFile.Main(argv);
        
        #1 decode with gpg command.
        cmd = "gpg --output {0} -d {1}".format(self.opensslFile, self.gpgFile);
        os.system(cmd);
        
        #2 decode with openssl command.
        cmd = "openssl enc -des3 -salt -d -in {0} -out {1} -pass pass:{2}".format(self.opensslFile, self.cmpFile, self.password);
        os.system(cmd);
        
        #3 compare files.
        self.assertTrue(filecmp.cmp(self.srcFile, self.cmpFile));
        
        #delete temp file.
        os.remove(self.srcFile);
        os.remove(self.gpgFile);
        os.remove(self.opensslFile);
        os.remove(self.cmpFile);
    
    def tearDown(self):
        pass;
    
if __name__ == '__main__':
    unittest.main();
