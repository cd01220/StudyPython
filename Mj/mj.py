#! /usr/bin/env python3.7

import copy
from functools import reduce

#define constant
TotalPais = 108.0
DebugPaisInRivalRate = True
DebugHostXiajiaoRate = False

def GetVersion():
    """
    In order to make Majiang algorithm more useful and easy to understand,
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
        fan = fan + 1 if fan < 4 else fan
        return self.baseWage * (2.0 ** fan)
        #return self.baseWage * (2.0 ** fan) + self.baseWage
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
    effectivePais: The pais number in which the available pais distribute
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
#caution,  when paisDist.keyRivalPais is float,  this function is not too accurate,
#we should use CalcRateOfAvailablePaisInRivals2(), this function is just for debugging.
#if you don't want CalcRateOfAvailablePaisInRivals2(), please make sure rivalPais
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
    condition = [(1, 20), (1, 16), (1, 12), (1, 8), (1, 4), (2, 20), (2, 12), (3, 20), (2, 12)]
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
        # 2 rival = [(x Pai, y Fan), (x Pai, y Fan)]
        rivalsInfoGrps =  [[(0.66, 0), (0.66, 0)], [(0.66, 0), (0.66, 1)],
                           [(0.66, 1), (0.66, 1)], [(0.66, 0), (0.66, 2)],
                           [(0.66, 1), (0.66, 2)], [(0.66, 2), (0.66, 2)]]
    else:
        # 2 rival = [(x Pai, y Fan), (x Pai, y Fan), (x Pai, y Fan)]
        rivalsInfoGrps = [[(0.66, 0), (0.66, 0), (0.66, 0)], [(0.66, 0), (0.66, 0), (0.66, 1)],
                          [(0.66, 0), (0.66, 1), (0.66, 1)], [(0.66, 1), (0.66, 1), (0.66, 1)],
                          [(0.66, 0), (0.66, 0), (0.66, 2)], [(0.66, 0), (0.66, 1), (0.66, 2)],
                          [(0.66, 1), (0.66, 1), (0.66, 2)], [(0.66, 1), (0.66, 2), (0.66, 2)],]
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

