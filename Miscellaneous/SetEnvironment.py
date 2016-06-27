'''
Created on 2016-06-21

@author: LiuHao
'''

import os
import sys
import importlib
import argparse

def Main(argv):
    print(importlib.import_module('__main__').__doc__.split("\n")[1]);

    parser = argparse.ArgumentParser(description="description: create password for specific web.",
                                     argument_default=argparse.SUPPRESS);
    parser.add_argument("-b", "--bin", dest="binSubDirectory", action="store", help="bin sub-directory");
    parser.add_argument(dest="envName", help="set environment name");
    parser.add_argument(dest="envValue", help="set environment value");

    args = parser.parse_args(argv[1:])

    if "binSubDirectory" in args:
        #remove obsolete string from path environment
        assert(args.envName not in os.environ or len(os.environ[args.envName]) != 0);
        print(os.environ["PATH"])
        if args.envName in os.environ and os.environ[args.envName] in os.environ["PATH"]:
            begin = os.environ["PATH"].find(os.environ[args.envName]);
            if os.environ["PATH"].find(";", begin) == -1:
                end = len(os.environ["PATH"])
            else:
                end = os.environ["PATH"].find(";", begin);
            os.environ["PATH"] = os.environ["PATH"][0:begin] + os.environ["PATH"][end+1:];
        print(os.environ["PATH"])

        #add home/bin into path environment
        cmd = 'setx /m PATH "' + os.path.join(args.envValue, args.binSubDirectory) \
              + ';' + os.environ["PATH"] + '"';
        os.system(cmd);
        print(cmd);

    #set home environment.
    cmd = 'setx /m ' + args.envName + ' "' + args.envValue + '"';
    os.system(cmd);
    print(cmd);

if __name__ == '__main__':
    sys.exit(Main(sys.argv));