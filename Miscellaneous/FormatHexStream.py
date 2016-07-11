#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Function:
  Format sting "0001020304050607080910" into "0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10"
'''
import sys

def FormatHexString(string):
    x = "0x" + string[0] + string[1]
    for i in range(2, len(string), 2):
        if ((i % 32) != 0):
            x = x + ", 0x" + string[i] + string[i+1]
        else:
            x = x + ",\n0x" + string[i] + string[i+1]
    print(x)
    return len(string)


def Main(argv):
    FormatHexString("4af0130001c30101f000f00600010000f000d520e9f6")

if __name__ == '__main__':
    sys.exit(Main(sys.argv))
