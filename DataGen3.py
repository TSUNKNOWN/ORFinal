#!/usr/bin/env python
# coding: utf-8

# In[7]:

import random
import numpy as np
import sys
import csv
import functools
import operator
from scipy.stats import expon
from pprint import pprint

Time = 300
PgrCnt = 10
Floor = 10
Speed = 5
Filename = None


# In[8]:

print('Usage: python DataGen.py Time MaxPeople Floor Speed [OutputFile]')
if 'y' in input('Default?(n/y)'):
    Filename = 'testoutput.csv'
elif len(sys.argv) == 1:
    Time = int(input('Time?'))
    PgrCnt = int(input('Number of Passenger?'))
    Floor = int(input('Floor?'))
    Speed = int(input('Speed?'))
elif len(sys.argv) >= 5:
    Time = int(sys.argv[1])
    PgrCnt = int(sys.argv[2])
    Floor = int(sys.argv[3])
    Speed = int(sys.argv[4])
    try:
        Filename = sys.argv[5]
    except:
        pass
elif sys.argv[1] == '-f':
    pass
else:
    # If conert to .py
    print('Invalid Arguments')
    exit(0)

Lambda = PgrCnt / Time

print(f'Time:{Time}')
print(f'N:{PgrCnt}')
print(f'H:{Floor}')
print(f'X:{Speed}')
print(f'Filename: {Filename}')
print(f'Frequency:{Lambda}')


# In[9]:


def getThreshold(interval, lbda=Lambda):
    # The probability that no people appear before interval
    return expon.pdf(interval*lbda)

def getTProb(args):
    return random.random()

# Not exactly probability, maybe some negative. But we only choose the maximum one, so forgive me plz.
def getAProb(args):
    aprobs = []
    for f in range(Floor):
        p = random.random() - getThreshold(args['Asinterval'][f])
        aprobs.append(p)
    return aprobs

def getDProb(args):
    dprobs = []
    a = args['a']
    for f in range(Floor):
        dprobs.append(random.random() - getThreshold(args['Dsinterval'][f]))
    # make sure the probability of same floor is minimum
    dprobs[a] = min(dprobs)-1
    return dprobs


# In[10]:


def getA(args):
    aprobs = getAProb(args)
    # a = aprobs.index(max(aprobs))
    a = 0
    args['Asinterval'][a] = 0
    args['a'] = a
    return a+1
def getD(args):
    dprobs = getDProb(args)
    d = dprobs.index(max(dprobs))
    args['Dsinterval'][d] = 0
    return d+1


# In[11]:


A = []
D = []
T = []
nowNum = 0
t = 0
interval = 0
args = {'time':t, 
        'Tsinterval':interval, 
        'Asinterval':[0 for _ in range(Floor)],
        'Dsinterval':[0 for _ in range(Floor)],
       'SumOfTInterval':0}
adTable = [[0 for j in range(Floor+1)] for i in range(Floor+1)]
adTable[0] = [i for i in range(Floor+1)]
for i in range(Floor+1):
    adTable[i][0] = i

tprob = getTProb(args)

while nowNum < PgrCnt :
    havePeople =  tprob > getThreshold(args['Tsinterval'])
    if havePeople:
        nowNum += 1
        tprob = getTProb(args)
        args['SumOfTInterval'] += args['Tsinterval']
        args['Tsinterval'] = 0 
        T.append(args['time'])
        a = getA(args)
        A.append(a)
        d = getD(args)
        D.append(d)
        adTable[a][d] += 1
    for f in range(Floor):
        args['Asinterval'][f] += 1
    for f in range(Floor):
        args['Dsinterval'][f] += 1
    args['Tsinterval'] += 1
    args['time'] = args['time'] + 1

if args['time'] > Time:
    print(f'Warning! Exceed expected time {Time} with t={args["time"]}')

print(f'The Last passenger arrived time: {args["time"]}')
print(f'Average arrived Interval: {args["SumOfTInterval"]/PgrCnt}')
# adTable[a][d] means # of passengers from a to d
print('From a to d scatter table:')
pprint(adTable)


# In[12]:


if Filename != None: 
    with open(Filename+'.csv', 'w') as f:
        print(f'Write to {Filename}.csv')
        writer = csv.writer(f)
        index = []
        for i in range(1, PgrCnt+1):
            index.append(str(i))
        writer.writerow(index)
        writer.writerow(T)
        writer.writerow(A)
        writer.writerow(D)
else:
    print(','.join(str(i) for i in range(1, PgrCnt+1)))
    print(','.join(str(t) for t in T))
    print(','.join(str(a) for a in A))
    print(','.join(str(d) for d in D))


#====================================================================
# .csv -> .dat

# ID      1     2     3    
#
# Arrive  1669  6009  8488
#
# Start.  2     3     4
#
# End.    5     1     6


with open(Filename+'.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    
    data = []

    for row in csv_reader:
        data.append(row)

    LOWEST_FLOOR = 1
    HIGHEST_FLOOR = Floor

    random.seed()
    CURRENT_FLOOR = random.randint(LOWEST_FLOOR, HIGHEST_FLOOR)

    file = open(f"{Filename}.dat","w+")

    file.write("param N := %d;\n" % PgrCnt)
    file.write("param L := %d;\n" % LOWEST_FLOOR)
    file.write("param H := %d;\n" % HIGHEST_FLOOR)
    file.write("param F := %d;\n" % CURRENT_FLOOR)
    file.write("param X := %d;\n\n" % Speed)

    file.write("param T :=\n")
    for i in range(PgrCnt):
        if i != (PgrCnt-1):
            file.write('    %d  %d\n' %((i+1),int(data[1][i])))
        else:
            file.write('    %d  %d;\n\n' %((i+1),int(data[1][i])))


    file.write("param A :=\n")
    for i in range(PgrCnt):
        if i != (PgrCnt-1):
            file.write('    %d  %d\n' %((i+1),int(data[2][i])))
        else:
            file.write('    %d  %d;\n\n' %((i+1),int(data[2][i])))


    file.write("param D :=\n")
    for i in range(PgrCnt):
        if i != (PgrCnt-1):
            file.write('    %d  %d\n' %((i+1),int(data[3][i])))
        else:
            file.write('    %d  %d;\n' %((i+1),int(data[3][i])))

    print(f'Parse to {Filename}.dat')
