import sys
import csv
import os, shutil
import random
import json
from math import ceil

random.seed(122)

d = 4
n = 30000

#title
data_number_on_title = ""
thousands = False
number = n
if(n >= 1000):
    thousands = True
    number = int(n / 1000)
data_number_on_title = str(number)
if(thousands == True):
    data_number_on_title += "K"

sys.stdout = open("TESTING_FC_D" + str(d) + "_N" + str(data_number_on_title) + ".txt", "wt")

max_d = []
min_d = []
normal = []
for i in range(0,d):
    max_d.append(0.0)
    min_d.append(999999.0)
    normal.append('null')

data_list = []
filtered_row_data_line = []

missing_persentage = 20

fp = open('covtype.data')
for line in fp:
    may_null = 2
    row = ''
    data_line = line.split(',')
    filtered_data_line = list(data_line[0:d])

    #print(filtered_data_line)
    
    #menyimpan data ke list untuk digunakan nanti
    data_list.append(filtered_data_line)


filtered_row_data_line = list(data_list[0:n])

for data_index in range(0, n):
    #mencari max dan min untuk tiap dimensi
    for i in range(0,d):
        filtered_row_data_line[data_index][i] = float(filtered_row_data_line[data_index][i])
        # print(filtered_row_data_line[data_index][i])
        # print(max_d[i])
        # print("-------")
        if(filtered_row_data_line[data_index][i] > max_d[i]):
            max_d[i] = filtered_row_data_line[data_index][i]
        if(filtered_row_data_line[data_index][i] < min_d[i]):
            min_d[i] = filtered_row_data_line[data_index][i]

# print("max : " + str(max_d))
# print("min : " + str(min_d))

# print("prev : " + str(filtered_row_data_line))



for data_index in range(0, n):
    may_null = 1
    for i in range(0,d):
        ran = random.randint(1,100)
        if ran < missing_persentage:
            if(may_null > 0):
                filtered_row_data_line[data_index][i] = 'null'
                may_null -= 1
            else:
                filtered_row_data_line[data_index][i] = (filtered_row_data_line[data_index][i] - min_d[i])/(max_d[i] - min_d[i]) * 100
                filtered_row_data_line[data_index][i] = round( filtered_row_data_line[data_index][i],1)

        else:
            filtered_row_data_line[data_index][i] = (filtered_row_data_line[data_index][i] - min_d[i])/(max_d[i] - min_d[i]) * 100
            filtered_row_data_line[data_index][i] = round( filtered_row_data_line[data_index][i],1)
# print("afte : " + str(filtered_row_data_line))

for data_index in range(0, n):
    row = "F" + str(data_index+1)
    for i in range(0, d):
        row += " " + str(filtered_row_data_line[data_index][i])
    print(row)

#with open('small_covetype.txt') as csvfile:
    #readCSV = csv.reader(csvfile, delimiter=',')

    # for row in readCSV:
    #     data.append(row[0:10])
    #     idx+=1
# with open('datasets/attribute.json') as f:
#     attribute = list(json.load(f))

# r = list(range(len(data)))
# random.shuffle(r)
# #res = list()
# #res.append(attribute[0:2+num_of_cols])
# idx = 0
# for i in r[0:num_of_rows]:
#     res_temp = [idx+1, "R"+str(idx+1)]
#     res_temp += list(map(int,data[i][0:num_of_cols]))
#     res.append(res_temp)
#     idx+=1
# with open("FORESTER_"+str(num_of_rows)+"_"+str(num_of_cols)+".csv", "w") as output:
#     writer = csv.writer(output, lineterminator='\n')
#     writer.writerows(res)