import sys
import random
import csv
import math

def antDataset(d, n):
    dataset = []
    header = []
    for i in range(d):
        header.append("att"+str(i+1))
    dataset.append(header)
    if d == 2:
        for i in range(n):
            x = random.randint(0, 100)
            y = 100 - x + random.randint(-15,15)
            if y > 100 : y = 100
            elif y < 0 : y = 0
            dataset.append([x,y])
    else:
        for i in range(n):
            row = [0] * d
            pivot = random.randint(0, d-1)
            row[pivot] = random.randint(0, 100)
            for j in range(d):
                if j != pivot:
                    y = 100 - row[pivot] + random.randint(-15, 15)
                    if y > 100 : y = 100
                    elif y < 0 : y = 0
                    row[j] = y
            dataset.append(row)
    return dataset

def indDataset(d, n):
    dataset = []
    header = []
    for i in range(d):
        header.append("att"+str(i+1))
    dataset.append(header)
    for i in range(n):
        row = []
        for j in range(d):
            row.append(random.randint(0,100))
        dataset.append(row)
    return dataset

def fcDataset(d, n):
    dataset = []
    filename = "covtype_small.data"
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        counter = 0
        max_att = [-sys.maxint] * d
        min_att = [sys.maxint] * d
        for row in reader:
            row_int = list()
            for i in range(d):
                print row[i],max_att[i],min_att[i]
                row_int.append(int(row[i]))
                max_att[i] = max(max_att[i], row_int[i])
                min_att[i] = min(min_att[i], row_int[i])
            dataset.append(row_int)
            counter += 1
            if counter >= n:
                break
    for row in dataset:
        for i in range(len(row)):
            row[i] = int( math.floor( 100 * float(row[i]-min_att[i]) / (max_att[i]-min_att[i]) ) )
    return dataset

dataset = []

type = (sys.argv[1]).lower()
d = int(sys.argv[2])
n = int(sys.argv[3])
filename = type + "_" + str(d) + "_" + str(n) + ".csv"

if type == "anticorrelated":
    dataset = antDataset(d, n)
elif type == "independent":
    dataset = indDataset(d, n)
elif type == "forestcover":
    dataset = fcDataset(d, n)
else:
    print "data type error"
    sys.exit(0)

print filename
with open(filename, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in dataset:
        csvwriter.writerow(row)