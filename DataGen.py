#!/usr/bin/env python
# coding: utf-8

# In[5]:


import random
import numpy as np
import sys
import csv
import functools
import operator
Time = 1000
MaxNum = 10
Floor = 7
Filename = None


# In[6]:


print('Usage: python DataGen.py Time MaxPeople Floor [OutputFile]')
if 'y' in input('Default?(n/y)'):
    Filename = 'testoutput.csv'
    print(f'Time:{Time}')
    print(f'MaxPeople:{MaxNum}')
    print(f'Floor:{Floor}')
    print(f'Filename: {Filename}')
    pass
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
else:
    # If conert to .py
    print('Invalid Arguments')
    exit(0)
Prob = 1-1/Time


# In[7]:


def getTProb(args):
    return calcTProb(args)
def getAProb(args):
    aprobs = []
    for f in range(Floor):
        aprobs.append(calcAProb(args))
    return aprobs
def getDProb(args):
    dprobs = []
    a = args['a']
    for f in range(Floor):
        dprobs.append(calcDProb(args))
    dprobs[a-1] = 0
    return dprobs


# In[8]:


def calcTProb(args):
    return random.random()
def calcAProb(args):
    return random.random()
def calcDProb(args):
    return random.random()


# In[15]:


A = []
D = []
T = []
nowNum = 0
t = 1
interval = 0
args = {'time':t, 'interval':interval}
while nowNum < MaxNum :
    havePeople = getTProb(args) > Prob
    if havePeople:
        nowNum += 1
        args['time'] = t
        args['interval'] = interval 
        T.append(t)
        aprobs = getAProb(args)
        a = aprobs.index(max(aprobs))+1
        A.append(a)
        args['a'] = a
        dprobs = getDProb(args)
        d = dprobs.index(max(dprobs))+1
        D.append(d)
        interval = 0
    interval += 1
    t += 1
if t > Time:
    print(f'Warning! Exceed expected time with t={t}')


# In[107]:


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




