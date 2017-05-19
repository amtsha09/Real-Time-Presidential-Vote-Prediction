
# cluster


import matplotlib.pyplot as plt
import networkx as nx
import itertools
from collect import get_twitter, robust_request
import os

num_com = 0
li = []


fr = open("nodes.txt","r")
li = fr.readlines()
li = list(map(str.strip, li))
fr.close()


edges = list(itertools.combinations(li, 2))


############ friends dictionary

twitter = get_twitter()

di = {}
for user in li:
    f = robust_request(twitter, "friends/ids", {"screen_name": user}).json()
    l = sorted(f['ids'])
    di[user] = l


edges_weight = {}
for edge in edges:
    intersect = len(set(di[edge[0]]) & set(di[edge[1]]))
    union = len(set(di[edge[0]]) | set(di[edge[1]]))
    edges_weight[edge] = intersect/union



ef = open("edges.txt","a")
for edge in edges:
    ef.write(edge[0])
    ef.write("\t")
    ef.write(edge[1])
    ef.write("\n")
ef.close()



g = nx.Graph()
g = nx.read_edgelist("edges.txt",delimiter = "\t")
nx.draw_networkx(g)
plt.show()



for i in sorted(edges_weight.items(), key=lambda x:x[1]):
    components = [c for c in nx.connected_component_subgraphs(g)]
    if len(components) == 2:
        break
    else:
        g.remove_edge(i[0][0],i[0][1])
        del edges_weight[(i[0][0],i[0][1])]

num_com = len(components)


nx.draw_networkx(g)

plt.show()



ow = open("output.txt","a")
ow.write("Number of communities discovered:" + str(num_com))
ow.write("\n")
ow.write("Average number of users per community:" + str(len(li)/num_com))
ow.write("\n")

ow.close()

