from itertools import combinations
from math import fabs

from point_module import Point
from random import random

from timeit import default_timer as timer

from vector_module import get_angle_of_vector, get_intersection

li = []
li2 = []
li3 = []
ori = Point((0, 0, 0))
orx = Point((1,0,0))

for i in range(90):
    li.append(Point((i,(90-i)/1000, 0)))

p1 = Point((-100,0,0))
p2 = Point((200,0,0))
p3 = Point((-50,0,0))

for i in li:
    print(i)
    get_intersection(p1,p2,p3,i,False)
