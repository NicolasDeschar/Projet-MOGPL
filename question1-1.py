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
J=[0,1,2]




pop[:]=list(map(int,pop))
gamma=((1+alpha)/len(J))*sum(pop)

nbcont=len(pop)+len(J)
nbvar=len(pop)*len(J)+len(J)

#contrainte somme(xij vi) <= gamma
mat=[]
for i in range(len(J)):
    l=[0]*nbvar
    for j in range(len(pop)):
        l[j+(i*len(pop))]=pop[j]
    l[(i-len(J))]=1
    mat.append(l)
    
#contrainte somme_j(xij) == 1
for i in range(len(pop)):
    l=[0]*nbvar
    for j in range(len(J)):
        l[i+(j*len(pop))]=1
    mat.append(l)
    

sm=[]
for i in range(len(J)):
    sm.append(gamma)
for i in range(len(pop)):
    sm.append(1)
    


def get_dist(i,j):
    try :
        return dist[i][j]
    except IndexError :
        return dist[j][i]

fo=[]
for i in J:
    for j in range(len(pop)):
        fo.append(get_dist(i,j))
for i in range(len(J)):
    fo.append(0)


lignes = range(nbcont)
colonnes = range(nbvar)



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
for i in range(nbvar-len(J)):
    u+=1
    x.append(m.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name="x%d" % (i+1)))
for i in range(len(J)):
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
for i in range(len(pop)*len(J)):
    temp.append(x[i].x)
    if len(temp)==len(pop):
        res.append(temp)
        temp=[]
np.set_printoptions(edgeitems=15)
matres=np.asmatrix(res)

di=0
for i in range(len(res)):
    for j in range(len(res[0])):
        di+=get_dist(j,J[i])*res[i][j]*pop[j]
di/=sum(pop)

print("")
print("Matrice des xij")
print(matres.T)
print("")
print("distance moyenne")
print(di)
























