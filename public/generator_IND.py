import sys
import random
from math import ceil

d = 4
n = 10000

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

sys.stdout = open("IND_D" + str(d) + "_N" + str(data_number_on_title) + ".txt", "wt")
random.seed(122)

missing_persentage = 20

for i in range(0,n):
    may_null = 2
    base = random.uniform(0,1)
    basedim = ceil(base / (1/d))-1
    basedata = random.uniform(0, 1)
    row = 'T'
    row += '%d' % (i+1+100)

    for dim in range(0,d):
        ran = random.randint(1,100)
        if ran <= missing_persentage:
            if(may_null > 0):
                row += ' null'
                may_null -= 1
            else:
                row += ' %d' % random.randint(0,100)
        else:
            row += ' %d' % random.randint(0,100)
    print(row)


