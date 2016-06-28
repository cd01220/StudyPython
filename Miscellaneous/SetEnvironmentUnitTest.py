#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-06-21

@author: LiuHao
History:
    ver.1.6, svn version 198: add test_HomeEnvAndOldPathAtMiddle.
    ver.1.6, svn version 199: add test_HomeEnvAndOldPathAtLasst.
    ver.1.6, svn version 200: change this history.
'''

import os
import sys
import unittest
import SetEnvironment

class TestFormatWords(unittest.TestCase):
    def setUp(self):
        pass;
    
    def test_OnlyHomeEnv(self):
        self.assertTrue("A01_HOME" not in os.environ);
        argv = [sys.argv[0], "A01_HOME", "A01HomeDir", "-d"];
        SetEnvironment.Main(argv);
        self.assertTrue("A01_HOME" in os.environ);
        self.assertEqual(os.environ["A01_HOME"], "A01HomeDir");

    def test_HomeEnvAndOldPathIsEmpty(self):
        path = os.environ["PATH"].strip(";");
        self.assertTrue("A02_HOME" not in os.environ);
        argv = [sys.argv[0], "A02_HOME", "A02HomeDir", "-d", "-b", "bin"];
        SetEnvironment.Main(argv);
        self.assertTrue("A02_HOME" in os.environ);
        self.assertEqual(os.environ["A02_HOME"], "A02HomeDir");
        self.assertTrue("A02HomeDir\\bin" in os.environ["PATH"]);
        self.assertEqual("A02HomeDir\\bin;" + path, os.environ["PATH"]);
        
    def test_HomeEnvAndOldPathAtFist(self):
        path = os.environ["PATH"].strip(";");
        self.assertTrue("A03_HOME" not in os.environ);
        argv = [sys.argv[0], "A03_HOME", "A03OldHomeDir", "-d", "-b", "bin"];
        SetEnvironment.Main(argv);
        self.assertEqual("A03OldHomeDir\\bin;" + path, os.environ["PATH"]);
        argv[2] = "A03NewHomeDir"
        SetEnvironment.Main(argv);        
        self.assertTrue("A03_HOME" in os.environ);
        self.assertEqual(os.environ["A03_HOME"], "A03NewHomeDir");
        self.assertEqual("A03NewHomeDir\\bin;" + path, os.environ["PATH"]);
    
    def test_HomeEnvAndOldPathAtMiddle(self):
        path = os.environ["PATH"].strip(";");
        self.assertTrue("A04_HOME" not in os.environ);
        argv1 = [sys.argv[0], "A04_HOME", "A04OldHomeDir", "-d", "-b", "bin"];
        SetEnvironment.Main(argv1);
        argv2 = [sys.argv[0], "A05_HOME", "A05HomeDir", "-d", "-b", "bin"];
        SetEnvironment.Main(argv2);
        #Start test.
        argv1[1] = "A04_HOME";
        argv1[2] = "A04NewHomeDir";
        SetEnvironment.Main(argv1);
        self.assertEqual(os.environ["A04_HOME"], "A04NewHomeDir");        
        self.assertEqual("A04NewHomeDir\\bin;" + "A05HomeDir\\bin;" + path, os.environ["PATH"]);
        pass;

    def test_HomeEnvAndOldPathAtLasst(self):
        argv = [sys.argv[0], "A06_HOME", "A06OldHomeDir", "-d"];
        SetEnvironment.Main(argv);        
        path = os.environ["PATH"].strip(";");
        os.environ["PATH"] = path + ";" + "A06OldHomeDir\\bin";
        #Start test
        argv = [sys.argv[0], "A06_HOME", "A06NewHomeDir", "-d", "-b", "bin"];
        SetEnvironment.Main(argv);
        self.assertTrue("A06_HOME" in os.environ);
        self.assertEqual(os.environ["A06_HOME"], "A06NewHomeDir");
        self.assertEqual("A06NewHomeDir\\bin;" + path, os.environ["PATH"]);
    
    def tearDown(self):
        pass;
    
if __name__ == '__main__':
    unittest.main();