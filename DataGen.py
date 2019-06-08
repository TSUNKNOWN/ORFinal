#!/usr/bin/env python
# coding: utf-8

# In[134]:


import random
import numpy as np
import sys
import csv
import functools
import operator
from scipy.stats import expon
from pprint import pprint
Time = 300
MaxNum = 100
Floor = 7
Filename = None


# In[135]:


print('Usage: python DataGen.py Time MaxPeople Floor [OutputFile]')
if 'y' in input('Default?(n/y)'):
    Filename = 'testoutput.csv'
elif len(sys.argv) == 1:
    Time = int(input('Time?'))
    MaxNum = int(input('MaxPeople?'))
    Floor = int(input('Floor?'))
elif len(sys.argv) >= 4:
    Duration = int(sys.argv[1])
    MaxNum = int(sys.argv[2])
    Floor = int(sys.argv[3])
    try:
        Filename = sys.argv[4]
    except:
        pass
elif sys.argv[1] == '-f':
    pass
else:
    # If conert to .py
    print('Invalid Arguments')
    exit(0)
Lambda = MaxNum/Time
print(f'Time:{Time}')
print(f'MaxPeople:{MaxNum}')
print(f'Floor:{Floor}')
print(f'Filename: {Filename}')
print(f'Frequency:{Lambda}')


# In[136]:


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


# In[137]:


def getA(args):
    aprobs = getAProb(args)
    a = aprobs.index(max(aprobs))
    args['Asinterval'][a] = 0
    args['a'] = a
    return a+1
def getD(args):
    dprobs = getDProb(args)
    d = dprobs.index(max(dprobs))
    args['Dsinterval'][d] = 0
    return d+1


# In[147]:


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
while nowNum < MaxNum :
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
print(f'Average arrived Interval: {args["SumOfTInterval"]/MaxNum}')
# adTable[a][d] means # of passengers from a to d
print('From a to d scatter table:')
pprint(adTable)


# In[122]:


if Filename != None:
    with open(Filename, 'w') as f:
        print(f'Write to {Filename}')
        writer = csv.writer(f)
        index = ['',]
        for i in range(1, MaxNum+1):
            index.append(str(i))
        writer.writerow(index)
        writer.writerow(T)
        writer.writerow(A)
        writer.writerow(D)
else:
    print(','.join(str(i) for i in range(1, MaxNum+1)))
    print(','.join(str(t) for t in T))
    print(','.join(str(a) for a in A))
    print(','.join(str(d) for d in D))


# In[ ]:




