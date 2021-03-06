# Data Science Programming Assignment 1 : apriori algorithm
# author : Seonha Park
# written in Python3

import sys

#to change raw input to command line argument
minsup_param = int(sys.argv[1])
input_file = sys.argv[2]
output_file = sys.argv[3]

minsup = minsup_param / 100

# change item_set between list and string {[item_id],[item_id],...[item_id]}
def list_to_str(item_set):
    brace = "{"
    for item_id in item_set:
        brace = brace + str(item_id)
        brace += ","
    brace = brace[:-1]
    brace += "}"
    return brace

def str_to_list(str_list):
    str_list = str_list[1:-1]
    new_list = list(map(int, str_list.split(",")))
    return new_list


# make subset of itemset
def jin_subset(item_set):
    result_set = [[]]
    for x in item_set:
        result_set.extend([y + [x] for y in result_set])
    # this is empty set
    result_set.pop(0)
    # this is not proper-subset
    result_set.pop(len(result_set)-1)
    for it in result_set:
        it.sort()
    return result_set


# return 1 if set1 and set2 is same set, return 0 other case
def set_comp(set1, set2):
    result = 0
    if len(set(set1).difference(set(set2))) == 0:
        if len(set(set2).difference(set(set1))) == 0:
            result = 1
    return result

#change round function because python round is not sa-sa-o-ip
def new_round(num):
    new_num = num*1000
    #if num is 13.255 -> new num is 13255
    over_num = int(new_num/1000)
    first_num = int((new_num%1000)/100)
    second_num = int((new_num%100)/10)
    third_num = int(new_num%10)
    upper = 0
    if third_num >= 5:
        second_num = second_num + 1
    if second_num > 9:
        second_num = second_num - 10
        first_num = first_num + 1
    if first_num > 9:
        first_num = first_num - 10
        upper = 1

    ret_num = int(over_num) + int(upper) + round(float(first_num/10),1) + round(float(second_num/100),2)
    ret_num = round(ret_num,2)
    return ret_num


# open input data file and store in transaction list
with open(input_file) as f:
    input_data = f.readlines()
input_data = [d.strip() for d in input_data]

# parse each input lines to item_ids and get the number of total transactions
transactions = []
total_trans = 0
for input_line in input_data:
    trans_list = list(map(int, input_line.split("\t")))
    transactions.append(trans_list)
    total_trans += 1


# Start apriori algorithm
cand = []
freq = []

# make C_1 (1-candidate itemset) by scanning transactions
# since list cannot be key of dictionary in python3, I changed sorted itemset to string
cand_1 = {}
for trans in transactions:
    for item_id in trans:
        itemset = []
        itemset.append(item_id)
        itemset_key = list_to_str(itemset)
        if itemset_key not in cand_1:
            cand_1[itemset_key] = 1
        else:
            cand_1[itemset_key] += 1
cand.append(cand_1)

# make L_1 (1-frequent itemset) by pruning C_1
freq_1 = {}
for key, value in cand_1.items():
    if value / total_trans >= minsup:
        freq_1[key] = value
freq.append(freq_1)


k = 2

# for(k=2 ; L_k != empty set ; k++)
while k <= total_trans and len(freq[k - 2]) != 0:
    # make cand_k(C_k) from freq_km(L_k-1) joining itself and pruning
    cand_k = {}
    freq_km = freq[k - 2]

    # self-joining step
    joined_fkm = []
    for k1, v1 in freq_km.items():
        for k2, v2 in freq_km.items():
            kj_s = set(str_to_list(k1)).union(set(str_to_list(k2)))
            kj_l = list(kj_s)
            kj_l.sort()
            if len(kj_l) != k:
                continue
            else:
                if list_to_str(kj_l) not in joined_fkm:
                    joined_fkm.append(list_to_str(kj_l))
                else:
                    continue

    # pruning step
    # check its subset in freq_km, freq_kmm ...
    # make each joined_fkm's non-empty subset
    pruned_fkm = []
    for j_set in joined_fkm:
        subs_fkm = jin_subset(str_to_list(j_set))
        prune = -1
        for subset in subs_fkm:
            prune = 1
            for fset in freq:
                for key_fset , val_fset in fset.items():
                    if set_comp(str_to_list(key_fset), subset) == 1:
                        prune = 0
            if prune == 1:
                break
        if prune == 1:
            continue
        else :
            pruned_fkm.append(j_set)
    for p_set in pruned_fkm:
        cand_k[p_set] = 0

    # for each transactions
    # increment the count of each candidate in C_k which are contained in t
    for candidate, value in cand_k.items():
        cand_list = str_to_list(candidate)
        for transact in transactions:
            if len(list(set(cand_list).difference(set(transact)))) == 0:
                cand_k[candidate] += 1

    # make freq_k(L_k) in cand_k(C_k) with minsup
    freq_k = {}
    for candidate, value in cand_k.items():
        if cand_k[candidate] / total_trans >= minsup:
            freq_k[candidate] = value

    cand.append(cand_k)
    freq.append(freq_k)
    k += 1

# since last frequent set is empty set (while terminology condition)
freq.pop(len(freq)-1)


out_f = open(output_file, "w")


# make association rule

# decompose freq(list of list of dictionary -> list of itemset list)
# except 1-frequent itemset

decomp_freq_dic = {}
decomp_freq = []
for fset in freq:
    for key, value in fset.items():
        if len(str_to_list(key)) > 1:
            decomp_freq.append(str_to_list(key))
        decomp_freq_dic[key] = value

#make association rules with each subset and write in output file
for fset in decomp_freq:
    set_size = len(fset)
    all_subset = jin_subset(fset)
    for subset in all_subset:
        lhs = subset
        rhs = list(set(fset).difference(set(lhs)))
        rhs.sort()

        s = decomp_freq_dic[list_to_str(fset)] / total_trans
        c = (decomp_freq_dic[list_to_str(fset)] / total_trans) / (decomp_freq_dic[list_to_str(list(lhs))] / total_trans)
        s *= 100
        c *= 100
        out_f.write(list_to_str(list(lhs)) + "\t" + list_to_str(list(rhs)) + "\t" + str(new_round(s)) + "\t" + str(new_round(c))+"\n")
