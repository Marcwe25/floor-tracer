import functools
from collections import defaultdict
from random import randint
from timeit import default_timer as timer
from itertools import combinations

t1 = timer()

li = []
li2 = []
for i in range(100):
    li.append([])
    for j in range(100):
        li[-1].append([])
        for k in range(100):
            li[-1][-1].append([[i][j][k]])

for i in range(100):
    li.append([])
    for j in range(100):
        li[-1].append([])
        for k in range(100):
            li2[-1][-1].append(li[i][j][k])


t2 = timer()


t2 = timer()




t3 = timer()

print("1 ",t2-t1)
print("2 ", t3-t2)
