import sys
import csv
import os, shutil
import random
import json


num_of_rows = int(sys.argv[1])
try:
    num_of_cols = int(sys.argv[2])
except IndexError:
    num_of_cols = 2
data = list()
with open('covtype.data') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    init = True
    idx = 0
    haha = list()
    for row in readCSV:
        data.append(row[0:10])
        idx+=1
# with open('datasets/attribute.json') as f:
#     attribute = list(json.load(f))

r = list(range(len(data)))
random.shuffle(r)
#res = list()
#res.append(attribute[0:2+num_of_cols])
idx = 0
for i in r[0:num_of_rows]:
    res_temp = [idx+1, "R"+str(idx+1)]
    res_temp += list(map(int,data[i][0:num_of_cols]))
    res.append(res_temp)
    idx+=1
with open("FORESTER_"+str(num_of_rows)+"_"+str(num_of_cols)+".csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(res)