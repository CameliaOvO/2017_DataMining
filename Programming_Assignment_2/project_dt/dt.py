# Data Science Programming Assignment 2 : decision tree
# author : Seonha Park
# written in Python3
import DecisionTree
import TreeNode
import random

def main():
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


    decision_label = attribute_name[len(attribute_name) - 1]
    tree = DecisionTree.GenerateTree(attribute_list, attribute_name)

    print("tree generated")



    print(tree)

    with open(test_file) as f:
        test_input = f.readlines()
    test_input = [d.strip() for d in test_input]
    test_input.pop(0)
    test_data = [[]]
    for line in test_input:
        test_data.append(line.split("\t"))
    test_data.remove([])

    f = open(output_file,"w")
    del attribute_name[attribute_name.index(decision_label)]
    for name in attribute_name:
        f.write(name + "\t")
    f.write(decision_label+"\n")
    randpick = 0
    for entry in test_data:
        tempDict = tree.copy()
        result = ""
        while (isinstance(tempDict, dict)):
            root = TreeNode.TreeNode(list(tempDict.keys())[0], tempDict[list(tempDict.keys())[0]])
            tempDict = tempDict[list(tempDict.keys())[0]]
            index = attribute_name.index(root.value)
            value = entry[index]
            if (value in list(tempDict.keys())):
                child = TreeNode.TreeNode(value, tempDict[value])
                result = tempDict[value]
                tempDict = tempDict[value]
            else:
#                result = random.choice(['unacc','acc','good','vgood'])
                result = "?"
                randpick += 1
                break
        for i in entry:
            f.write(i+"\t")
        f.write(result+"\n")

    f.close()
    print(randpick)

if __name__ == '__main__':
    main()