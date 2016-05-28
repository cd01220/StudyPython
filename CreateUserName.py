'''
Created on 2016-5-28

@author: LiuHao
'''
import sys  

def Main(argv):
    assert len(argv) == 2 and argv[1].islower();
    assert "." not in argv[1];
    print("User Name   : " + argv[1] + "." + "lh97");
    print("Opt Password: " + "China.LiuHao.97");

if __name__ == '__main__':
    sys.exit(Main(sys.argv));
