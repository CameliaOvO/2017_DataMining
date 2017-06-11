# Data Science Programming Assignment 4 : predict the ratings of movies
# author : Seonha Park
# written in Python3

import sys
import math

def get_sim(user1, user2, intersected, record_list):
    mean_user1 = 0.0
    for item in intersected:
        mean_user1 += record_list[(user1,item)]
    mean_user1 = float(mean_user1)/float(len(intersected))

    mean_user2 = 0.0
    for item in intersected:
        mean_user2 += record_list[(user2,item)]
    mean_user2 = float(mean_user2)/float(len(intersected))

    dist_user1 = 0.0
    dist_list1 = []
    for item in intersected:
        temp = float(record_list[(user1,item)])-mean_user1
        dist_list1.append(temp)
        dist_user1 += math.pow(temp,2.0)
    dist_user1 = math.sqrt(dist_user1)

    dist_user2 = 0.0
    dist_list2 = []
    for item in intersected:
        temp = float(record_list[(user2,item)])-mean_user2
        dist_list2.append(temp)
        dist_user2 += math.pow(temp,2.0)
    dist_user2 = math.sqrt(dist_user2)

    sim_nume = 0.0
    for i,j in zip(dist_list1,dist_list2):
        sim_nume += i*j

    sim_deno = dist_user1 * dist_user2
    if abs(sim_deno) < 0.00001:
        return 1.0


    return sim_nume/sim_deno


def predict(user, item, record_list, user_item, get_intersect,average_common, user_mean,sim_dict,neighbor_dict):
    mean_user = user_mean[user]

    neighbor = []
    for i in neighbor_dict[user]:
        if item in user_item[i]:
            neighbor.append(i)

    sim_list = []
    sim_l_nume = []

    for neigh in neighbor:
        temp = sim_dict[(user,neigh)]
        sim_list.append(temp)
        sim_l_nume.append(temp * (record_list[(neigh,item)] - user_mean[neigh]))

    if len(sim_list) > 0 and sum(sim_list) > 0 :
        result = mean_user + (sum(sim_l_nume)/sum(sim_list))
    else:
        result = mean_user

    if result < 1:
        result = 1
    elif result > 5:
        result = 5
    else:
        result = round(result)

    return result

def main():
    # get command line argument
    train_file = sys.argv[1]
    test_file = sys.argv[2]

    with open(train_file) as f:
        train_data = f.readlines()
    train_data = [d.strip() for d in train_data]

    # make record_list
    record_list = {}
    user_list = []
    item_list = []
    user_list = set(user_list)
    item_list = set(item_list)
    for line in train_data:
        each_line = line.split("\t")
        temp_key = (int(each_line[0]), int(each_line[1]))
        temp_value = int(each_line[2])
        record_list[temp_key] = temp_value
        user_list.add(int(each_line[0]))
        item_list.add(int(each_line[1]))

    # make user_item
    user_item = {}
    user_mean = {}
    for user in user_list:
        mean = 0.0
        for item in item_list:
            if(user,item) in record_list:
                if user in user_item.keys():
                    user_item[user].append(item)
                    mean += record_list[(user,item)]
                else:
                    user_item[user] = []
                    user_item[user].append(item)
        mean = float(mean) / float(len(user_item[user]))
        user_mean[user] = mean



    # make get_intersect and get common average
    nume = 0
    deno = 0
    get_intersect = {}
    for k1, v1 in user_item.items():
        for k2, v2 in user_item.items():
            if k1 != k2:
                intersected = set(user_item[k1]).intersection((user_item[k2]))
                get_intersect[(k1,k2)] = intersected
                nume += len(intersected)
                deno += 1

    average_common = int(float(nume)/float(deno))

    # make sim dict
    sim_dict = {}
    for k,v in get_intersect.items():
        if len(v) > average_common:
            sim_dict[k] = get_sim(k[0],k[1],v,record_list)

    # make neighbor dict
    neighbors = {}
    for user1 in user_list:
        for user2 in user_list:
            if user1 != user2 :
                if len(get_intersect[(user1,user2)]) > average_common:
                    if user1 in neighbors.keys():
                        neighbors[user1].append(user2)
                    else:
                        neighbors[user1] = []
                        neighbors[user1].append(user2)
        if user1 not in neighbors.keys():
            neighbors[user1] = []

    #start test
    with open(test_file) as f:
        test_data = f.readlines()
    test_data = [d.strip() for d in test_data]

    test_list = []
    for line in test_data:
        each_line = line.split("\t")
        temp_tuple = (int(each_line[0]), int(each_line[1]))
        test_list.append(temp_tuple)


    output_file = train_file+"_prediction.txt"
    out_f = open(output_file,"w")
    for test in test_list:
        out_f.write(str(test[0])+"\t"+str(test[1])+"\t")
        out_f.write(str(predict(test[0],test[1],record_list,user_item,get_intersect,average_common,user_mean,sim_dict,neighbors)))
        out_f.write("\n")
    out_f.close()



if __name__ == '__main__':
    main()
