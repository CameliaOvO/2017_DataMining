# Data Science Programming Assignment 2 : decision tree
# author : Seonha Park
# written in Python3
import DecisionTree
import TreeNode
import sys

#get label which has largest value. to estimate non-leaf ended entry
def getMaxLabel(parent_attr, this_attr, root_attr):
    max_array = []
    max_val = 0
    #find largest number label
    for k , v in this_attr["num"].items():
        if v > max_val:
            max_array = []
            max_array.append(k)
            max_val = v
        elif v == max_val:
            max_array.append(k)

    #if two or more label has same value, find parent node's largest label
    if len(max_array) > 1:
        parent_max = 0
        parent_array = []
        for k, v in parent_attr["num"].items():
            if v > parent_max:
                parent_array = []
                parent_array.append(k)
                parent_max = v
            elif v == parent_max:
                parent_array.append(k)
        #if two or more label has same value in parent node, find root node's largest label
        if len(parent_array) > 1:
            root_array = []
            root_val = 0
            for k, v in root_attr["num"].items():
                if v > root_val:
                    root_array = []
                    root_array.append(k)
                    root_val = v
                elif v == root_val:
                    root_array.append(k)
            return root_array[0]
        else :
            return parent_array[0]
    else:
        return max_array[0]


def main():
    # get training file, test file and output file's name from command line argument
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    output_file = sys.argv[3]

    # get training file and make list of columns
    with open(train_file) as f:
        train_data = f.readlines()
    train_data = [d.strip() for d in train_data]

    # make train_data string to attribute list and get each attribute name and total number of columns
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

    print(possible_name)

    # get decision class's label and generate tree
    decision_label = attribute_name[len(attribute_name) - 1]
    tree = DecisionTree.GenerateTree(attribute_list, attribute_name)

    # get test input from test file
    with open(test_file) as f:
        test_input = f.readlines()
    test_input = [d.strip() for d in test_input]
    test_input.pop(0)
    test_data = [[]]
    for line in test_input:
        test_data.append(line.split("\t"))
    test_data.remove([])

    # predict decision class and write in output file
    f = open(output_file,"w")
    del attribute_name[attribute_name.index(decision_label)]
    for name in attribute_name:
        f.write(name + "\t")
    f.write(decision_label+"\n")
    for entry in test_data:
        # call decision tree
        tempDict = tree.copy()
        parentDict = tempDict
        rootDict = tree.copy()
        rootDict = rootDict[list(rootDict.keys())[0]]
        result = ""
        # trace tree while the answer is found or tree is end
        while isinstance(tempDict, dict):
            root = TreeNode.TreeNode(list(tempDict.keys())[0], tempDict[list(tempDict.keys())[0]])

            tempDict = tempDict[list(tempDict.keys())[0]]
            index = attribute_name.index(root.value)
            value = entry[index]

            if (value in list(tempDict.keys())):
                child = TreeNode.TreeNode(value, tempDict[value])
                result = tempDict[value]
                parentDict = tempDict
                tempDict = tempDict[value]
            # can't find the entry in tree, follow majority vote
            else:
                result = getMaxLabel(parentDict, tempDict,rootDict)
                break
        for i in entry:
            f.write(i+"\t")
        f.write(result+"\n")
    f.close()

if __name__ == '__main__':
    main()