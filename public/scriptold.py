#!/usr/bin/python

import sys
import time
import numpy as np

size_of_vec = 1000
marker = 1
local_skyline = {}
candidate_skyline = {}
global_skyline = {}
shadow_skyline = {}
virtual_points = {}
t = 5

def ReverseSkyline():
	t1 = time.time()
	X = np.arange(size_of_vec)
	Y = np.arange(size_of_vec)
	Z = X - Y
	print( time.time())
	return time.time() - t1

def TestReadFile():
	file_object = open("testread.txt", "r")
	file_content = file_object.read()
	print(file_content + "harusnya sudah new line")
	print("Numpy version : " + np.__version__)

def Testing():
	a = np.arange(10,25,5) 
	print(a)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i

def Insert_Local_Skyline(current_specs, node, current_bit):
	global local_skyline
	#Check apakah current specs didominasi oleh data dalam node N
	#START
	dominating = 1
	if(len(node[current_bit]) == 0):
		#insert the current specs to the node
		node[current_bit].append(current_specs)
	else:
		for i in range(0, len(node[current_bit])):	#pengulangan sebanyak data yang ada didalam node, untuk dibandingkan satu persatu dengan data baru
			dominated_value = 0
			greater_flag = 0
			for j in range(0, len(current_specs)):
				if(marker == 5):
					print(node)
			if(dominated_value == len(current_specs) and greater_flag == 1):
				dominating = 0
				break
	#END
	if(dominating == 1):		#P is not dominated by any points on local_skyline list of N
		local_skyline[current_bit].append(current_specs)
		#delete all real points that are dominated by P from the local_skyline and shadow_skyline list of N
		return True
	else:
		pass
		#if P is dominated only by virtual_point
			#insert P into shadow_skyline list N
			#N.updated_flag = True
			#Delete all points that are dominated by P from the shadow_skyline
	return False




product_specs = np.loadtxt('product_specs.txt', 
							skiprows=1,
							unpack=True)
user_preference = np.loadtxt('user_preference.txt', 
								skiprows=1, 
								unpack=True)

#why_not_points = np.empty((1,1))
#global_skyline = np.empty((1,1))
#candidate_skyline = np.empty((1,1))


for x in range(0, len(user_preference[0])):	#pengulangan sebanyak user preference
	fp = open("all_product.txt")
	bitwise = []
	node = {}
	#local_skyline was initialized here
	shadow_skyline = {}
	virtual_points = {}
	for line in fp:
		current_bit = ""
		current_specs = line.split()
		for i in current_specs:
			if i == "null":
				current_bit = current_bit + "0"
			else:
				current_bit = current_bit + "1"
		bitwise.append(current_bit)
		if current_bit not in node:
			node[current_bit] = []
			local_skyline[current_bit] = []
			shadow_skyline[current_bit] = []
			virtual_points[current_bit] = []
		is_skyline = Insert_Local_Skyline(current_specs, node, current_bit)
	fp.close()




#MAIN LOOPING OF THE ALGORITHM
# for x in range(0, len(user_preference[0])):	#pengulangan sebanya user preference
# 	for i in range(0, len(product_specs)):
# 		print(user_preference[i][x])
# 	print('newline')



# print(product_specs)
# print(' :: ')
# print(user_preference)



#print(product_specs[0][0])

#Testing()
#TestReadFile()
# time_spend = ReverseSkyline()
# print(time_spend)

