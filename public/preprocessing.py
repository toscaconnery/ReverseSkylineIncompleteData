#!/usr/bin/python

import sys
import numpy as np

start_time = time.time()

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
safe_region = []
number_of_preference = 0
customer_skyline = {}
customer_index = 0
query_point = []
list_customer = []
ct = []
ct_has_skyline = True
product_list = "TESTING_FC_D3_N100.txt"
user_preference = "TESTING_USER_D3_N10.txt"
intersection = []
ct_cost = []
q_cost = []
jumlah_rsl = 0
list_rsl = []


def insert_local_skyline(current_specs, bitmap):
	global local_skyline
	global shadow_skyline
	global virtual_point

	for i in range(0, len(local_skyline[bitmap])):
		dominating_local = False
		dominated_by_local = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and local_skyline[bitmap][i][j] != 'null'):
				if(current_specs[j] < local_skyline[bitmap][i][j]):
					dominating_local = True
				elif(current_specs[j] > local_skyline[bitmap][i][j]):
					dominated_by_local = True
		if(dominating_local == True and dominated_by_local == False):
			local_skyline[bitmap][i][-1] = 'delete'
		elif(dominating_local == False and dominated_by_local == True):
			for k in range(0, i+1):
				local_skyline[bitmap][k][-1] = 'ok'
			return False
	dominated = 0
	for i in range(0, len(virtual_point[bitmap])):
		dominating_virtual = False
		dominated_by_virtual = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and virtual_point[bitmap][i][j] != 'null'):
				if(current_specs[j] < virtual_point[bitmap][i][j]):
					dominating_virtual = True
				elif(current_specs[j] > virtual_point[bitmap][i][j]):
					dominated_by_virtual = True
		if(dominating_virtual == False and dominated_by_virtual == True):
			dominated = 1
			break
	if(dominated == 0):
		content = list(current_specs)
		content.append('ok')
		local_skyline[bitmap].append(content)
		for i in sorted(local_skyline[bitmap], reverse=True):
			if (i[-1] == 'delete'):
				local_skyline[bitmap].remove(i)
		for i in range(0, len(shadow_skyline[bitmap])):
			dominating_shadow = False
			dominated_by_shadow = False
			for j in range(1, len(current_specs)):
				if(current_specs[j] != 'null' and shadow_skyline[bitmap][i][j] != 'null'):
					if(current_specs[j] < shadow_skyline[bitmap][i][j]):
						dominating_shadow = True
					elif(current_specs[j] > shadow_skyline[bitmap][i][j]):
						dominated_by_shadow = True
			if(dominating_shadow == True and dominated_by_shadow == False):
				shadow_skyline[bitmap][i][-1] = 'delete'
		for i in sorted(shadow_skyline[bitmap], reverse=True):
			if (i[-1] == 'delete'):
				shadow_skyline[bitmap].remove(i)
		return True
	elif(dominated == 1):
		n_updated_flag[bitmap] = True
		for i in range(0, len(shadow_skyline[bitmap])):
			dominating_shadow = False
			dominated_by_shadow = False
			for j in range(1, len(current_specs)):
				if(current_specs[j] != 'null' and shadow_skyline[bitmap][i][j] != 'null'):
					if(current_specs[j] < shadow_skyline[bitmap][i][j]):
						dominating_shadow = True
					elif(current_specs[j] > shadow_skyline[bitmap][i][j]):
						dominated_by_shadow = True
			if(dominating_shadow == True and dominated_by_shadow == False):
				shadow_skyline[bitmap][i][-1] = 'delete'
		for i in sorted(shadow_skyline[bitmap], reverse=True):
			if (i[-1] == 'delete'):
				shadow_skyline[bitmap].remove(i)
		content = list(current_specs)
		content.append('ok');
		shadow_skyline[bitmap].append(content)
	return False


def insert_candidate_skyline(current_specs, bitmap):
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
				insert_virtual_point(current_specs, candidate_skyline[i][-2])
				list_bit_inserted.append(candidate_skyline[i][-2])
		elif(dominating_candidate == False and dominated_by_candidate == True):
			content = list(candidate_skyline[i][:-2])
			insert_virtual_point(content, bitmap)
			dominated = 1
	candidate_skyline = [i for i in candidate_skyline if i[-1] == 'ok']
	if(dominated == 0):
		content = list(current_specs)
		content.append(bitmap)
		content.append('ok')
		candidate_skyline.append(content)



def insert_virtual_point(current_specs, bitmap):
	global local_skyline
	global virtual_point
	global shadow_skyline
	#MEMBANDINGKAN DENGAN LOCAL SKYLINE
	#Move all dominated local_skyline N to shadow_skyline
	for i in range(0, len(local_skyline[bitmap])):
		dominating_local = False
		dominated_by_local = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and local_skyline[bitmap][i][j] != 'null'):
				if(current_specs[j] < local_skyline[bitmap][i][j]):
					dominating_local = True
				elif(current_specs[j] > local_skyline[bitmap][i][j]):
					dominated_by_local = True
		if(dominating_local == True and dominated_by_local == False):
			local_skyline[bitmap][i][-1] = 'delete'
	for i in reversed(local_skyline[bitmap]):
		if (i[-1] == 'delete'):
			shadow_skyline[bitmap].append(i)
			local_skyline[bitmap].remove(i)
			shadow_skyline[bitmap][-1][-1] = 'ok'
	
	for i in range(0, len(virtual_point[bitmap])):
		dominating_virtual = False
		dominated_by_virtual = False
		superset_check = 0

		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and virtual_point[bitmap][i][j] != 'null'):
				if(current_specs[j] < virtual_point[bitmap][i][j]):
					dominating_virtual = True
				elif(current_specs[j] > virtual_point[bitmap][i][j]):
					dominated_by_virtual = True
			if(current_specs[j] != 'null'):
				superset_check += 1
			elif(current_specs[j] == 'null' and virtual_point[bitmap][i][j] == 'null'):
				superset_check += 1
		if(dominating_virtual == True and dominated_by_virtual == False and superset_check == len(current_specs)):
			virtual_point[bitmap][i][-1] = 'delete'

	for i in reversed(virtual_point[bitmap]):
		if(i[-1] == 'delete'):
			virtual_point[bitmap].remove(i)
	content = list(current_specs)
	content.append('ok')
	virtual_point[bitmap].append(content)


def update_global_skyline():
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
			global_skyline.remove(i)
	for i in reversed(candidate_skyline):
		if(i[-1] == 'delete'):
			candidate_skyline.remove(i)
	for g in range(0, len(global_skyline)):
		for i in n_updated_flag:
			if (n_updated_flag[i] == True and i in shadow_skyline):
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
			global_skyline.remove(i)
	for i in reversed(candidate_skyline):
		if(i[-1] == 'delete'):
			candidate_skyline.remove(i)
	for i in candidate_skyline:
		global_skyline.append(i)

	for i in n_updated_flag:
		n_updated_flag[i] == False



def calculate_rsl_q(customer_skyline, query_point):
	global data_length
	for dict_index in customer_skyline:
		transformed_query_point = []
		for q in range(0, data_length):
			transformed_value = abs(float(query_point[q+1]) - customer_skyline[dict_index][-2][q])
			transformed_query_point.append(transformed_value)
		for data_index in range(0, len(customer_skyline[dict_index]) - 2):
			dominating_q = False
			dominating_customer = False
			for i in range(0, data_length):
				if(customer_skyline[dict_index][data_index][i+1] != 'null'):
					if(customer_skyline[dict_index][data_index][i+1] < transformed_query_point[i]):
						dominating_q = True
					elif(customer_skyline[dict_index][data_index][i+1] > transformed_query_point[i]):
						dominating_customer = True
			if(dominating_q == True and dominating_customer == False):
				customer_skyline[dict_index][-1] = 'delete'
			elif(dominating_q == False and dominating_customer == True):
				customer_skyline[dict_index][data_index][-1] = 'delete'
		if(customer_skyline[dict_index][-1] == 'ok'):
			for i in range(len(customer_skyline[dict_index]) - 3, -1, -1):
				if(customer_skyline[dict_index][i][-1] == 'delete'):
					customer_skyline[dict_index].remove(customer_skyline[dict_index][i])
		if(len(customer_skyline[dict_index]) <= 2):
			customer_skyline[dict_index][-1] = 'delete'
	return customer_skyline


def Prepare_Data(line, customer):
	global bitmap
	global node
	global local_skyline
	global candidate_skyline
	global global_skyline
	global shadow_skyline
	global virtual_point
	global n_updated_flag
	global data_length

	current_spec = line.split()
	data = []
	transformed_data = []
	transformed_data.append(current_spec[0])
	data.append(current_spec[0])
	for i in range(1, data_length+1):
		if(current_spec[i] == "null"):
			bitmap += "0"
			data.append(current_spec[i])
			transformed_data.append(current_spec[i])
		else:
			bitmap += "1"
			difference = abs(float(current_spec[i]) - customer[i-1])
			data.append(float(current_spec[i]))
			transformed_data.append(float(difference))
	if bitmap not in node:
		node[bitmap] = []
		local_skyline[bitmap] = []
		shadow_skyline[bitmap] = []
		virtual_point[bitmap] = []
		n_updated_flag[bitmap] = False
	return transformed_data


data_length = len(ct)
fu = open(user_preference)
for list_user in fu:
	temp = [float(x) for x in list_user.split()]
	list_customer.append(temp)

for x in range(0, len(list_customer)):
	fp = open(product_list)
	node.clear()
	local_skyline.clear()
	candidate_skyline.clear()
	global_skyline.clear()
	shadow_skyline.clear()
	virtual_point.clear()
	number_of_preference += 1
	for line in fp:
		bitmap = ""
		transformed_data = Prepare_Data(line, list_customer[x])
		is_skyline = insert_local_skyline(transformed_data, bitmap)
		if is_skyline == True:
			insert_candidate_skyline(transformed_data, bitmap)
			if(len(candidate_skyline) > t):
				update_global_skyline()
				candidate_skyline.clear()
	fp.close()
	update_global_skyline()
	if(len(global_skyline) > 0):
		customer_skyline[str(customer_index)] = list(global_skyline)
		customer_skyline[str(customer_index)].append(list(list_customer[x]))
		customer_skyline[str(customer_index)].append("ok")
		customer_index += 1
fu.close()
ddr_prime_ct = generate_ddr_prime_ct(ct)
safe_region = generate_safe_region_q()


if(ct_has_skyline == True):
	intersection_status = check_intersection(safe_region, ddr_prime_ct)
else:
	intersection_status = False
if(intersection_status == True):
	move_query_point()
else:
	Move_Why_Not_And_Query_Point()