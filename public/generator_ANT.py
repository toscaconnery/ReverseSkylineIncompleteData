import sys
import random
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

sys.stdout = open("TESTING_ANT_D" + str(d) + "_N" + str(data_number_on_title) + ".txt", "wt")

missing_persentage = 20

for i in range(0,n):
    base = random.uniform(0,1)
    basedim = ceil(base / (1/d))-1
    basedata = random.uniform(0, 1)
    row = 'A'
    row += '%d' % (i+1)
    may_null = 2
    for dim in range(0,d):
        if dim != basedim:
            ran = random.randint(1, 100)
            if ran <= missing_persentage:
                if(may_null > 0):
                    row += ' null'
                    may_null -= 1
                else:
                    #sama dengan kodingan dibawah
                    baseotherdim = 1 - basedata
                    posneg = random.uniform(0,1)
                    if posneg <= 0.5:
                        addsub = -1 * (0.5 - posneg) * 0.2
                    else:
                        addsub = (posneg - 0.5) * 0.2
                    data = baseotherdim + addsub
                    if data < 0:
                        data = 0.0
                    elif data > 1:
                        data = 1.0
                    row += ' %d' % ceil(data*100)
            else:
                baseotherdim = 1 - basedata
                posneg = random.uniform(0,1)
                if posneg <= 0.5:
                    addsub = -1 * (0.5 - posneg) * 0.2
                else:
                    addsub = (posneg - 0.5) * 0.2
                data = baseotherdim + addsub
                if data < 0:
                    data = 0.0
                elif data > 1:
                    data = 1.0
                row += ' %d' % ceil(data*100)
        else:
            row += ' %d' % ceil(basedata*100)
    print(row)


