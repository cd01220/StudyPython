#! /usr/bin/env python3.3
# -*- coding: utf-8 -*-
'''
Created on 2016-5-26

@author: LiuHao
History:
    ver.2.0, svn version 257->258: add trading history, (4385.00,  394.65, "2017.07.29").
    ver.2.0, svn version 258->259: add trading history, (21936973, 21936885, 21939824, 21945015).
    ver.2.0, svn version 259->300: 1 let Main() support -p parameter. 
                                   2 add function PrintStatisticData() to support calling from other module.
    ver.2.0, svn version 277->278: add trading history, (22131671).
    ver.2.0, svn version 282->283: add trading history, (22160315).
    ver.2.0, svn version 285->286: add trading history, (22164574).
                                   
Example:
    from urllib import request
    import json
    import BitcoinRecords      
    httpResponse = request.urlopen("http://api.btctrade.com/api/ticker?coin=btc");
    market = json.loads(httpResponse.read().decode());
    currentPrice = market["last"];
    BitcoinRecords.PrintAnalysisData();
    BitcoinRecords.PrintStatisticData(currentPrice);                             
'''
import sys
import argparse

def PrintAnalysisData():
    print("-------------Analysis Data-------------");
    #deals, priceMargin, price, fundUtilizationRate
    elements = [(20, 60, 4000, 0.40), (20, 60, 4000, 0.80), 
                (40, 30, 4000, 0.40), (40, 30, 4000, 0.80),
                (40, 60, 4000, 0.40), (40, 60, 4000, 0.80),
                (60, 60, 4000, 0.40), (60, 60, 4000, 0.80)];
        
    print("Deals  Price Margin   Price   Fund Utilization Rate  Output Rate");
    print("-----  ------------  -------  ---------------------  -----------");
    for deals, priceMargin, price, fundUtilizationRate in  elements:
        incRate = (1 + priceMargin/price) ** (deals) * fundUtilizationRate + (1-fundUtilizationRate);
        resultString = "{0:5d}  {1:12d}  {2:7d}  {3:21.2f}  {4:11.2f}";
        print(resultString.format(deals, priceMargin, price, fundUtilizationRate, incRate));    
    print("");

def PrintStatisticData(currentPrice):
    print("-------------History  Data-------------");
    records = [(4341.67, -400.00, "2016.07.11"), (4415.01, -500.00, "2016.07.22"), 
               (4365.00, -200.00, "2016.07.22"), (4377.00,  -43.77, "2016.07.26"), 
               (4400.00,   79.20, "2016.07.27"), (4355.00, -391.95, "2017.07.27"),
               (4385.00,  394.65, "2017.07.29"), (4345.00, -443.19, "21936973, 2017.07.31"),
               (4351.00, -395.94, "21936885, 2017.07.31"), (4220.45, -291.20, "21939824, 2017.07.31"),
               (4195.45, -209.70, "21945015, 2017.07.31"), (3580.00, -400.96, "22131671, 2017.08.03"),
               (3630.00,  406.56, "22160315, 2017.08.03"), (3645.00, -404.59, "22164574, 2017.08.03"),
               (3680.00,  408.48, "22166974, 2017.08.03"), (3715.00, -408.65, "22170442, 2017.08.03"),
               (3720.30,  409.26, "22217520, 2017.08.03")];
    totalInvestment  = 0;
    coinStock = 0;
    grossProfit = 0;
    for x,y,_ in records:
        if y > 0:
            avrPrice = totalInvestment / coinStock;
            coins    = y / x;
            grossProfit     = grossProfit + (x - avrPrice) * coins;
            totalInvestment = totalInvestment - avrPrice * coins;
            coinStock       = coinStock - coins;
        else:
            totalInvestment = totalInvestment + abs(y);
            coinStock = coinStock + (abs(y) / x);
        #print("{0:.2f}, {1:.2f}, , {2:.2f}".format(totalInvestment, coinStock, totalInvestment / coinStock))
        #stock can not be negative. 
        assert(coinStock > -0.0001);
    print("hist net profit      : {0:.2f}".format(grossProfit));
    
    if (coinStock > 0.0001):
        avrPrice = totalInvestment / coinStock;
        incRate = (currentPrice - avrPrice) / avrPrice;
        profit = (currentPrice - avrPrice) * coinStock;
        print("average price        : {0:.2f}".format(avrPrice)); 
        print("current price        : {0:.2f}".format(currentPrice)); 
        print("total investment Rmb : {0:.2f}".format(totalInvestment));
        print("total stock Btc      : {0:.4f}".format(coinStock));    
        print("amount of increase   : {0:.4f}".format(incRate));
        print("profit               : {0:.2f}".format(profit));

def Main(argv):
    parser = argparse.ArgumentParser(description="description: Analysis bitcoin dealing information.");
    parser.add_argument("-p", "--price", dest="currentPrice", action="store", type=int,
                        help="set current price.", default=0);
    args = parser.parse_args(argv[1:]);
    if args.currentPrice == 0:
        currentPrice = int(input("Current Price: "));
    else:
        currentPrice = args.currentPrice;
        
    PrintAnalysisData();
    PrintStatisticData(currentPrice);

if __name__ == '__main__':
    sys.exit(Main(sys.argv));