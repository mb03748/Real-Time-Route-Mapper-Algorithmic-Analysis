import time
import itertools
import urllib.request
import json
import copy
import sys
import urllib.request
import json
import random

global table

start = time.time()
g = {}


""" list of largest cities """
cityString = "Oslo Karachi Istanbul Moscow Cairo Lagos Paris London Kabul Baku Manama Sitra Brussels Giza Suez Berlin Hamburg Munich Frankfurt Dusseldorf Accra Athens Tehran Mashhad Rome Milan Turin Lahore Faisalabad Rawalpindi Islamabad Multan Peshawar Quetta Kotli Bhawalpur Sargodha Amman Almaty Nairobi Beirut Tripoli Benghazi Luxembourg Sharjah Dubai Ajman Birmingham Liverpool Nottingham Bristol Manchester Glasgow Edinburgh Leeds Cardiff Tashkent Samarkand Ankara Izmir Bursa Konya Zanzibar Zurich Basel Bern Aleppo Damascus Madrid Barcelona Valencia Riyadh Jeddah Mecca Medina Dammam Doha Muscat"
#80 cities currntly 

cityList = cityString.split(" ")


def nodeGenerator(n):
    lst = []
    while len(lst) != n:
        randNo = random.randint(0, len(cityList))
        if cityList[randNo] not in lst:
            lst.append(cityList[randNo])
    return lst

nodes =  ['Rome', 'Multan', 'Manchester', 'london', 'Paris', "Murree", "Sialkot"] 
print("Cities:", nodes)



list1 = []
for x in nodes:
    for y in nodes:
        if x!=y:
            if [y,x] not in list1:
                list1.append([x,y])
edges = list1



for i in edges:
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyDtXUOF8QiIB608KLzmSlPZJhHjh81Wrvw'

    origin = i[0].replace(',','').replace(' ','+').replace('،','')
    destination = i[1].replace(',','').replace(' ','+').replace('،','')

    request = endpoint + 'origin='+origin+'&destination='+destination+'&key='+api_key
    response = urllib.request.urlopen(request).read()
    directions = json.loads(response)
    distance = directions['routes'][0]['legs'][0]['distance']['text'][:-3].replace(',','')
    i.append(float(distance))



################################################HELPER FUNCTIONS###########################################


def addnodes(g,nodes):
    for i in nodes:
        g[i] = []
    return g
addnodes(g,nodes)

def addedges(g,edges,directed=False):

    if directed:

        for start, *end in edges:

            g[start].append(list(end))

    else:

        for i in edges:

            start,*end=i

            g[start].append(list(end))

            start=i[1]

            appan=[i[0]]+list(i[2:])

            g[start].append(appan)

    return g

addedges(g,edges)
end = time.time()
total = end - start
print(g)
print('')
print("Time taken to build the graph: ",total)


def swap(a,i,j):
    a[i],a[j] = a[j],a[i]

def listOfNodes(g):
    lst = []
    for i in g.keys():
        lst.append(i)
    return lst

def removeNodes(g,nodes):
    for i in nodes:
        if i in g:
            del g[i]
    return g

def gnn(g,node,V):
    a = 100000
    if isinstance(node,list):
        node=node[0]
    for i in g[node]:
        if i[1]<a and i[0] not in V:
            a = i[1]
            b = i
    return b


def graphToMatrix(graph):
    global table
    table = []
    if len(graph) <= 1:
        return 0
    for i in range(len(graph)+1):
        table.append([])
        for j in range(len(graph)+1):
            table[i].append(0)
    return table




#########################################DYNAMMIC PROGRAMMING###########################################

start = time.time()
t = graphToMatrix(g)

table = t

print("Matrix: ", table)
count = 0
for i in range(len(nodes)):
    for j in range(len(nodes)):
        if nodes[i] == nodes[j]:
            continue
        else:
            table[i][j] = g[nodes[i]][count][1]
            count = count + 1
    count = 0

end = time.time()
total = end - start
print("Time taken to build our matrix is: ",total)
print("This is our matrix for DP: ", table)

####adding this to make data [1,2,3,4] #####
data = []
for i in range(len(nodes)):
    data.append(i+1)
############################################
n = len(data)
all_sets = []
g1 = {}
p = []
final = []

def dynamicSolve():
    for x in range(1, n):
        g1[x + 1, ()] = table[x][0]
    
    recursive(data[0], tuple(data[1:]))
    final.append(0)
    solution = p.pop()
    final.append(solution[1][0])
    for x in range(n - 2):
        for latest in p:
            if tuple(solution[1]) == latest[0]:
                solution = latest
                final.append(solution[1][0])
                break
    final.append(0)
    print("\nThis is our list",final)

    print("[",end="")
    for i in final:
        if i == 0:
            print(nodes[i], end=' ')
        else:
            print(nodes[i-1], end=' ')
    print("]")
    return


def recursive(k, a):
    if (k, a) in g1:
        # Already calculated Set g[%d, (%s)]=%d' % (k, str(a), g[k, a]))
        return g1[k, a]
    values = []
    minimumValue = []
    for j in a:
        includedIna = copy.deepcopy(list(a))
        includedIna.remove(j)
        minimumValue.append([j, tuple(includedIna)])
        result = recursive(j, tuple(includedIna))
        values.append(table[k-1][j-1] + result)
    # get minimun value from set as optimal solution for
    if len(values) > 0:
        g1[k, a] = min(values)
    else:
        g1[k, a] = 0
    #g[k, a] = min(values)
    p.append(((k, a), minimumValue[values.index(g1[k, a])]))
    return g1[k, a]

start = time.time()
dynamicSolve()
end = time.time()
total = end - start
print("Time taken by Dynammic Programming is: ",total)

#########################################GET NEAREST NEIGHBIOUR###########################################

def tsp(g,node):
    V = []
    d = 0
    lst = []
    a = listOfNodes(g)
    V.append(node)
    lst.append(node)
    while len(V) < len(a):
        b = gnn(g, node, V)
        node = b[0]
        temp = b[0]
        lst.append(temp)
        removeNodes(g,node)
        V.append(node)
    lst = lst + [lst[0]]
    for j in range(len(lst)):
        if j+1<len(lst):
            v1 = lst[j]
            v2 = lst[j+1]
            for edge in edges:
                if (edge[0] == v1 and edge[1] == v2) or (edge[0] == v2 and edge[1] == v1):
                    d += edge[2]
                    
    print(d,lst)

start = time.time()
tsp(g, nodes[0])
end = time.time()
total = end - start
print("Time taken by nearsest neighbor is: ",total,"\n")

addnodes(g,nodes)
addedges(g,edges)

#########################################BRUTE FORCE###########################################
def bruteforce(nodes,n):
    a = float('inf')
    b = None
    nodes.remove(n)
    perm = itertools.permutations(nodes)
    for i in perm:
        d = 0
        temp = [n] + list(i) + [n]
        for j in range(len(temp)):
            if j+1<len(temp):
                v1 = temp[j]
                v2 = temp[j+1]
                for edge in edges:
                    if (edge[0] == v1 and edge[1] == v2) or (edge[0] == v2 and edge[1] == v1):
                        d += edge[2]
        if d < a:
            b = temp        
            a = d

    return a,b

start = time.time()
print(bruteforce(nodes, nodes[0]))
end = time.time()
total = end - start
print("Time taken by Brute Force: ",total,"\n") 
