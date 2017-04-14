# Data Science Programming Assignment 2 : decision tree
# author : Seonha Park
# written in Python3

import sys
import math



# TODO: Implement Gini Index
def gini_selection(D, attribute_name, attribute_list,total_attr):
    attr_name = []

    # Gini(D) 구하기
    gini_dic = D[attribute_name[len(attribute_name)-1]]
    gini_val_list = []
    for k, v in gini_dic.items():
        if k in v:
            gini_val_list.append(v[k])

    gini_D = 1.0
    for i in gini_val_list:
        gini_D -= (float(i)/float(total_attr)) * (float(i)/float(total_attr))

    del D[attribute_name[len(attribute_name)-1]]

    min_gini_index = 1
    # 각각의 attr에 대해 Gini_a(D)
    for k,v in D.items():
        all_label = []
        for k1, v1 in v.items():
            all_label.append(k1)
        label_subsets = [[]]
        proper_subsets = []
        for x in all_label:
            label_subsets.extend([y + [x] for y in label_subsets])
        label_subsets.pop(0)
        label_subsets.pop(len(label_subsets)-1)
        for sets in label_subsets:
            sets.sort()
            remain_set = list(set(all_label).difference(set(sets)))
            remain_set.sort()
            set_tuple = (sets,remain_set)
            if len(sets) < len(remain_set):
                proper_subsets.append(set_tuple)
            elif len(sets) == len(remain_set):
                new_tuple = (remain_set,sets)
                if new_tuple not in proper_subsets:
                    proper_subsets.append(set_tuple)

#        print(proper_subsets)
#        print(v)
        for subset in proper_subsets:
            for i in range(0,2):
                for key in subset[i]:
                    print(key + " : "),
                    print(v[key])

    return attr_name



# get command line argument
# train_file = sys.argv[1]
# test_file = sys.argv[2]
# output_file = sys.argv[3]

# erase after finish dt
train_file = "data/dt_train1.txt"
test_file = "data/dt_test1.txt"
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

possible_name = {}
# get possible classes
for i in range(len(attribute_name)):
    ith_class = []
    for attr in attribute_list:
        if attr[i] not in ith_class:
            ith_class.append(attr[i])
    possible_name[attribute_name[i]] = ith_class

class_label = possible_name[attribute_name[len(attribute_name)-1]]

# make D_1
data_partition = {}
for i in range(len(attribute_name)):
    ith_attr = {}
#    for label in class_label:
#        ith_attr[label] = 0

    for attr in attribute_list:
        if attr[i] not in ith_attr:
            ith_attr[attr[i]] = {attr[len(attribute_name)-1] : 1}
        else :
            if attr[len(attribute_name)-1] not in ith_attr[attr[i]]:
                ith_attr[attr[i]][attr[len(attribute_name)-1]] = 1
            else :
                ith_attr[attr[i]][attr[len(attribute_name) - 1]] += 1

    for k,v in ith_attr.items():
        for label in class_label:
            if label not in v:
#               print(label + " is not in " + k)
                v[label] = 0


    data_partition[attribute_name[i]] = ith_attr


#for k, v in data_partition.items():
#    print(k),
#    print(v)


#gini_selection(data_partition,attribute_name,attribute_list,total_attribute)



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








