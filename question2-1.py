#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 14:38:06 2020

@author: etudiant
"""

#!/usr/bin/python

# Copyright 2013, Gurobi Optimization, Inc.


from gurobipy import *
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
#print("pop",pop)
#print("dist",dist)

alpha=0.2
k=3

pop[:]=list(map(int,pop))


gamma=((1+alpha)/k)*sum(pop)
print(gamma)

nbcont=len(pop)+len(pop)
nbvar=len(pop)*len(pop)+len(pop)+len(pop)**2

#contrainte somme(xij vi) <= gamma
mat=[]
for i in range(len(pop)):
    l=[0]*nbvar
    for j in range(len(pop)):
        l[j+(i*len(pop))]=pop[j]
    tr=k+(len(pop)**2)
    l[i-tr]=1
    mat.append(l)
    
#contrainte somme_j(xij) == 1
for i in range(len(pop)):
    l=[0]*nbvar
    for j in range(len(pop)):
        l[i+(j*len(pop))]=1
    mat.append(l)
    
#contrainte somme(xjj) == k
l=[0]*nbvar
v=0
for i in range(len(pop)):
    l[v]=1
    v+=1+len(pop)
    
mat.append(l)
print("l",l)
        
#contrainte xjj - xij >= 0
n=-1
for i in range(len(pop)):
    for j in range(len(pop)):
        l=[0]*nbvar
        l[i+(j*len(pop))]=-1
        l[i+(i*len(pop))]=1
        l[n]=-1
        n-=1
        mat.append(l)
        
        
    

sm=[]
for i in range(len(pop)):
    sm.append(gamma)
for i in range(len(pop)):
    sm.append(1)
sm.append(k)

for i in range(len(pop)):
    for j in range(len(pop)):
        sm.append(0)

    


def get_dist(i,j):
    try :
        return dist[i][j]
    except IndexError :
        return dist[j][i]

fo=[]
for i in range(len(pop)):
    for j in range(len(pop)):
        fo.append(get_dist(i,j))
for i in range(len(pop)):
    fo.append(0)
for i in range(len(pop)):
    for j in range(len(pop)):
        fo.append(0)
#print(fo)

lignes = range(nbcont)
colonnes = range(nbvar)

#print("a")
#print(a)

# Matrice des contraintes
a = mat
#print(a)
print("")

# Second membre
b = sm
#print(b)
print("")

# Coefficients de la fonction objectif
c = fo
#print(c)

m = Model("mogplex")     
        
# declaration variables de decision
x = []
u=0
for i in range(len(pop)**2):
    u+=1
    x.append(m.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name="x%d" % (i+1)))
for i in range(len(pop)):
    u+=1
    x.append(m.addVar(vtype=GRB.INTEGER, lb=0, name="x%d" % (u+1)))
for i in range(len(pop)**2):
    u+=1
    x.append(m.addVar(vtype=GRB.INTEGER, lb=0, name="x%d" % (u+1)))
# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]
    
        
# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)

# Definition des contraintes
for i in lignes:
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) == b[i], "Contrainte%d" % i)

# Resolution
m.optimize()
res=[]
temp=[]
for i in range(len(pop)*len(pop)):
    temp.append(x[i].x)
    if len(temp)==len(pop):
        res.append(temp)
        temp=[]
np.set_printoptions(edgeitems=15)
matres=np.asmatrix(res)
print(matres)

#print(res)
di=0
for i in range(len(res)):
    for j in range(len(res[0])):
        di+=get_dist(j,i)*res[i][j]*pop[j]
di/=sum(pop)

print("")
print("Matrice des xij")
print(matres.T)
print("")
print("distance moyenne")
print(di)





