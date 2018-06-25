import sys
import random
from math import ceil

sys.stdout = open("T_D4_N100XY.txt", "wt")

random.seed(122)

d = 4
n = 100
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


