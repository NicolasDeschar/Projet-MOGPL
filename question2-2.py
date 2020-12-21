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





alpha=0.2
k=5




pop[:]=list(map(int,pop))
gamma=((1+alpha)/k)*sum(pop)

nbcont=len(pop)+len(pop)
nbvar=len(pop)*len(pop)+1

#contrainte somme(xij vi) <= gamma
mat=[]
for i in range(len(pop)):
    l=[0]*nbvar
    for j in range(len(pop)):
        l[j+(i*len(pop))]=pop[j]
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
        
#contrainte xjj - xij >= 0
n=-1
for i in range(len(pop)):
    for j in range(len(pop)):
        l=[0]*nbvar
        l[j+(i*len(pop))]=-1
        l[i+(i*len(pop))]=1
        mat.append(l)
        
        
#contrainte somme_j(dij xij) <=z
for i in range(len(pop)):
    l=[0]*nbvar
    for j in range(len(pop)):
        l[i+(j*len(pop))]=get_dist(i,j)
    l[-1]=-1
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

for i in range(len(pop)):
    sm.append(0)


def get_dist(i,j):
    try :
        return dist[i][j]
    except IndexError :
        return dist[j][i]

fo=[0]*nbvar
fo[-1]=1


lignes = range(len(mat))
colonnes = range(len(mat[0]))



# Matrice des contraintes
a = mat

# Second membre
b = sm


# Coefficients de la fonction objectif
c = fo

m = Model("mogplex")     
        
# declaration variables de decision
x = []
u=0
for i in range(len(pop)**2):
    u+=1
    x.append(m.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name="x%d" % (i+1)))
x.append(m.addVar(vtype=GRB.INTEGER, lb=0, name="x%d" % (i+1)))
# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]
    


# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)

# Definition des contraintes


for i in range(len(mat)-(len(pop))):
    if b[i]==1 or b[i]==k:
         m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) == b[i], "Contrainte%d" % i)
    elif b[i]==0:
         m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) >= b[i], "Contrainte%d" % i)
    else :
         m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)

for i in range(len(mat)-(len(pop)),len(mat)):
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
    
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


print("")
print("Matrice des xij")
print(matres.T)
print("")
print("distance maximale")
print(m.objVal)

