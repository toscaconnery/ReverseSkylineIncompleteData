import sys
import random
from math import ceil

d = 4
n = 2000

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

sys.stdout = open("T_D" + str(d) + "_N" + str(data_number_on_title) + ".txt", "wt")
random.seed(122)

missing_persentage = 20

for i in range(0,n):
    base = random.uniform(0,1)
    basedim = ceil(base / (1/d))-1
    basedata = random.uniform(0, 1)
    row = 'T'
    row += '%d' % (i+1+100)

    for dim in range(0,d):
        ran = random.randint(1,100)
        if ran <= missing_persentage:
            row += ' null'
        else:
            row += ' %d' % random.randint(100,150)
    print(row)


