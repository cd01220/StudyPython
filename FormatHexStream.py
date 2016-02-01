#! /usr/bin/env python3.3
# -*- coding: GB2312 -*-
# Function:
#   Format sting "0001020304050607080910" into "0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x10"

def FormatHexString(string):
    x = "0x" + string[0] + string[1]
    for i in range(2, len(string), 2):
        if ((i % 16) != 0):
            x = x + ", 0x" + string[i] + string[i+1]            
        else:
            x = x + ",\r\n0x" + string[i] + string[i+1] 
    print(x)
    return len(string)

FormatHexString("4af01e0001c30000f000f01100010000f00b4109000301000201000101efec089c")