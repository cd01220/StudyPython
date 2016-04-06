#! /usr/bin/env python3.3
# -*- coding: GB2312 -*-
import random
def GetRandomPais(paisNumber):
    allPais = []
    for i in range(1, 10):
        for j in range(0,4):
            allPais.append(i)
    hostPais = []
    for i in range(0, paisNumber):
        pai = random.choice(allPais)
        allPais.remove(pai)
        hostPais.append(pai)
    hostPais.sort()
    return hostPais

hostPais = GetRandomPais(14)
print(hostPais)