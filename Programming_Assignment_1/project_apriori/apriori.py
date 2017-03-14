#Data Science Programming Assignment 1 : apriori algorithm
#author : Seonha Park

#TODO : change minsup and filenames raw string to parameter
minsup_param = 5
input_file = "../input.txt"
output_file = "output.txt"
minsup = minsup_param / 100

#change item_set between list and string {[item_id],[item_id],...[item_id]}
def list_to_str(item_set):
	format = "{"
	for id in item_set:
		format = format+str(id)
		format+= ","
	format = format[:-1]
	format+= "}"
	return format

def str_to_list(str_list):
	str_list = str_list[1:-1]
	new_list = list(map(int, str_list.split(",")))
	return new_list


#open input data file and store in transaction list
with open(input_file) as f:
	input_data = f.readlines()
input_data = [d.strip() for d in input_data]

#parse each input lines to item_ids and get the number of total transactions
transactions = []
total_trans = 0
for input_line in input_data:
	trans_list = list(map(int, input_line.split("\t")))
	transactions.append(trans_list)
	total_trans+=1

#check input
#for t in transactions:
#	print(t)
#print("total transactions : " + str(total_trans))

#Start apriori algorithm
"""
Apriori Pseoudo-Code
C_k : candidate itemset of size k
L_k : frequent itemset of size k

C_1 = find 1-itemsets by scanning database
L_1 = find 1-frequent itemsets by pruning C_1

for(k=2 ; L_k != NULL ; k++) do begin
	C_k = candidates generated from L_k-1 by joining L_k-1 with itself
	for each transaction t do
	increment the count of each candidate in C_k which are contained in t
	L_k = candidates in C_k with minsup
	end
return U ^ k _ L_k
"""

cand = []
freq = []

#make C_1 (1-candidate itemset) by scanning transactions
#since list cannot be key of dictionary in python3, I changed sorted itemset to string
cand_1 = {}
for trans in transactions:
	for id in trans:
		itemset = []
		itemset.append(id)
		itemset_key = list_to_str(itemset)
		if itemset_key not in cand_1:
			cand_1[itemset_key] = 1
		else :
			cand_1[itemset_key]+= 1
cand.append(cand_1)

#make L_1 (1-frequent itemset) by pruning C_1
freq_1 = {}
for key, value in cand_1.items():
	if value/total_trans >= minsup :
		freq_1[key] = value
freq.append(freq_1)


k = 2

#for(k=2 ; L_k != empty set ; k++)
while k < total_trans and len(freq[k-2]) != 0 :
#make cand_k(C_k) from freq_km(L_k-1) joining itself
	cand_k = {}
	freq_km = freq[k-2]
	joined_fkm = []
	for k1, v1 in freq_km.items():
		for k2, v2 in freq_km.items():
			kj_s = set(str_to_list(k1)).union(set(str_to_list(k2)))
			kj_l = list(kj_s)
			kj_l.sort()
			if len(kj_l) != k:
				continue
			else :
				if list_to_str(kj_l) not in joined_fkm :
					joined_fkm.append(list_to_str(kj_l))
				else :
					continue
	for j_set in joined_fkm:
		cand_k[j_set] = 0

#for each transactions
#increment the count of each candidate in C_k which are contained in t
	for candidate , value in cand_k.items():
		cand_list = str_to_list(candidate)
		for transact in transactions:
			if len(list(set(cand_list).difference(set(transact)))) == 0:
				cand_k[candidate] += 1

#make freq_k(L_k) in cand_k(C_k) with minsup
	freq_k = {}
	for candidate, value in cand_k.items():
		if cand_k[candidate] / total_trans >= minsup:
			freq_k[candidate] = value

	cand.append(cand_k)
	freq.append(freq_k)
	k+= 1


#check freq list
for f in freq:
	print(f)


#make association rule
