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

#make association rule
