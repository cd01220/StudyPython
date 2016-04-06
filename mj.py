#! /usr/bin/env python3.3
# -*- coding: GB2312 -*-

import copy
import itertools
from functools import reduce

#define constant
TotalPais = 108.0
DebugPaisInRivalRate = True
DebugHostXiajiaoRate = False

def GetVersion():
    """
    In order to make Majiang algorithm more usefull and easy to understand,
    Liuhao rewrite Majiang algorithm based on python.  
    """
    ver = "Majiang for Python3.3,  v1.0"
    return ver


#### Base rule, to calculate the price for DianPao, DianGang, Zimo, AnGang ... ####
class BaseRule:
    def __init__(self):
        self.baseWage = 10
    def GetBaseWage(self):
        return self.baseWage
    def GetDianpaoPrice(self, fan):
        assert fan >= 0 and fan <= 4, "Wrong parameter."
        return self.baseWage * (2.0 ** fan)
    def GetZimoUnitPrice(self, fan):
        assert fan >= 0 and fan <= 4, "Wrong parameter."
        return self.baseWage * (2.0 ** fan) + self.baseWage
        #return self.baseWage * (2.0 ** (fan + 1))
    def GetZimoIncome(self, rivalsNum, fan):
        return self.GetZimoUnitPrice(fan) * rivalsNum
    def GetWanGangIncome(self, rivalsNum):
        return self.baseWage * rivalsNum
    def GetDianGangIncome(self, rivalsNum):
        return self.baseWage * rivalsNum + self.baseWage
    def GetAnGangIncome(self, rivalsNum):
        return self.baseWage * 2 * rivalsNum

class PaisDistribution:
    """
    thePaiqiang: number of pais left behind in Paiqiang.
    theKeyRival: The rival number who needs this kind of Pai(for example who need Tong).
    effectivePais: The pais number in which the abailable pais distribute 
    """
    def __init__(self, thePaiqiang, 
                 theKeyRival, theAvailablePais, theIndispensablePais):        
        self.paiqiang = thePaiqiang
        self.keyRival = theKeyRival
        self.keyRivalPais = (TotalPais - thePaiqiang) * (theKeyRival / 4)
        self.oneRivalPais = (TotalPais - thePaiqiang) / 4
        self.effectivePais = self.keyRivalPais + thePaiqiang
        if theAvailablePais >  thePaiqiang:
            self.availablePais = thePaiqiang
        else:
            self.availablePais = theAvailablePais
        if theIndispensablePais > theAvailablePais:
            self.indispensablePais = theAvailablePais
        else:
            self.indispensablePais = theIndispensablePais
        assert self.effectivePais >= self.keyRivalPais, "Wrong parameter"
        assert self.effectivePais >= self.availablePais, "Wrong parameter"
        assert self.availablePais >= self.indispensablePais, "Wrong parameter"
    def Print(self):
        print("paiqiang            = {0}".format(self.paiqiang))
        print("keyRival            = {0}".format(self.keyRival))
        print("keyRivalPais        = {0}".format(self.keyRivalPais))
        print("oneRivalPais        = {0}".format(self.oneRivalPais))
        print("effectivePais       = {0}".format(self.effectivePais))
        print("availablePais       = {0}".format(self.availablePais))
        print("indispensablePais = {0}".format(self.indispensablePais))

#Caution: CalcCombNumber(0, x) = 1, CalcCombNumber(2, 1) = 0
def CalcCombNumber(members, total):
    members = round(members)
    total   = round(total)
    combinations = reduce(lambda x,y:x*y, range(total+1-members, total+1), 1) \
        / reduce(lambda x,y:x*y, range(1, members + 1), 1)
    return combinations

#get the rate of "the keyRival has exactly indispensablePais pais of availablePais" 
#has been get by KeyRivals, 
#caustion,  when paisDist.keyRivalPais is float,  this function is not too accurate,
#we should use CalcRateOfAvailablePaisInRivals2(), this function is just for debuging.
#if you dont want CalcRateOfAvailablePaisInRivals2(), please make sure rivalPais
#is integer
def CalcRateOfAvailablePaisInRivals1(paisDist, doCalculateOnlyOneRival, isExacltly):
    if doCalculateOnlyOneRival:
        rivalPais = paisDist.oneRivalPais
    else:
        rivalPais = paisDist.keyRivalPais
    combTotal = CalcCombNumber(rivalPais, paisDist.effectivePais);    
    if isExacltly:
        combOk  = CalcCombNumber(paisDist.indispensablePais, paisDist.availablePais) 
        combOk *= CalcCombNumber(rivalPais - paisDist.indispensablePais, 
                                 paisDist.effectivePais - paisDist.availablePais)
    else:
        combOk = 0
        loopEnd = min(rivalPais, paisDist.availablePais)
        for i in range(paisDist.indispensablePais, loopEnd + 1):
            combOk += CalcCombNumber(i, paisDist.availablePais) * \
                      CalcCombNumber(rivalPais - i, 
                                     paisDist.effectivePais - paisDist.availablePais) 
    #print(combTotal, combOk)
    rate = combOk / combTotal
    return rate

def CalcRateOfAvailablePaisInRivals2(paisDist, doCalculateOnlyOneRival, isExacltly):
    paisDist = copy.copy(paisDist)
    if doCalculateOnlyOneRival:
        rivalPais = paisDist.oneRivalPais
    else:
        rivalPais = paisDist.keyRivalPais
        
    rate = 0
    if isExacltly:
        rate1 = 1.0
        rate2 = 1.0
        superfluous = paisDist.availablePais - paisDist.indispensablePais
        combinations = CalcCombNumber(superfluous, paisDist.availablePais)
        for i in range(1, superfluous + 1):
            rate1 *= (paisDist.effectivePais - rivalPais)/paisDist.effectivePais
            paisDist.effectivePais -= 1
        for i in range(1, paisDist.indispensablePais + 1):
            rate2 *= rivalPais / paisDist.effectivePais
            rivalPais -= 1
            paisDist.effectivePais -= 1
        rate = rate1 * rate2 * combinations
        #print("1:", rate, rate1, rate2, combinations)
    else:
        for i in range(paisDist.indispensablePais, paisDist.availablePais + 1):
            paisDist.indispensablePais = i
            rate += CalcRateOfAvailablePaisInRivals2(paisDist, doCalculateOnlyOneRival, True)
            
    #print("4:", rate)
    return rate
    
def CalcRateOfAvailablePaisInRivals(paisDist, doCalculateOnlyOneRival, isExacltly):
    rate2 = CalcRateOfAvailablePaisInRivals2(paisDist, doCalculateOnlyOneRival, isExacltly);
    if DebugPaisInRivalRate:
        rate1 = CalcRateOfAvailablePaisInRivals1(paisDist, doCalculateOnlyOneRival, isExacltly);
        assert abs(rate1 - rate2) < 0.001,  "bug, rate1={0:.2f}, rate2={1:.2f}.".format(rate1,rate2)
    return rate2

#########################################################################################

#### About pai you needed, for example 2 Wang, left behind in Paiqiang ####
#Assume you have {1,3} Wang, {4,5} Tong.  How to get the rate of 2 Wang or {3,6} Tong to te 
#left in the Paiqiang?
def PrintRateOfAvailablePaisInPaiqiang():
    #conditions: [(KeyRivalNumber, PaiqiangNumber, AvailablePaisNumber)]
    conditions = [(3, 12, 1), (2, 12, 1), (1, 12, 1)]
    print("You have {1,3} Tong, x raivals need Tong, ",
          "what's the rate of any of 2 Tong exists in Paiqiang?")
    print("KeyRivalNum", "PaiqiangNum", "RateOfOne")
    for x,y,z in conditions:
        paisDist = PaisDistribution(y, x, z, z)
        #paisDist.Print()
        rate = 1-CalcRateOfAvailablePaisInRivals(paisDist, False, True)
        print("{0:11d}{1:12d}{2:10.2f}".format(x, y, rate))

print("----")
PrintRateOfAvailablePaisInPaiqiang()

#### The rate you may DianGang when you abandon one Pai ####
#Assume you have one 9 Tong and no 9 Tong was abandon by others, what's the rate
#you will DianGang when you abandon 9 Tong?
def CalcDianGangRate(keyRivalNum, paiqiangNum):
    """
    Calculate the rate of DianGang.
    keyRivalNum: The rival number who needs this kind of Pai(for example who need Tong), 
                 3 >= keyRivalNum >= 1.
    paiqiangNum: number of pais left behind in Paiqiang.
    """
    paisDist = PaisDistribution(paiqiangNum, keyRivalNum, 3, 3)
    #paisDist.Print()
    rate = CalcRateOfAvailablePaisInRivals(paisDist, True, True) * keyRivalNum
    return rate
    
def CalcRivalPengPaiRate(keyRivalNum, paiqiangNum):
    paisDist = PaisDistribution(paiqiangNum, keyRivalNum, 3, 2)
    #paisDist.Print()
    rate = CalcRateOfAvailablePaisInRivals(paisDist, True, False) * keyRivalNum
    return rate
    
def PrintGangAndPengRate():
    condition = [(1, 16), (1, 12), (1, 8), (1, 4)]
    print("You and x rivals need Tong, nobody abandon 9 Tong before, ",
          "what is the rate of DianGang when you abandon 9 Tong?")
    print("KeyRivalNum", "PaiqiangNum", "keyRivalPais", "  GangRate", "   PengRate")    
    for keyRival, paiqiang in condition:
        paisDist = PaisDistribution(paiqiang, keyRival, 0, 0)
        rateOfGang = CalcDianGangRate(keyRival,paiqiang)
        rateOfPeng = CalcRivalPengPaiRate(keyRival,paiqiang)
        print("{0:11d}{1:12d}{2:12.2f}{3:12.2f}{4:12.2f}".format(keyRival, paiqiang, paisDist.keyRivalPais, rateOfGang, rateOfPeng))

print("----")
PrintGangAndPengRate()

#no other rival needs Tong,  you have {1,3,7} Tong,  {2,5,66,8,9} in Paiqiang,  
#You can wait for 2 Tong,  or wait for two of 56689 Tong.  whether you should
#abandon 1,3 Tong and waiting for two of 56689 Tong?
def PrintSelectPais():
    rivals = 4
    print("Case 1, host {1,3,7}, Paiqiang {2,5,6,6,8,9}")
    print("Rate of receiving only 2 Tong: {0:.2f}".format(1/4))
    print("Rate of receiving 56|68|89   : {0:.2f}".format(1/4 * 7/16 + 7/16 * 1/4 + 1/4 * 1/4))
    
print("----")
PrintSelectPais()

#your pais {33444677}, you can get a Jiao of {58} if you abandon 7. pais abandoned by 
#others {455568889999},  if and only if your rival has {56678 or 56778} you and rival are dead. 
#what's the rate of one rival has the {56678 or 56778}?  That is {58} + 3 of {6677}?    
def PrintRateRivalGetPartOfPais():
    keyRivals = 1
    paiqiang  = 12
    paisDist = PaisDistribution(paiqiang, keyRivals, 0, 0)
    print("What's the rate of your rivals has X-Number pais from total AvailabePais?")
    print("KeyRvial={0}, PaiqiangNum={1}, keyRivalPais={2}".format(keyRivals, paiqiang, paisDist.keyRivalPais))
    print("PaisInRival", "AvailabePais", "   Rate")
    
    conditions = [(1, 1), (0, 2), (1, 2), (2, 2), (0, 3), (1, 3), (2, 3), (3, 3), (2, 4), (3, 4), (4, 4)]
    for x,y in conditions:
        paisDist = PaisDistribution(paiqiang, keyRivals, y, x)
        #paisDist.Print()
        rate = CalcRateOfAvailablePaisInRivals(paisDist, True, True)
        print("{0:10d}{1:14d}{2:8.2f}".format(x, y, rate))

print("----")
PrintRateRivalGetPartOfPais()

#jiaoCombination: list of PaisDistribution
def CalcRateRivalHasSpecificJiao(jiaoList):
    rate = 0.0
    for jiao in jiaoList:
        singleJiaoRate = 1.0
        for paisDist in jiao:
            singleJiaoRate *= CalcRateOfAvailablePaisInRivals(paisDist, True, True) * paisDist.keyRival
        rate += singleJiaoRate
    return rate
    
def PrintRateRivalHasSpecificJiao():
    print("Assume host and one rival need Wan. ")
    print("If 56778 Wan are unknown, what's the relative posibility the rival Hu one spcific Pai?")
    print("If rival hu 6 Wan, then rival's pai may be {5, 7} or {7, 8}")
    print("If rival hu 7 Wan, then rival's pai may be {5, 6} or {6, 8}",
          "or {7, 7} or {7} or {5,6,7,7} or {6,7,7,8}")
    #rateJiao6: rate of 57 or 78
    rawJiaoCombs    = [[(1,1), (1,2), (0,2)], [(1,2), (1,1), (0,2)]]
    jiaoList = []
    for jiao in rawJiaoCombs:
        curJiao = []
        for x, y in jiao:
            paisDist = PaisDistribution(16, 1, y, x)
            curJiao.append(paisDist)
        jiaoList.append(curJiao)
    rate = CalcRateRivalHasSpecificJiao(jiaoList)
    print("Rate of Jiao 6 Wan: {0:.2f}".format(rate))
    
    #rate of 56 or 68 or 7 or 77 or 5677 or 6778
    rawJiaoCombs = [[(2,2), (0,3)], [(2,2), (0,3)], [(1,2), (0,4)],
                    [(2,2), (0,3)], [(4,4), (0,1)], [(4,4), (0,1)]]
    jiaoList = []
    for jiao in rawJiaoCombs:
        curJiao = []
        for x, y in jiao:
            paisDist = PaisDistribution(16, 1, y, x)
            curJiao.append(paisDist)
        jiaoList.append(curJiao)
    rate = CalcRateRivalHasSpecificJiao(jiaoList)
    print("Rate of Jiao 7 Wan: {0:.2f}".format(rate))
      
print("----")
PrintRateRivalHasSpecificJiao()

class XiajiaoCondition:
    """
    theWinner:  the rival who Hupai before host Xiajiao.
    self.hostPais:  the pais number that host maybe get from paiqiang between 
                    current point and theCheckPoint
    """
    def __init__(self, thePaiqiang, theAvailablePais, theIndispensablePais, theCheckPoint, theWinner):        
        self.paiqiang = thePaiqiang
        if theAvailablePais >  thePaiqiang:
            self.availablePais = thePaiqiang
        else:
            self.availablePais = theAvailablePais
        self.indispensablePais = theIndispensablePais
        self.checkPoint = theCheckPoint
        self.hostPais = 0
        for i in range(0, theWinner+1):
            self.hostPais += (thePaiqiang - theCheckPoint) / (theWinner + 1) / (4 - i)
        assert self.paiqiang >= self.checkPoint, "Wrong parameter"
        assert self.paiqiang >= self.availablePais, "Wrong parameter"
        assert self.indispensablePais <= self.availablePais, "Wrong parameter"
        assert self.indispensablePais <= self.hostPais , "Wrong parameter"

#32 pias(y pais is available) in Paiqiang,  what's the rate host get x pais at the 
#points 4 pais left in Paiqiang
def CalcRateOfXiajiao1(condition):
    combTotal = CalcCombNumber(condition.hostPais, condition.paiqiang); 
    combOk = 0
    loopEnd = min(round(condition.hostPais), condition.availablePais)
    for i in range(condition.indispensablePais, loopEnd + 1):
        if condition.hostPais < i:
            break
        combOk += CalcCombNumber(i, condition.availablePais) * \
                  CalcCombNumber(condition.hostPais - i, 
                                 condition.paiqiang - condition.availablePais)
    rate = combOk / combTotal
    return rate

def CalcRateOfXiajiao2(condition, isExacltly = False):
    condition = copy.copy(condition)
    if isExacltly:
        rate1 = 1.0
        rate2 = 1.0
        superfluous = condition.availablePais - condition.indispensablePais
        for i in range(1, superfluous + 1):
            rate1 *= (condition.paiqiang - condition.hostPais) / condition.paiqiang
            condition.paiqiang -= 1
        rate1 *= CalcCombNumber(superfluous, condition.availablePais)
        for i in range(1, condition.indispensablePais + 1):
            rate2 *= condition.hostPais / condition.paiqiang
            condition.hostPais -= 1
            condition.paiqiang -= 1
        #print("1:", rate1, rate2)
        rate = rate1 * rate2
    else:
        rate = 0
        for i in range(condition.indispensablePais, condition.availablePais + 1):
            condition.indispensablePais = i
            rate += CalcRateOfXiajiao2(condition, True)            
    #print("4:", rate)
    return rate

def CalcRateOfXiajiao(condition):
    rate2 = CalcRateOfXiajiao2(condition)
    if DebugHostXiajiaoRate:
        rate1 = CalcRateOfXiajiao1(condition)
        assert abs(rate1 - rate2) < 0.01,  "bug, rate1={0:.2f}, rate2={1:.2f}.".format(rate1,rate2)
    return rate2
    
def PrintRateOfXiajiao():
    conditions = [(3, 10), (4, 13), (5, 17)]
    paiqiang = 32
    checkPoint = 8
    print("{0} pias(y pais is available) in Paiqiang,  what's the rate host ".format(paiqiang),
          "get x pais at the points where {0} pais left in Paiqiang".format(checkPoint))
    print("Indispensable Available winner   Rate")
    for winner in range(0, 2 + 1):
        for indispensablePais,availablePais in conditions:
            condition = XiajiaoCondition(paiqiang, availablePais, indispensablePais, checkPoint, winner)
            rate = CalcRateOfXiajiao(condition)
            print("{0:13d} {1:9d} {2:6d}   {3:.2f}".format(indispensablePais, availablePais, winner, rate))
        print("-")

print("----")
PrintRateOfXiajiao()


DoNotHupai = 0
Zimo       = 1
Dianpao    = 2

# Host Hupai history.
# (left rivals when host Hupai, Paiqiang when Hupai, Fan, DoNotHupai or Zimo or Dianpao)
huLostInPoints1 = \
[
    (2, 30, 0, Zimo), (2, 26, 0, Dianpao), (2, 20, 0, Dianpao), (3, 26, 0, Zimo), (2, 10, 0, Dianpao),       #1-5
    (2, 21, 0, Dianpao), (2, 12, 0, Zimo), (1, 10, 1, Dianpao), (1, 1, 0, Dianpao), (0, 0, 2, DoNotHupai),   #6-10    
    (0, 0, 2, DoNotHupai), (1, 20, 0, Dianpao), (3, 6, 0, Dianpao), (1, 1, 0, Dianpao), (1, 19, 0, Zimo),    #11-15
    (1, 18, 0, Dianpao), (2, 29, 1, Zimo), (0, 0, 1, DoNotHupai), (0, 0, 0, DoNotHupai), (1, 28, 0, Zimo),   #16-20
    (1, 3, 1, Zimo), (3, 18, 0, Zimo), (1, 37, 3, Dianpao), (1, 7, 1, Zimo), (2, 20, 0, Dianpao),            #21-25
    (2, 16, 2, Dianpao), (3, 23, 1, Zimo), (2, 32, 0, Zimo), (0, 0, 4, DoNotHupai), (0, 0, 3, DoNotHupai),   #26-30
]

huLostInPoints2 = \
[
    (3, 26, 0, Zimo), (1, 10, 2, Zimo), (3, 26, 1, Zimo), (0, 15, 3, DoNotHupai), (3, 18, 0, Dianpao),        #1-5
    (1, 5, 0, Zimo), (3, 25, 2, Zimo), (2, 17, 1, Dianpao), (1, 7, 0, Dianpao), (2, 8, 1, Zimo),              #6-10    
    (2, 11, 1, Zimo), (0, 0, 1, DoNotHupai), (1, 21, 0, Dianpao), (1, 10, 0, Dianpao), (1, 5, 1, Dianpao),    #11-15
    (3, 21, 0, Dianpao), (1, 5, 1, Zimo), (3, 35, 0, Zimo), (2, 5, 0, Zimo), (0, 8, 2, DoNotHupai),           #16-20
    (3, 31, 0, Dianpao), (1, 2, 2, Zimo), (0, 5, 2, DoNotHupai), (2, 30, 0, Dianpao), (0, 7, 0, DoNotHupai),  #21-25
    (2, 3, 1, Zimo), (3, 28, 1, Zimo), (0, 3, 0, DoNotHupai), (0, 18, 1, DoNotHupai), (1, 27, 0, Dianpao),    #26-30
]

# huLostInPoints3 is more accurate thanhuLostInPoints1, huLostInPoints2
huLostInPoints3 = \
[
    (3, 35, 3, Dianpao), (3, 7, 0, Zimo), (0, 2, 0, DoNotHupai), (3, 18, 3, Zimo), (0, 0, 1, DoNotHupai),  #1-5
    (2, 9, 0, Dianpao), (2, 11, 1, Zimo), (1, 7, 2, Dianpao), (3, 15, 3, Zimo), (2, 26, 0, Zimo),              #6-10    
    (2, 6, 0, Dianpao), (0, 3, 0, DoNotHupai), (1, 23, 1, Dianpao), (1, 21, 2, Zimo), (3, 42, 0, Zimo),       #11-15
    (2, 0, 0, DoNotHupai), (3, 17, 1, Dianpao), (2, 5, 1, Dianpao), (3, 25, 3, Dianpao), (3, 7, 0, Dianpao),  #16-20
    (1, 20, 0, Dianpao), (0, 0, 3, DoNotHupai), (0, 0, 3, DoNotHupai), (2, 18, 0, Dianpao), (0, 13, 0, DoNotHupai),  #21-25
    (1, 7, 3, Dianpao), (2, 6, 1, Dianpao), (0, 13, 2, DoNotHupai), (3, 15, 0, Dianpao), (0, 0, 1, DoNotHupai),  #26-30
    (0, 0, 0, DoNotHupai), (3, 29, 0, Dianpao), (2, 10, 0, Zimo), (2, 6, 3, Dianpao), (1, 0, 1, Zimo),  #31-35
    (3, 26, 0, Dianpao), (2, 0, 1, Dianpao), (3, 18, 0, Zimo), (3, 22, 0, Dianpao), (3, 20, 0, Dianpao),  #36-40
    (2, 12, 2, Zimo), (0, 15, 0, DoNotHupai), (2, 25, 1, Zimo), (3, 16, 0, Dianpao), (0, 0, 3, DoNotHupai),  #41-45
    (0, 11, 0, DoNotHupai), (0, 0, 3, DoNotHupai), (2, 20, 0, Dianpao), (3, 18, 0, Zimo), (1, 19, 0, Dianpao),  #46-50
]

def CalcLostOfRivalHupai(begin, end):
    baseRule = BaseRule()
    rounds = 0
    lost = 0
    histData = [huLostInPoints1, huLostInPoints2, huLostInPoints3]
    for huLostInPoints in histData:
        rounds += len(huLostInPoints)
        for leftRivals, paiqiang, fan, type in huLostInPoints:
            if paiqiang < begin or paiqiang >= end:  #[begin, end)
                continue
            if type == Zimo:
                lost += baseRule.GetZimoUnitPrice(fan)
            if type == Dianpao:
                lost += baseRule.GetDianpaoPrice(fan) / leftRivals
    
    lost = lost * 3 / rounds
    return lost

def PrintLostOfRivalHupai():
    TypeName = ["NotHupai", "Zimo", "Dianpao"]
    print("Index LeftRival Paiqiang Fan Type(0N, 1Z, 2D)")
    index = 1
    histData = [huLostInPoints1, huLostInPoints2, huLostInPoints3]
    for huLostInPoints in histData:
        for leftRivals, paiqiang, fan, type in huLostInPoints:
            print("{0:5d}".format(index), 
                  "{0:9d} {1:8d} {2:3d} {3:s}".format(leftRivals, paiqiang, fan, TypeName[type]))
            index += 1
    area = [(0, 32), (4, 32), (8, 32), (16, 32)]
    print("If host didn't Hupai in area [begin, end), how much host will lost?")
    for begin, end in area:
        lost = CalcLostOfRivalHupai(begin, end)
        print("[begin {0:2d}, end {1:2d}), lost = {2:.2f}".format(begin, end, lost))

print("----")
PrintLostOfRivalHupai()

    
#### Calculate Zimo rate, if nobody else Hu before you (no Jiao) ... ####
def PrintPowConst():
    print("Zimo rate, if nobody else Hu before you (no Jiao).")
    for i in range(1, 5):
        print("1 - (3/4)**{0:1d} = {1:4.2f}".format(i, 1-(3/4)**i))
    for i in range(1, 5):
        print("1 - (2/3)**{0:1d} = {1:4.2f}".format(i, 1-(2/3)**i))

print("----")
PrintPowConst()

#### How many Pais you must abandon to get a Jiao 
#### (start count 1 when you abadon one Pais which you can keep in hand...
#We get the following data from QQ Majiang. 
paisAbandonedForJiao = [4, 2, 4, 7, 4, 2, 8, 2, 2, 3, 2, 5, 1, 2, 4, 1, 6, 7, 3]
def PrintPaisAbandonedForJiao():
    pais = 0
    for i in paisAbandonedForJiao:
        pais = pais + i
    print("How many pais you should abandon for jiao? ")
    print("Note: We start to count 1 when you abadon one Tong or Tiao and you need Tong and Tiao, ",
          "And once we started the count, every Pais is counted, that is Wan is counted in. ")
    print("The abandoned Pais are:{0:.2f}".format(pais / len(paisAbandonedForJiao)))

print("----")
PrintPaisAbandonedForJiao()

#### The reason the last player could never Hu. We count the percent when the last one   
#### has no Jiao or his Jiao has been received by others.  Here "last one" means the 
#### player never Hu and the other 2 player has Hu.
#We get the following data from QQ Majiang. The first field means there still has Pais 
#the last Player can Hu. The second field means the last player has no Jiao or there is 
#no Pai of his Jiao in Paiqiang.
deadRateWhen3Winer = [(10, 20)] #[(rounds of availablePai != 0, rounds of availablePai == 0)...]
def GetDeadReason():
    countX = 0
    countY = 0
    for x,y in deadRateWhen3Winer:
        countX = countX + x
        countY = countY + y
    rate = countY / (countX+countY)
    return rate

#### Hu time area. When the first, second and third one Hu? Here are some real statistics, the 
#### first number is the Pais number of Paiqiang when first winner Hu.  And the second number  
#### is for second winner.  If there is zero,  that means there is no winner Hu, they complete 
#### this round of game till all Pais in Paiqiang are consumed. for example: {28, 10, 0},  the 
#### first one Hu when there were 28 Pais in Paiqiang, and the second winner Hu When there were 
#### 10 Pais in Paiqiang, While the other player never Hu untill there is no Pais in Paiqiang.
histHuPoints = [
    # Day 1
    (28, 17, 9), (24, 0, 0), (36, 5, 0), (4, 3, 0), (28, 15, 14), (14, 6, 4), (27, 13, 0), 
    (29, 9, 0), (16, 14, 10), (29, 28, 27), (14, 0, 0), (24, 16, 16), (20, 15, 14),
    # Day 2
    (24, 18, 0), (23, 0, 0), (22, 7, 1), (32, 28, 6), (28, 8, 7), (24, 14, 13), (30, 18, 8), 
    (23, 10, 8), (2, 0, 0), (31, 19, 10), (32, 20, 8), (0, 0, 0), (16, 12, 10), (10, 8, 0), 
    (15, 4, 1), (34, 31, 22), (2, 0, 0), (43, 14, 11), (30, 12, 8), (20, 13, 4),
    # Day 3
    (15, 13, 12), (13, 1, 0), (21, 1, 0), (17, 12, 11), (33, 3, 0), (21, 15, 3), (17, 1, 0), 
    (19, 17, 4), (23, 5, 0), (6, 2, 0),(7, 0, 0)]

def CalcHuPointsKey(point):
    key = point[0]*10000 + point[1]*100 + point[2]
    return key

def PrintHuAreaRawData():
    sortedHistHuPoints = histHuPoints.copy()
    sortedHistHuPoints.sort(key=CalcHuPointsKey)
    for x, y, z in sortedHistHuPoints:
        print("{0:3d}, {1:3d}, {2:3d}".format(x,y,z))
    
def PrintAverageTimePoint():
    winner1 = 0
    zero1st = 0
    winner2 = 0
    zero2nd = 0
    winner3 = 0
    zero3rd = 0
    for x, y, z in histHuPoints:
        winner1 = winner1 + x
        winner2 = winner2 + y
        winner3 = winner3 + z
        if (x == 0):
            zero1st = zero1st + 1
        if (y == 0):
            zero2nd = zero2nd + 1
        if (z == 0):
            zero3rd = zero3rd + 1
    rounds = len(histHuPoints)
    print("Average HupaiTime(When the 1st, 2nd, 3rd winner Hu):")
    print("    1st = {0:.2f}".format(winner1 / rounds))
    print("    2nd = {0:.2f}".format(winner2 / rounds))
    print("    3rd = {0:.2f}".format(winner3 / rounds))
    print("Dead player anylasis.(Total", rounds, "rounds)")
    print("    1st column zero:", zero1st)
    print("    2nd column zero:", zero2nd)
    print("    3rd column zero:", zero3rd)
    zero4th = rounds
    rateOfNoPaiDead = GetDeadReason()
    rivalRate = (1-rateOfNoPaiDead)/2
    hostRate  = 1 - (1-rateOfNoPaiDead)/2
    print("    4th column zero: {0:d}, ".format(zero4th), 
          "{0:.2f} of them are No Pai or No Jiao,".format(rateOfNoPaiDead),
          "when 2 player has gone and host has a definitive pai, "
          "rival's Hu rate = {0:.2f}, host's Hu rate = {1:.2f}".format(rivalRate, hostRate))

def IsBetween(low, high, value):
    if value >= low and value <= high:
        return 1
    return 0
          
def PrintHuAreaDistribution():
    area0to0   = 0   #2 or more player never Hu.
    area1to4  = 0
    area1to10  = 0
    area11to20 = 0
    area21to30 = 0
    area31to54 = 0
    for x, y, z in histHuPoints:
        area0to0 += IsBetween(0, 0, x)
        area0to0 += IsBetween(0, 0, y)
        area0to0 += IsBetween(0, 0, z)
        area1to4 += IsBetween(1, 4, x)
        area1to4 += IsBetween(1, 4, y)
        area1to4 += IsBetween(1, 4, z)        
        area1to10 += IsBetween(1, 10, x)
        area1to10 += IsBetween(1, 10, y)
        area1to10 += IsBetween(1, 10, z)
        area11to20 += IsBetween(11, 20, x)
        area11to20 += IsBetween(11, 20, y)
        area11to20 += IsBetween(11, 20, z)
        area21to30 += IsBetween(21, 30, x)
        area21to30 += IsBetween(21, 30, y)
        area21to30 += IsBetween(21, 30, z)
        area31to54 += IsBetween(31, 54, x)
        area31to54 += IsBetween(31, 54, y)
        area31to54 += IsBetween(31, 54, z)

    rounds = len(histHuPoints)
    print("Hupai Area Statistic:")
    print("    Area 0  ~ 0 : {0:3d}, {1:.2f}".format(area0to0,   area0to0  / (rounds * 4)))
    print("    Area 1  ~ 4 : {0:3d}, {1:.2f}".format(area1to4,  area1to4 / (rounds * 4)))
    print("    Area 1  ~ 10: {0:3d}, {1:.2f}".format(area1to10,  area1to10 / (rounds * 4)))
    print("    Area 11 ~ 20: {0:3d}, {1:.2f}".format(area11to20, area11to20 / (rounds * 4)))
    print("    Area 21 ~ 30: {0:3d}, {1:.2f}".format(area21to30, area21to30 / (rounds * 4)))
    print("    Area 31 ~ 54: {0:3d}, {1:.2f}".format(area31to54, area31to54 / (rounds * 4)))

print("----")
PrintHuAreaRawData()
PrintAverageTimePoint()
PrintHuAreaDistribution()

#possiblePaiNumber: If one of you Jiao (for example 9 Tong) is in Paiqiang and someone else
#   receives Tong, the 9 Tong is a Possible-Pai, Possible-Pai-Number is the total number of 
#   your Possible-Pai. In order to simpfy the calculation,  we assume that the Possible-Pai
#   never be abandoned by other player who get it from Paiqiang.
#   
class Host:
    def __init__(self, theDefinitivePaiNumber, thePossiblePaiNumber, theFanNumber):
        self.definitivePaiNumber = theDefinitivePaiNumber
        self.possiblePaiNumber = thePossiblePaiNumber
        self.fanNumber = theFanNumber

class Rival:
    def __init__(self, theDefinitivePaiNumber, theFanNumber):
        self.definitivePaiNumber = theDefinitivePaiNumber
        self.fanNumber = theFanNumber

#### What's your Pai value?  
###  We calculate your Pai's value based on you Definitive-Pai-Number and Fans.
#### host:  class Host
#### rivals:  list<class Rival>
def HostFistZimoRate(host, rivals):
    playerNumber = len(rivals) + 1
    rivalPaiTotal = 0
    for rival in rivals:
        rivalPaiTotal += rival.definitivePaiNumber
    totalDefinitivePaiNumber = host.definitivePaiNumber + rivalPaiTotal
    totalPaiNumber   = host.possiblePaiNumber + totalDefinitivePaiNumber
    #get the rate host Hupai by obtain one of possible pai(definitive pai is not included).
    rateHostZimoPossilbe = 0.0
    for i in range(1, round(host.possiblePaiNumber + 1)):
        rateHostZimoPossilbe += (1 - rateHostZimoPossilbe) / (totalPaiNumber - i) / playerNumber 
    rate = rateHostZimoPossilbe
    if totalDefinitivePaiNumber != 0:
        rate = host.definitivePaiNumber / totalDefinitivePaiNumber / playerNumber
        rate = rateHostZimoPossilbe + (1-rateHostZimoPossilbe) * rate
    return rate

#### Definitive-Pai-Number:  Refer to CalHostPaiValue()
#### Possible-Pai-Number  :  Refer to CalHostPaiValue()
#### rivals:  list<struct {int fanNumber, float paiNumber}>
def HostFistRcvDianpaoRate(host, rivals):
    playerNumber = len(rivals) + 1
    totalPaiNumber = host.definitivePaiNumber 
    for rival in rivals:
        totalPaiNumber += rival.definitivePaiNumber
    rate = 0.0
    if totalPaiNumber != 0:
        rate = host.definitivePaiNumber / totalPaiNumber * (playerNumber - 1) / playerNumber;
    return rate

def HostFirstHupaiRate(host, rivals):
    rate = HostFistZimoRate(host, rivals) + HostFistRcvDianpaoRate(host, rivals)
    return rate

####  value = rate of first Hupai * income
def EstimateHostFirstHupaiValue(host, rivals):
    baseRule = BaseRule()
    receivePaoIncome = baseRule.GetDianpaoPrice(host.fanNumber)
    firstRcvDianpaoRate = HostFistRcvDianpaoRate(host, rivals)
    zimoIncome = baseRule.GetZimoIncome(len(rivals), host.fanNumber)
    firstZimoRate = HostFistZimoRate(host, rivals)
    value = receivePaoIncome * firstRcvDianpaoRate + zimoIncome * firstZimoRate;
    return value;

### Calculate theRival's rate to Zimo Hu, while all other play may Zimo or receive Dianpao.        
def RivalFistZimoRate(host, theRival, rivals):
    playerNumber = len(rivals) + 1
    rivalPaiTotal = 0
    for rival in rivals:
        rivalPaiTotal += rival.definitivePaiNumber
    totalDefinitivePaiNumber = host.definitivePaiNumber + rivalPaiTotal
    totalPaiNumber   = host.possiblePaiNumber + totalDefinitivePaiNumber
    #get the rate host Hupai by obtain one of possible pai(definitive pai is not included).
    rateHostZimoPossilbe = 0.0
    for i in range(1, round(host.possiblePaiNumber + 1)):
        rateHostZimoPossilbe += (1 - rateHostZimoPossilbe) / (totalPaiNumber - i) / playerNumber     
    rate = 0.0
    if theRival.definitivePaiNumber > 0.01:
        rate = (1-rateHostZimoPossilbe) * theRival.definitivePaiNumber \
               / totalDefinitivePaiNumber / playerNumber
    return rate
    
def RivalFistRcvDianpaoByHostRate(host, theRival, rivals):
    playerNumber = len(rivals) + 1
    rivalPaiTotal = 0
    for rival in rivals:
        rivalPaiTotal += rival.definitivePaiNumber
    totalDefinitivePaiNumber = host.definitivePaiNumber + rivalPaiTotal
    totalPaiNumber   = host.possiblePaiNumber + totalDefinitivePaiNumber
    #get the rate host Hupai by obtain one of possible pai(definitive pai is not included).
    rateHostZimoPossilbe = 0.0
    for i in range(1, round(host.possiblePaiNumber + 1)):
        rateHostZimoPossilbe += (1 - rateHostZimoPossilbe) / (totalPaiNumber - i) / playerNumber
    rate = 0.0
    if theRival.definitivePaiNumber > 0.01:
        rate = (1-rateHostZimoPossilbe) * theRival.definitivePaiNumber / totalDefinitivePaiNumber
        rate = rate / playerNumber
    return rate

def RivalFistRcvDianpaoByAnyoneRate(host, theRival, rivals):
    playerNumber = len(rivals) + 1
    rivalPaiTotal = 0
    for rival in rivals:
        rivalPaiTotal += rival.definitivePaiNumber
    totalDefinitivePaiNumber = host.definitivePaiNumber + rivalPaiTotal
    totalPaiNumber   = host.possiblePaiNumber + totalDefinitivePaiNumber
    #get the rate host Hupai by obtain one of possible pai(definitive pai is not included).
    rateHostZimoPossilbe = 0.0
    for i in range(1, round(host.possiblePaiNumber + 1)):
        rateHostZimoPossilbe += (1 - rateHostZimoPossilbe) / (totalPaiNumber - i) / playerNumber
    rate = 0.0
    if theRival.definitivePaiNumber > 0.01:
        rate = (1-rateHostZimoPossilbe) * theRival.definitivePaiNumber / totalDefinitivePaiNumber
        rate = rate * (playerNumber-1) / playerNumber
    return rate

def RivalFirstHupaiRate(host, theRival, rivals):
    rate  = RivalFistZimoRate(host, theRival, rivals) 
    rate += RivalFistRcvDianpaoByAnyoneRate(host, theRival, rivals)
    return rate

def EstimateRivalFistHupaiValue(host, rivals):
    baseRule = BaseRule()
    value = 0.0
    for rival in rivals:
        rivalZimoRate = RivalFistZimoRate(host, rival, rivals)
        hostDianpaoRate = RivalFistRcvDianpaoByHostRate(host, rival, rivals)
        value += baseRule.GetZimoUnitPrice(rival.fanNumber) * rivalZimoRate
        value += baseRule.GetDianpaoPrice(rival.fanNumber) * hostDianpaoRate
    return value

def EstimateHostOneRoundPaiValue(host, rivals):
    hostValue   = EstimateHostFirstHupaiValue(host, rivals)
    rivalsValue = EstimateRivalFistHupaiValue(host, rivals)
    return hostValue - rivalsValue

#### Definitive-Pai-Number:  If one of you Jiao (for example 9 Tong) is in Paiqiang and nobody  
####       else receive Tong, the 9 Tong is a Definitive-Pai, Definitive-Pai-Number is the 
####       total number of your Definitive-Pai.
#### Possible-Pai-Number  :  If one of you Jiao (for example 9 Tong) is in Paiqiang and someone 
####       else receives Tong, the 9 Tong is a Possible-Pai, Possible-Pai-Number is the 
####       total number of your Possible-Pai.
#### Total-Pai-Number     :  Definitive-Pai-Number + Possible-Pai-Number 
#### Rival-Number         :  How many player except you has not gone (Hu) when we calculate your 
####       Pai's value.
def EstimateHostPaiValue(host, rivals):
    baseRule = BaseRule()
    value = 0.0
    if (len(rivals) < 2):
        value = EstimateHostOneRoundPaiValue(host, rivals)
        return value
    else:
        value = EstimateHostFirstHupaiValue(host, rivals)
    winners = []
    for rival in rivals:
        if (rival.definitivePaiNumber > 0):
            winners.append(rival)
    for rival in winners:
        rateRival = RivalFirstHupaiRate(host, rival, rivals)
        dianpaoLoss = baseRule.GetDianpaoPrice(rival.fanNumber) \
                      * RivalFistRcvDianpaoByHostRate(host, rival, rivals)
        zimoLoss    = baseRule.GetZimoUnitPrice(rival.fanNumber) \
                      * RivalFistZimoRate(host, rival, rivals)
        #host's lost when current winner Hu before host.
        currRoundLoss = dianpaoLoss + zimoLoss
        #after current winner Hu,  the other play continue the game.
        #assume that,  every time one rival gone,  the possilbe pais discrease 1/playerNumber
        host.possiblePaiNumber *= (len(rivals) - 1) / len(rivals)
        leftRivals = rivals.copy()
        leftRivals.remove(rival)
        nextRoundValue = EstimateHostPaiValue(host, leftRivals) * rateRival
        value = value - currRoundLoss + nextRoundValue 
    return value

def CreateRivalList(rivalsData):
    rivals=[]
    rival =()
    for x,y in rivalsData:
        rival = Rival(x, y)
        rivals.append(rival)
    return rivals

def RivalListToString(rivals):
    rivalsStr = "Players={0}".format(len(rivals)+1)
    for rival in rivals:
        rivalsStr += "; ({0}P,{1}F)".format(rival.definitivePaiNumber, rival.fanNumber)
    return rivalsStr

def PaiValueToString(paiNumber, paiValue, betMore):
    paiValueStr = "{0:3d}".format(paiNumber)
    for x,y in zip(paiValue, betMore):
        paiValueStr += " {0:8.2f}{1:s}".format(x, y)
    return paiValueStr

def GetRivalData(x):
    if x == 0:
        rivalsInfoGrps =  [[(0.33, 0), (1, 0)], [(0.33, 0), (2, 0)], 
                           [(0.33, 0), (1, 1)], [(0.33, 0), (2, 1)], 
                           [(0.33, 1), (1, 0)], [(0.33, 1), (2, 0)]]
    else:
        rivalsInfoGrps = [[(0.33, 0), (1, 0), (1, 0)], [(0.33, 0), (1, 0), (2, 0)], 
                          [(0.33, 0), (2, 0), (2, 0)], [(0.33, 0), (2, 0), (3, 0)], 
                          [(0.33, 0), (1, 1), (1, 0)], [(0.33, 0), (1, 1), (2, 0)], 
                          [(0.33, 0), (2, 1), (2, 0)], [(0.33, 0), (2, 1), (3, 0)], 
                          [(0.33, 0), (1, 1), (1, 1)], [(0.33, 0), (1, 1), (2, 1)], 
                          [(0.33, 0), (2, 1), (2, 1)], [(0.33, 0), (2, 1), (3, 1)],] 
    return rivalsInfoGrps

def PrintPaiValue():
    baseRule = BaseRule()
    rivalsInfoGrps = GetRivalData(1)
    for rivalsInfo in rivalsInfoGrps:
        rivals=CreateRivalList(rivalsInfo)
        print(RivalListToString(rivals))
        print("Pai    Value     Value     Value     Value     Value")
        print("       (0F){0}  (1F){1}  (2F){2}  (3F){3} (4F){4}".format(baseRule.GetDianpaoPrice(0),
              baseRule.GetDianpaoPrice(1), baseRule.GetDianpaoPrice(2), baseRule.GetDianpaoPrice(3), baseRule.GetDianpaoPrice(4)))
        prvValue = [0.0, 0.0, 0.0, 0.0, 0.0]
        curValue = [0.0, 0.0, 0.0, 0.0, 0.0]
        for pai in range(1,6):
            betMore = [" ", " ", " ", " ", " "]
            for fan in range(0,5):
                host = Host(pai, 0, fan)
                curValue[fan] = EstimateHostPaiValue(host, rivals)
                if prvValue[fan] >= baseRule.GetDianpaoPrice(fan):
                    betMore[fan] = "*"
            prvValue = curValue.copy()
            print(PaiValueToString(pai, curValue, betMore))
        print("")        

print("----")
PrintPaiValue()

