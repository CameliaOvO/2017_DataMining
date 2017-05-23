# Data Science Programming Assignment 3 : perform clustering by using DBSCAN
# author : Seonha Park
# written in Python3

import sys
import math

VISIT = 1
UNVISIT = 0
UNCLASSIFIED = 0
NOISE = -1


# get distance between p[idx1, x1, y1] and q[idx1, x2, y2]
def dist(p, q):
    return math.sqrt(abs(p[1] - q[1]) ** 2 + abs(p[2] - q[2]) ** 2)


# use in regionQuery(P,eps)
def checkEpsNeighbor(p, q, eps):
    return dist(p, q) < eps


# return all points within P's eps-neighborhood (including P)
def regionQuery(p, all_point, eps):
    returnPts = []
    for q in all_point:
        if checkEpsNeighbor(p, q, eps):
            returnPts.append(q)
    return returnPts


# do DBSCAN algorithm
def DBSCAN(D, eps, minPts):
    cluster_id = 0
    visited = [UNVISIT] * len(D)
    classified = [UNCLASSIFIED] * len(D)
    #check all unvisited points
    for p in D:
        if visited[p[0]] == UNVISIT:
            visited[p[0]] = VISIT
            N = regionQuery(p, D, eps)
            if len(N) < minPts:
                classified[p[0]] = NOISE
            else:
                cluster_id += 1
                expandCluster(p, N, visited, classified, cluster_id, D, eps, minPts)
    return classified


# expand [cluster_id]th cluster
def expandCluster(P, N, visited, C_set, C, dataset, eps, minPts):
    C_set[P[0]] = C
    #check all eps-neighbors of P
    while len(N) > 0:
        P_ = N[0]
        if visited[P_[0]] == UNVISIT:
            visited[P_[0]] = VISIT
            N_ = regionQuery(P_, dataset, eps)
            if len(N_) >= minPts:
                N = N + N_
        if C_set[P_[0]] == UNCLASSIFIED:
            C_set[P_[0]] = C
        N.pop(0)


def main():
    # get command line argument
    input_file = sys.argv[1]
    num_of_cluster = int(sys.argv[2])
    eps = int(sys.argv[3])
    minpts = int(sys.argv[4])

    with open(input_file) as f:
        input_data = f.readlines()
    input_data = [d.strip() for d in input_data]

    # make train_data string to attribute list and get each attribute name and total number of columns
    object_list = []
    for line in input_data:
        each_line = line.split("\t")
        each_line[0] = int(each_line[0])
        each_line[1] = float(each_line[1])
        each_line[2] = float(each_line[2])
        object_list.append(each_line)

    # do clustering with DBSCAN and get clusters and number of cluster
    clustered = DBSCAN(object_list, eps, minpts)
    clusters = max(clustered)

    # separate points by cluster
    cluster_list = [[] for x in range(clusters)]
    for o, c in zip(object_list, clustered):
        if c > 0:
            cluster_list[c - 1].append(o)

    # make list of regionQuery result of all point (to reduce execution time)
    region_list = []
    for o in object_list:
        o_eps_neighbor = regionQuery(o,object_list,eps)
        region_list.append(o_eps_neighbor)

    # reduce the number of cluster if it is bigger than that in parameter
    while num_of_cluster < clusters:
        # calculate which cluster to merge (smallest cluster)
        size_of_cluster = [0] * clusters
        for c in range(len(size_of_cluster)):
            size_of_cluster[c] = len(cluster_list[c])
        to_merge = size_of_cluster.index(min(size_of_cluster))
        # move points to nearest bigger cluster
        for p in cluster_list[to_merge]:
            neighbors = region_list[p[0]]
            distance = sys.maxsize
            for neighbor in neighbors:
                if dist(p,neighbor) < distance and clustered[p[0]] != clustered[neighbor[0]]:
                    distance = dist(p,neighbor)
                    nearest = neighbor
            cluster_list[clustered[nearest[0]]-1].append(p)
            clustered[p[0]] = clustered[nearest[0]]
        cluster_list.pop(to_merge)
        clusters -= 1

    # write output file
    output_form = (input_file.split("."))[0] + "_cluster_"
    output_files = []
    for n in range(num_of_cluster):
        output_files.append(output_form + str(n) + ".txt")

    for idx in range(len(output_files)):
        out_f = open(output_files[idx], "w")
        cluster_list[idx].sort()
        to_write = cluster_list[idx]
        for c in to_write:
            out_f.write(str(c[0]) + "\n")


if __name__ == '__main__':
    main()
