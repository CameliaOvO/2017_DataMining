# Data Science Programming Assignment 3 : perform clustering
# author : Seonha Park
# written in Python3

import sys
import math

# get distance between p[idx1, x1, y1] and q[idx1, x2, y2]
def dist(p,q):
    return math.sqrt(abs(p[1]-q[1])**2 + abs(p[2]-q[2])**2)

# use in regionQuery(P,eps)
def checkEpsNeighbor(p,q,eps):
    return dist(p,q) < eps

# return all points within P's eps-neighborhood (including P)
def regionQuery(p,all_point,eps):
    returnPts = []
    for q in all_point:
        if checkEpsNeighbor(p,q,eps):
            returnPts.append(q)
    return returnPts

def DBSCAN(D, eps, minPts):
    pass

def expandCluster(P,N,C,eps,minPts):
    pass

"""
DBSCAN(D, eps, MinPts)
   C = 0
   for each unvisited point P in dataset D
      mark P as visited
      N = regionQuery(P, eps)
      if sizeof(N) < MinPts
         mark P as NOISE
      else
         C = next cluster
         expandCluster(P, N, C, eps, MinPts)

expandCluster(P,N,C,eps,MinPts)
   add P to cluster C
   for each point P' in N
      if P' is not visited
         mark P' as visited
         N' = regionQuery(P', eps)
         if sizeof(N') >= MinPts
            N = N joined with N'
      if P' is not yet member of any cluster
         add P' to cluster C

"""

def main():
    # get command line argument
    # input_file = sys.argv[1]
    # num_of_cluster = sys.argv[2]
    # eps = sys.argv[3]
    # minpts = sys.argv[4]

    input_file = "data/input1.txt"
    num_of_cluster = 8
    eps = 15
    minpts = 22

    with open(input_file) as f:
        input_data = f.readlines()
    input_data = [d.strip() for d in input_data]

    # make train_data string to attribute list and get each attribute name and total number of columns
    object_list = []
    total_object = 0
    for line in input_data:
        each_line = line.split("\t")
        object_list.append(each_line)
        total_object += 1


if __name__ == '__main__':
    main()