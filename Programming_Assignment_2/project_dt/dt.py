# Data Science Programming Assignment 2 : decision tree
# author : Seonha Park
# written in Python3

import sys
import math


# TODO: implement attribute selection method(D, attr_list) in 3 ways
def attr_selection(D, attribute_list,total_attr):
    attr_name = ""
    #using gain ratio

    #using Gini index

    return attr_name




# get command line argument
# train_file = sys.argv[1]
# test_file = sys.argv[2]
# output_file = sys.argv[3]

# erase after finish dt
train_file = "data/dt_train.txt"
test_file = "data/dt_test.txt"
output_file = "data/dt_result.txt"

# get train file and make list of columens
with open(train_file) as f:
    train_data = f.readlines()
train_data = [d.strip() for d in train_data]

# make train_data string to attribute list and get each attribute name and total number of column
attribute_list = []
total_attribute = 0
for line in train_data:
    each_line = line.split("\t")
    attribute_list.append(each_line)
    total_attribute += 1
attribute_name = attribute_list[0]
attribute_list.pop(0)
total_attribute -= 1


# make D_1
data_partition = {}
for i in range(len(attribute_name)):
    ith_attr = {}
    for attr in attribute_list:
        if attr[i] not in ith_attr:
            ith_attr[attr[i]] = 1
        else :
            ith_attr[attr[i]] += 1
    data_partition[attribute_name[i]] = ith_attr


for k, v in data_partition.items():
    print(k),
    print(v)

"""
Make Decision Tree
input : Data partition  D (data_partition)
        set of candidate attributes attr_list (attribute_list)
        Attribute Selection Method (attr_selection)

output : A tree

node {
        is leaf
        classification

    }


"""








