#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-08-02

@author: LiuHao
History:
    ver.2.0, svn version 277->278: add .py version and btcbenchmark value information into output.
'''
import argparse
import sys
import time
from urllib import request

import json

def ComparePrice(loops):
    btcbenchmark = 4.5;
    ltcbenchmark = 0.03;
    print("ver.2.0 svn 277, btcbenchmark={0:.2f}, ltcbenchmark={1:.2f}".format(btcbenchmark, ltcbenchmark))
    fmt = "{0:4s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s}";
    print(fmt.format("Coin", "Buy Price", "Sell Price", "Buy Price", "Sell Price", "Difference", "Difference"));
    fmt = "     {0:10s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s}";
    print(fmt.format("(btctrade)", "(btctrade)", "(okcoin)", "(okcoin)", "(b-o)", "(o-b)"));
    fmt = "{0:4s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s}";
    print(fmt.format("----", "----------", "----------", "----------", "----------", "----------", "----------"));
    
    #1 transfer money from okcoin to btctrade, -1 transfer money from btctrade to okcoin, 0 clearance
    btcOpt = 0;  
    ltcOpt = 0;  
    btcProfit = 0;
    ltcProfit = 0;
    for i in range(0, loops):
        coin = "btc" if i % 2 == 0 else "ltc";
        if i % 100 == 0:  
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())));
        
        try:            
            httpResponse = request.urlopen("http://api.btctrade.com/api/ticker?coin="+coin, data=None, timeout=2);
            btctradeMarket = json.loads(httpResponse.read().decode());
            
            httpResponse = request.urlopen("https://www.okcoin.cn/api/v1/ticker.do?symbol="+coin+"_cny", data=None, timeout=2);
            okcoinMarket = json.loads(httpResponse.read().decode());
        except:
            pass;
        else:
            btctradeBuyPrice = btctradeMarket["buy"];
            btctradeSellPrice = btctradeMarket["sell"];
            okcoinBuyPrice  = float(okcoinMarket["ticker"]["buy"]);
            okcoinSellPrice = float(okcoinMarket["ticker"]["sell"]);
            
            if coin == "btc":
                delimiter = "*"
                benchmark = btcbenchmark
                opt = btcOpt;
                profit = btcProfit;
            else:
                delimiter = "#"
                benchmark = ltcbenchmark
                opt = ltcOpt;
                profit = ltcProfit;
                
            signal = delimiter * 5;
            if btctradeBuyPrice - okcoinSellPrice > benchmark:
                if opt == 0:
                    signal = delimiter + "$<" + delimiter * 2;  #transfer money from okcoin to btctrade;
                    profit = btctradeBuyPrice - okcoinSellPrice;
                elif opt == -1:
                    signal = delimiter + "$<<" + delimiter;  #transfer money from okcoin to btctrade;
                    profit = btctradeBuyPrice - okcoinSellPrice;
                opt = 1;
            elif okcoinBuyPrice - btctradeSellPrice > benchmark:
                if opt == 0:
                    signal = delimiter + "$>" + delimiter * 2;  #transfer money from btctrade to okcoin;
                    profit = okcoinBuyPrice - btctradeSellPrice;
                elif opt == 1:
                    signal = delimiter + "$>>" + delimiter;  #transfer money from btctrade to okcoin;
                    profit = okcoinBuyPrice - btctradeSellPrice;
                opt = -1;
            elif profit - (btctradeSellPrice - okcoinBuyPrice) > benchmark:
                if opt == 1:
                    signal = delimiter + "$=" + delimiter * 2;
                    opt = 0;
                    profit = 0;
            elif profit - (okcoinSellPrice - btctradeBuyPrice) > benchmark:
                if opt == -1:
                    signal = delimiter + "$=" + delimiter * 2;
                    opt = 0;
                    profit = 0;
            
            
            if coin == "btc":
                btcOpt = opt;
                btcProfit = profit;
            else:
                ltcOpt = opt;
                ltcProfit = profit;
                                
            fmt = "{0:4s} {1:10.2f} {2:10.2f} {3:10.2f} {4:10.2f} {5:10.2f} {6:10.2f} " + signal;
            print(fmt.format(coin, btctradeBuyPrice, btctradeSellPrice, okcoinBuyPrice, okcoinSellPrice, 
                             btctradeBuyPrice - okcoinSellPrice, okcoinBuyPrice - btctradeSellPrice));
            
        time.sleep(1);

def Main(argv):    
    parser = argparse.ArgumentParser(description="description: Analysis bitcoin market information.");
    parser.add_argument("-l", "--loops", dest="loops", action="store", type=int,
                        help="set current price.", default=0);
    args = parser.parse_args(argv[1:]);
    if args.loops == 0:
        loops = int(input("Loop Number: "));
    else:
        loops = args.loops;
    ComparePrice(loops);  


if __name__ == '__main__':
    sys.exit(Main(sys.argv));