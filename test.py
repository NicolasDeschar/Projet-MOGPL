#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 01:07:22 2020

"""
import numpy as np

def read_csv ( filename ):
    data = np.loadtxt ( filename, delimiter=';', dtype=np.str ).T
    pop=np.ndarray.tolist(data[0][1:])
    dist=[]
    for i in range(len(data)-2):
        dist.append([])
    for i in range(2,len(data)):
        temp=data[i]
        temp2=temp[1:]
        for j in range(len(temp2)):
            if len(temp2[j])!=0:
                dist[j].append(int(temp2[j]))
        
    return pop,dist

pop,dist=read_csv ( "villes.csv" )
'''print("pop",pop)
print("dist",dist)'''


alpha=0.1
J=[3,4,5]

pop[:]=list(map(int,pop))
#print(pop)
#print(dist)
gamma=((1+alpha)/len(J))*sum(pop)


nbcont=len(pop)+len(J)
nbvar=len(pop)*len(J)+len(J)

mat=[]
for i in range(len(J)):
    l=[0]*nbvar
    for j in range(len(pop)):
        l[j+(i*len(pop))]=pop[j]
    l[(i-len(J))]=1
    mat.append(l)
    

for i in range(len(pop)):
    l=[0]*nbvar
    for j in range(len(J)):
        l[i+(j*len(pop))]=1
    mat.append(l)
    

#print(mat)

'''
dist1=list(dist)
print(dist)
for i in range (len(dist)-1):
    for k in range(l)
    
    a=u[:,i]
    print(a)
    for j in range(len(a)):
        dist[i].append(a[j])
        
print(dist)
''' 

def get_dist(i,j):
    try :
        return dist[i][j]
    except IndexError :
        return dist[j][i]


fo=[]
for i in J:
    for j in range(len(pop)):
        fo.append(get_dist(i,j))
print(fo)

print(sum(pop))
print(1306983*3)
