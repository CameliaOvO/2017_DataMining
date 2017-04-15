# Data Science Programming Assignment 2 : decision tree
# author : Seonha Park
# written in Python3

import sys
import math

class Tree(object):
    def __init__(self, name = 'root'):
        self.name = ""
        self.childs = []


# implement gain ratio
def GainRatio(D, attribute_name, total_attr):
    attr_name = ""

    #info(D) 구하기
    info_dic = D[attribute_name[len(attribute_name)-1]]
    info_val_list = []
    for k, v in info_dic.items():
        if k in v:
            info_val_list.append(v[k])

    info_d = 0.0
    for i in info_val_list:
        info_d -= (float(i)/float(total_attr)) * math.log2((float(i)/float(total_attr)))
    print(info_d)

    del D[attribute_name[len(attribute_name)-1]]


    gain_list = {}
    for k,v in D.items():
        calc_info = 0.0
        for k1, v1 in v.items():
            total_in_class = 0
            list_in_class = []
            for k2, v2 in v1.items():
                list_in_class.append(v2)
                total_in_class += v2
            for num in list_in_class:
                info_dj = (float(num)/float(total_in_class)) * math.log2(float(num)/float(total_in_class))
                calc_info -= float(total_in_class)/float(total_attr) * info_dj
        gain_list[k] = info_d - calc_info

    split_info = {}
    for k, v in D.items():
        calc_info = 0.0
        list_in_class = []
        for k1, v1 in v.items():
            total_in_class = 0
            for k2, v2 in v1.items():
                total_in_class += v2
            list_in_class.append(total_in_class)
        for num in list_in_class:
            calc_info -= (float(num)/float(total_attr)) * math.log2(float(num)/float(total_attr))
        split_info[k] = calc_info

    gain_ratio = {}
    for k, v in gain_list.items():
        for k1, v1 in split_info.items():
            if k == k1 :
                gain_ratio[k] = v / v1
    print (gain_ratio)

    attr_name = max(gain_ratio, key=gain_ratio.get)

    return attr_name



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

#    for k,v in ith_attr.items():
#        for label in class_label:
#            if label not in v:
#               print(label + " is not in " + k)
#                v[label] = 0


    data_partition[attribute_name[i]] = ith_attr


for k, v in data_partition.items():
    print(k),
    print(v)


#gini_selection(data_partition,attribute_name,attribute_list,total_attribute)


GainRatio(data_partition,attribute_name,total_attribute)




def Generate_decision_tree(D, attribute_name, attribute_list, selection_method, total_attr):
    pass







