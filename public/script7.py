#!/usr/bin/python

import sys
import time
import numpy as np

marker = 1
node = {}
local_skyline = {}
candidate_skyline = []
global_skyline = []
shadow_skyline = {}
virtual_point = {}
why_not_points = {}
n_updated_flag = {}
data_length = 0
t = 5
rsl = []
number_of_preference = 0
customer = []
customer_index = 0

def Insert_Local_Skyline(current_specs, current_bit):
	print("Insert_Local_Skyline : " + str(current_specs))
	global local_skyline
	global shadow_skyline
	global virtual_point

	for i in range(0, len(local_skyline[current_bit])):	#pengulangan sebanyak data yang ada didalam local_skyline, untuk dibandingkan satu persatu dengan data baru
		dominating_local = False
		dominated_by_local = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and local_skyline[current_bit][i][j] != 'null'):
				if(current_specs[j] < local_skyline[current_bit][i][j]):
					dominating_local = True
				elif(current_specs[j] > local_skyline[current_bit][i][j]):
					dominated_by_local = True
		if(dominating_local == True and dominated_by_local == False):
			local_skyline[current_bit][i][-1] = 'delete'
		elif(dominating_local == False and dominated_by_local == True):
			for k in range(0, i+1):
				local_skyline[current_bit][k][-1] = 'ok'
			return False
	dominated = 0
	for i in range(0, len(virtual_point[current_bit])):
		dominating_virtual = False
		dominated_by_virtual = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and virtual_point[current_bit][i][j] != 'null'):
				if(current_specs[j] < virtual_point[current_bit][i][j]):
					dominating_virtual = True
				elif(current_specs[j] > virtual_point[current_bit][i][j]):
					dominated_by_virtual = True
		if(dominating_virtual == False and dominated_by_virtual == True):
			dominated = 1
			break
	#if p is dominated only by virtual_point
		#Insert P to shadow_skyline
		#N.updated_flag = True
		#Delete all dominated shadow_skyline
	#else
		#Delete all dominated local_skyline
		#Insert P to local_skyline
		#Delete all dominated shadow_skyline
	#inser
	if(dominated == 0):
		content = list(current_specs)
		content.append('ok')
		local_skyline[current_bit].append(content)
		for i in sorted(local_skyline[current_bit], reverse=True):
			if (i[-1] == 'delete'):
				local_skyline[current_bit].remove(i)
		for i in range(0, len(shadow_skyline[current_bit])):
			dominating_shadow = False
			dominated_by_shadow = False
			for j in range(1, len(current_specs)):
				if(current_specs[j] != 'null' and shadow_skyline[current_bit][i][j] != 'null'):
					if(current_specs[j] < shadow_skyline[current_bit][i][j]):
						dominating_shadow = True
					elif(current_specs[j] > shadow_skyline[current_bit][i][j]):
						dominated_by_shadow = True
			if(dominating_shadow == True and dominated_by_shadow == False):
				shadow_skyline[current_bit][i][-1] = 'delete'
		for i in sorted(shadow_skyline[current_bit], reverse=True):
			if (i[-1] == 'delete'):
				print(">>> Shadow " + str(i) + " removed")
				shadow_skyline[current_bit].remove(i)
		return True
	elif(dominated == 1):
		n_updated_flag[current_bit] = True
		for i in range(0, len(shadow_skyline[current_bit])):
			dominating_shadow = False
			dominated_by_shadow = False
			for j in range(1, len(current_specs)):
				if(current_specs[j] != 'null' and shadow_skyline[current_bit][i][j] != 'null'):
					if(current_specs[j] < shadow_skyline[current_bit][i][j]):
						dominating_shadow = True
					elif(current_specs[j] > shadow_skyline[current_bit][i][j]):
						dominated_by_shadow = True
			if(dominating_shadow == True and dominated_by_shadow == False):
				shadow_skyline[current_bit][i][-1] = 'delete'
		for i in sorted(shadow_skyline[current_bit], reverse=True):
			if (i[-1] == 'delete'):
				print(">>> Shadow " + str(i) + " removed")
				shadow_skyline[current_bit].remove(i)
		content = list(current_specs)
		content.append('ok');
		shadow_skyline[current_bit].append(content)
		print(">>> Shadow " + str(content)  + " appended, data dominated by virtual")
	return False


def Insert_Candidate_Skyline(current_specs, current_bit):
	print("Insert_Candidate_Skyline : " + str(current_specs))
	global candidate_skyline
	list_bit_inserted = []
	dominated = 0

	for i in range(0, len(candidate_skyline)):
		dominating_candidate = False
		dominated_by_candidate = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and candidate_skyline[i][j] != 'null'):
				if(current_specs[j] < candidate_skyline[i][j]):
					dominating_candidate = True
				elif(current_specs[j] > candidate_skyline[i][j]):
					dominated_by_candidate = True
		if(dominating_candidate == True and dominated_by_candidate == False):
			candidate_skyline[i][-1] = 'delete'
			if(candidate_skyline[i][-2] not in list_bit_inserted):
				Insert_Virtual_Point(current_specs, candidate_skyline[i][-2])
				list_bit_inserted.append(candidate_skyline[i][-2])
		elif(dominating_candidate == False and dominated_by_candidate == True):
			content = list(candidate_skyline[i][:-2])
			Insert_Virtual_Point(content, current_bit)
			dominated = 1
	candidate_skyline = [i for i in candidate_skyline if i[-1] == 'ok']
	if(dominated == 0):
		content = list(current_specs)
		content.append(current_bit)
		content.append('ok')
		candidate_skyline.append(content)
		print(">>> Candidate inserted")



def Insert_Virtual_Point(current_specs, current_bit):
	print("Insert_Virtual_Point : " + str(current_specs) + " to " + str(current_bit))
	global local_skyline
	global virtual_point
	global shadow_skyline
	#Move all dominated local_skyline N to shadow_skyline
	for i in range(0, len(local_skyline[current_bit])):
		dominating_local = False
		dominated_by_local = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and local_skyline[current_bit][i][j] != 'null'):
				if(current_specs[j] < local_skyline[current_bit][i][j]):
					dominating_local = True
				elif(current_specs[j] > local_skyline[current_bit][i][j]):
					dominated_by_local = True
		if(dominating_local == True and dominated_by_local == False):
			local_skyline[current_bit][i][-1] = 'delete'

	for i in reversed(local_skyline[current_bit]):
		if (i[-1] == 'delete'):
			print(">>> Local " + str(i) + " moved to shadow")
			shadow_skyline[current_bit].append(i)
			local_skyline[current_bit].remove(i)
			shadow_skyline[current_bit][-1][-1] = 'ok'
	
	#Remove all dominated virtual_point that has same bit
	for i in range(0, len(virtual_point[current_bit])):
		dominating_virtual = False
		dominated_by_virtual = False
		superset_check = 0

		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and virtual_point[current_bit][i][j] != 'null'):
				if(current_specs[j] < virtual_point[current_bit][i][j]):
					dominating_virtual = True
				elif(current_specs[j] > virtual_point[current_bit][i][j]):
					dominated_by_virtual = True
			if(current_specs[j] != 'null'):
				superset_check += 1
			elif(current_specs[j] == 'null' and virtual_point[current_bit][i][j] == 'null'):
				superset_check += 1
		if(dominating_virtual == True and dominated_by_virtual == False and superset_check == len(current_specs)):
			virtual_point[current_bit][i][-1] = 'delete'

	for i in reversed(virtual_point[current_bit]):
		if(i[-1] == 'delete'):
			print(">>> Virtual " + str(i) + " removed")
			virtual_point[current_bit].remove(i)
	content = list(current_specs)
	content.append('ok')
	print(">>> Virtual " + str(content) + " appended")
	virtual_point[current_bit].append(content)


def Update_Global_Skyline():
	print("Update_Global_Skyline")
	global global_skyline
	global candidate_skyline
	global shadow_skyline
	global data_length
	for c in range(0, len(candidate_skyline)):
		for g in range(0, len(global_skyline)):
			dominating_global = False
			dominating_candidate = False
			for i in range(1, data_length):
				if(candidate_skyline[c][i] != 'null' and global_skyline[g][i] != 'null'):
					if(candidate_skyline[c][i] < global_skyline[g][i]):
						dominating_global = True
					elif(candidate_skyline[c][i] > global_skyline[g][i]):
						dominating_candidate = True
			if(dominating_global == True and dominating_candidate == False):
				global_skyline[g][-1] = 'delete'
			elif(dominating_global == False and dominating_candidate == True):
				candidate_skyline[c][-1] = 'delete'

	for i in reversed(global_skyline):
		if(i[-1] == 'delete'):
			print(">>> Global " + str(i) + " removed by candidate")
			global_skyline.remove(i)
	for i in reversed(candidate_skyline):
		if(i[-1] == 'delete'):
			print(">>> Candidate " + str(i) + " removed by global")
			candidate_skyline.remove(i)
	for g in range(0, len(global_skyline)):
		for i in n_updated_flag:
			if (n_updated_flag[i] == True):
				for s in range(0, len(shadow_skyline[i])):
					dominating_global = False
					dominating_shadow = False
					for j in range(1, data_length):
						if(global_skyline[g][j] != 'null' and shadow_skyline[i][s][j] != 'null' ):
							if(global_skyline[g][j] < shadow_skyline[i][s][j]):
								dominating_shadow = True
							elif(global_skyline[g][j] > shadow_skyline[i][s][j]):
								dominating_global = True
					if(dominating_global == True and dominating_shadow == False):
						global_skyline[g][-1] == 'delete'

	for c in range(0, len(candidate_skyline)):
		for i in node:
			for s in range(0, len(shadow_skyline[i])):
				dominating_candidate = False
				dominating_shadow = False
				for j in range(1, data_length):
					if(candidate_skyline[c][j] != 'null' and shadow_skyline[i][s][j] != 'null'):
						if(candidate_skyline[c][j] < shadow_skyline[i][s][j]):
							dominating_shadow = True
						elif(candidate_skyline[c][j] > shadow_skyline[i][s][j]):
							dominating_candidate = True
				if(dominating_candidate == True and dominating_shadow == False):
					candidate_skyline[c][-1] = 'delete'

	for i in reversed(global_skyline):
		if(i[-1] == 'delete'):
			print(">>> Global " + str(i) + " removed by shadow")
			global_skyline.remove(i)
	for i in reversed(candidate_skyline):
		if(i[-1] == 'delete'):
			print(">>> Candidate " + str(i) + " removed by shadow")
			candidate_skyline.remove(i)
	for i in candidate_skyline:
		global_skyline.append(i)
	for i in n_updated_flag:
		n_updated_flag[i] == False


product_specs = np.loadtxt('product_specs.txt', skiprows=1, unpack=True)
user_preference = np.loadtxt('user_preference.txt', skiprows=1, unpack=True)
current_product = np.loadtxt('current_product.txt', skiprows=1, unpack=True)

for x in range(0, len(user_preference[0])):
	fp = open("random_specs.txt")
	node.clear()
	local_skyline.clear()
	candidate_skyline.clear()
	global_skyline.clear()
	shadow_skyline.clear()
	virtual_point.clear()
	indexhelper = 0
	print("")
	print("")
	print("")
	print("")
	number_of_preference += 1
	print("Processing User Preference No : " + str(number_of_preference))
	for line in fp:
		print("")
		print("")
		current_bit = ""
		current_spec = line.split()
		data = []
		transformed_data = []
		transformed_data.append(current_spec[0])
		data.append(current_spec[0])
		data_length = len(current_spec)
		for i in range(1, data_length):
			if(current_spec[i] == "null"):
				current_bit += "0"
				data.append(current_spec[i])
				transformed_data.append(current_spec[i])
			else:
				current_bit += "1"
				difference = abs(float(current_spec[i]) - user_preference[i-1][x])
				data.append(float(current_spec[i]))
				transformed_data.append(float(difference))
		if current_bit not in node:
			node[current_bit] = []
			node[current_bit].append(data)
			local_skyline[current_bit] = []
			shadow_skyline[current_bit] = []
			virtual_point[current_bit] = []
			n_updated_flag[current_bit] = False
		else:
			node[current_bit].append(data)

		# indexhelper += 1
		# print(indexhelper)
		is_skyline = Insert_Local_Skyline(transformed_data, current_bit)
		if is_skyline == True:
			print(">>> Local inserted")
			Insert_Candidate_Skyline(transformed_data, current_bit)
			if(len(candidate_skyline) > t):
				Update_Global_Skyline()
				candidate_skyline.clear()
		print("**************************************************")
		print("local     : " + str(local_skyline))
		print("candidate : " + str(candidate_skyline))
		print("shadow    : " + str(shadow_skyline))
		print("virtual   : " + str(virtual_point))
		print("**************************************************")
	fp.close()
	Update_Global_Skyline()

	#print("global skyline  : " + str(global_skyline))

	print("GLOBAL SKYLINE : " + str(global_skyline))

	for g in global_skyline:
		print(g)

	customer.append(customer_index)
	customer[customer_index] = list(global_skyline)
	customer_index += 1

print(customer)

for c in customer:
	print(c)

	#inputing the result to customer variable
	
	
	
	# for y in n_updated_flag:
	# 	n_updated_flag[y] = False

	#print("")
