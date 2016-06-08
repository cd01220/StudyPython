'''
Created on 2016-5-28

@author: LiuHao
'''
import os
import sys  

def Main(argv):
    assert len(argv) == 2 and argv[1].islower();
    assert "." not in argv[1];
    userName = argv[1] + "." + "lh97";
    password = "China.LiuHao.97";
    print("User Name   : " + userName);
    print("Opt Password: " + password);
    os.system("echo " + userName + " " + password + " | clip")

if __name__ == '__main__':
    sys.exit(Main(sys.argv));



