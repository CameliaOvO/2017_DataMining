# Data Science Programming Assignment 2 : decision tree
# author : Seonha Park
#written in Python3
import math

def majorityClass(attributes, data, target):
    freq_value  = {}
    index = attributes.index(target)
    for entry in data:
        if entry[index] in freq_value:
            freq_value[entry[index]] += 1
        else:
            freq_value[entry[index]] = 1
    max = 0
    major_label = ""
    for key in freq_value.keys():
        if freq_value[key] > max:
            max = freq_value[key]
            major_label = key
    return major_label


def GainRatio(D, attribute_name, total_attr):
    attr_name = ""

    #get Info(D)
    info_dic = D[attribute_name[len(attribute_name)-1]]
    info_val_list = []
    for k, v in info_dic.items():
        if k in v:
            info_val_list.append(v[k])

    info_d = 0.0
    for i in info_val_list:
        if i > 0:
            info_d -= (float(i)/float(total_attr)) * math.log2((float(i)/float(total_attr)))
        else:
            info_d -= 0
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
                if num > 0:
                    info_dj = (float(num)/float(total_in_class)) * math.log2(float(num)/float(total_in_class))
                else:
                    info_dj = 0
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
            if num > 0:
                calc_info -= (float(num)/float(total_attr)) * math.log2(float(num)/float(total_attr))
            else:
                calc_info -= 0
        split_info[k] = calc_info

    gain_ratio = {}
    for k, v in gain_list.items():
        for k1, v1 in split_info.items():
            if k == k1 :
                gain_ratio[k] = v / v1
    attr_name = max(gain_ratio, key=gain_ratio.get)

    return attr_name


def getValues(data, attributes, attribute):
    index = attributes.index(attribute)
    values = []
    for entry in data:
        if entry[index] not in values:
            values.append(entry[index])
    return values


def getEntries(data, attributes, selected, val):
    all_entries = [[]]
    index = attributes.index(selected)
    for entry in data:
        if entry[index] == val:
            new_entry = []
            for i in range(0,len(entry)):
                if i != index :
                    new_entry.append(entry[i])
            all_entries.append(new_entry)
    all_entries.remove([])
    return all_entries


def makeDataPartition(attribute_name, attribute_list):
    possible_name = {}
    for i in range(len(attribute_name)):
        ith_class = []
        for attr in attribute_list:
            if attr[i] not in ith_class:
                ith_class.append(attr[i])
        possible_name[attribute_name[i]] = ith_class
    class_label = possible_name[attribute_name[len(attribute_name)-1]]

    data_partition = {}
    for i in range(len(attribute_name)):
        ith_attr = {}

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
                    v[label] = 0

        data_partition[attribute_name[i]] = ith_attr
    return data_partition


def getNumOfAnswer(attribute_list):
    result_dict = {}
    for attr in attribute_list:
        if attr[len(attr)-1] not in result_dict:
            result_dict[attr[len(attr)-1]] = 1
        else:
            result_dict[attr[len(attr) - 1]] += 1
    return result_dict

def GenerateTree(attribute_list, attribute_name):
    target = attribute_name[len(attribute_name)-1]
    attribute_list = attribute_list[:]
    values = []
    idx = attribute_name.index(target)
    for attr in attribute_list:
        values.append(attr[idx])

    if not attribute_list or (len(attribute_name) - 1) <= 0:
        return majorityClass(attribute_name, attribute_list, target)

    elif values.count(values[0]) == len(values):
        return values[0]

    else :
        selected = GainRatio(makeDataPartition(attribute_name, attribute_list), attribute_name, len(attribute_list))
        tree = {selected:{}}

        for value in getValues(attribute_list, attribute_name, selected):
            all_attribute = getEntries(attribute_list, attribute_name, selected, value)
            new_attribute = attribute_name[:]
            new_attribute.remove(selected)

            child = GenerateTree(all_attribute, new_attribute)
#            print("child " + value + " generated and total number is " + str(len(all_attribute)))
            tree[selected][value] = child
            tree[selected]["num"] = getNumOfAnswer(attribute_list)
    return tree