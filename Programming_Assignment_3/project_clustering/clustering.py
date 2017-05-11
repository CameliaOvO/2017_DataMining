# Data Science Programming Assignment 3 : perform clustering
# author : Seonha Park
# written in Python3

import sys

#get command line argument
# input_file = sys.argv[1]
# num_of_cluster = sys.argv[2]
# eps = sys.argv[3]
# minpts = sys.argv[4]

input_file = "data/input1.txt"
num_of_cluster = 8
eps = 15
minpts = 22

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

regionQuery(P, eps)
   return all points within P's eps-neighborhood (including P)
"""