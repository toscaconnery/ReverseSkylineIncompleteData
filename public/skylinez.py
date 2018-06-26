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
safe_region = []
number_of_preference = 0
customer_skyline = {}
customer_index = 0
query_point = []
list_customer = []
ct = []
#product_list = "random_specs.txt"
#product_list = "mwq_data.txt"
product_list = "testing_product_list.txt"
user_preference = "testing_user_preference.txt"
intersection = []
ct_cost = []
q_cost = []
jumlah_rsl = 0
list_rsl = []

def insert_local_skyline(current_specs, bitmap):
	global local_skyline
	global shadow_skyline
	global virtual_point

	for i in range(0, len(local_skyline[bitmap])):	#pengulangan sebanyak data yang ada didalam local_skyline, untuk dibandingkan satu persatu dengan data baru
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
	
	#MEMBANDINGKAN DENGAN VIRTUAL POINT
	#Remove all dominated virtual_point that has same bit
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


def generate_query_point(): #NEW
	global query_point
	#query_point = "QP 6 2 1 3"
	#query_point = "QP 15 8 5 26"
	#query_point = "QP 90 80 80 80"
	#query_point = "QP 45 40 44 41"
	#query_point = "QP 7 5 7 8"
	#query_point = "QP 15 15 15 15"
	#query_point = "QP 4 6 8 4"

	########
	#query_point = "QP 45 40 44 41" 	#sampel yang bisa, ct : 23, 34.5, 24, 33, data : new_data.txt
	#query_point = "QP 45 26 18 25"
	########

	########
	#query_point = "QP 90 80 80 80"
	#query_point = "QP 38 67 47 33"
	########

	########
	query_point = "QP 80 80 80 80"
	#query_point = "QP 70 69 71 69"
	########

def generate_ct():
	global ct
	# ct.append(float(23))
	# ct.append(float(53))
	# ct.append(float(24))
	# ct.append(float(30))

	# ct.append(float(23))
	# ct.append(float(34.5))
	# ct.append(float(24))
	# ct.append(float(33))
	

	#moving_why_not_and_query_point, q : [80, 80, 80, 80]
	# ct.append(float(23))
	# ct.append(float(20))
	# ct.append(float(24))
	# ct.append(float(25))
	#TO
	ct.append(float(76.5))
	ct.append(float(77.5))
	ct.append(float(79.5))
	ct.append(float(78))


	# ct.append(float(23))
	# ct.append(float(34.5))
	# ct.append(float(24))
	# ct.append(float(33))
	# ct.append(2)
	# ct.append(5)
	# ct.append(8)
	# ct.append(2)

def generate_cost():
	global ct_cost
	global q_cost
	ct_cost.append(3)
	ct_cost.append(3)
	ct_cost.append(3)
	ct_cost.append(2)
	q_cost.append(4)
	q_cost.append(3)
	q_cost.append(2)
	q_cost.append(3)

def calculate_rsl_q(customer_skyline, query_point):
	### - MENGHAPUS SEMUA SKYLINE DARI 'customer_skyline' YANG BUKAN RSL DARI Q, SEHINGGA HANYA TERSISA RSL Q
	### - PASTIKAN NILAI YANG DIPROSES ADALAH HASIL TRANSFORMASI DARI ASLINYA TERHADAP DATA POINT KONSUMEN
	global data_length
	print("")
	print("")
	print("")
	print("")
	print("")
	print("")
	print("CALCULATE RSL Q")
	print("Q : " + str(query_point))
	print("CUSTOMER SKYLINE per user : ")
	for i in customer_skyline:
		print(customer_skyline[i])
	print("-------------------------------------------x")
	for dict_index in customer_skyline:
		transformed_query_point = []
		for q in range(0, data_length):
			transformed_value = abs(float(query_point[q+1]) - customer_skyline[dict_index][-2][q])
			transformed_query_point.append(transformed_value)
		print("q menjadi : " + str(transformed_query_point))
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
		#deleting dominated data on customer skyline
		if(customer_skyline[dict_index][-1] == 'ok'):
			for i in range(len(customer_skyline[dict_index]) - 3, -1, -1):
				if(customer_skyline[dict_index][i][-1] == 'delete'):
					customer_skyline[dict_index].remove(customer_skyline[dict_index][i])
	return customer_skyline




def generate_safe_region_q():
	### - SEMUA CUSTOMER SKYLINE HANYA YANG JADI RSL DARI Q, (PANGGIL FUNGSI GET RSL Q TERLEBIH DAHULU)
	#This function calculate all safe region areas from every DDR Prime of customer data
	global customer_skyline
	global query_point
	global safe_region
	global data_length
	global jumlah_rsl

	query_point = query_point.split()
	print("CURRENT CUSTOMER SKYLINE : ")
	for i in customer_skyline:
		print(customer_skyline[i])
	calculate_rsl_q(customer_skyline, query_point)
	print("AFTER CALCULATING RSL Q, CUSTOMER SKYLINE : ")
	for i in customer_skyline:
		print(customer_skyline[i])

	safe_region = []
	#SAFE REGION ADALAH JARAK DARI TIAP USER PREFERENCE KE DDR PRIME NYA MASING_MASING 
	for dict_index in customer_skyline:		#c is dictionary index
		print("")
		print("")
		print("CUSTOMER SKYLINE KE : " + str(dict_index))
		if(customer_skyline[dict_index][-1] == 'ok'):
			jumlah_rsl += 1
			list_rsl.append(dict_index)
			print("Data CS : " + str(customer_skyline[dict_index]))
			ddr_prime = []
			for data_index in range(0, len(customer_skyline[dict_index])-2):
				data = []
				for i in range(0, data_length):
					if(customer_skyline[dict_index][data_index][i+1] != 'null'):
						# print("A " + str(query_point[i+1]))
						# print("B " + str(customer_skyline[dict_index][-2][i]))
						#difference = abs(float(query_point[i+1]) - customer_skyline[dict_index][-2][i])
						top = customer_skyline[dict_index][-2][i] + customer_skyline[dict_index][data_index][i+1]
						bottom = customer_skyline[dict_index][-2][i] - customer_skyline[dict_index][data_index][i+1]
						#difference = abs(customer_skyline[dict_index][-2][i] - customer_skyline[dict_index][data_index][i+1])
						# print("A " + str(customer_skyline[dict_index][-2][i]) + " + B " + str(customer_skyline[dict_index][data_index][i+1]))
						# top = customer_skyline[dict_index][-2][i] + customer_skyline[dict_index][data_index][i+1]
						# bottom = customer_skyline[dict_index][-2][i] - customer_skyline[dict_index][data_index][i+1]
					else:
						top = 'null'
						bottom = 'null'
					max_min_value = [top, bottom]
					data.append(max_min_value)
				ddr_prime.append(data)
			#q juga harus dibandingkan karena q juga adalah bagian RSL dari customer skyline ini
			data = []
			for i in range(0, data_length):
				diff = abs(float(query_point[i+1]) - customer_skyline[dict_index][-2][i])
				top = customer_skyline[dict_index][-2][i] + diff
				bottom = customer_skyline[dict_index][-2][i] - diff
				max_min_value = [top, bottom]
				data.append(max_min_value)
			ddr_prime.append(data)
			print("this ddr_prime : " + str(ddr_prime))
			print("q              : " + str(query_point))
			#filtering, mendapatkan semua safe region yang mengandung q di dalamnya
			used_ddr_prime = []
			for data_index in range(0, len(ddr_prime)):
				q_dimension_counter = 0
				for i in range(0, data_length):
					# print("TOP    : " + str(ddr_prime[data_index][i][0]))
					# print("BOTTOM : " + str())
					if(ddr_prime[data_index][i][0] >= float(query_point[i+1]) and ddr_prime[data_index][i][1] <= float(query_point[i+1])):
						q_dimension_counter += 1

				if(q_dimension_counter == data_length):
					used_ddr_prime.append(ddr_prime[data_index])
			ddr_prime = list(used_ddr_prime)

			print("DDR_PRIME x : " + str(ddr_prime))

			##NEED ADJUSTMENT AT THE END AND BEGINNING OF THE DATA ON DDR PRIME
			if(len(safe_region) == 0):
				print("SAFE REGION BARU/////////")
				safe_region = list(ddr_prime)
				print("SR    : " + str(safe_region))
			else:
				#checking intersection
				print("SAFE REGION UPDATE///////")
				new_safe_region = []
				for safe_index in range(0, len(safe_region)):
					for ddr_index in range(0, len(ddr_prime)):
						intersect_status = True
						intersect_data = []
						#perulangan sebanyak dimensi
						for i in range(0, data_length):
							#top
							if(ddr_prime[ddr_index][i][0] == 'null' and safe_region[safe_index][i][0] == 'null'):
								top = 'null'
							elif(ddr_prime[ddr_index][i][0] == 'null'):
								top = safe_region[safe_index][i][0]
							elif(safe_region[safe_index][i][0] == 'null'):
								top = ddr_prime[ddr_index][i][0]
							else:
								top = min(ddr_prime[ddr_index][i][0], safe_region[safe_index][i][0])

							#bottom
							if(ddr_prime[ddr_index][i][1] == 'null' and safe_region[safe_index][i][1] == 'null'):
								bottom = 'null'
							elif(ddr_prime[ddr_index][i][1] == 'null'):
								bottom = safe_region[safe_index][i][1]
							elif(safe_region[safe_index][i][1] == 'null'):
								bottom = ddr_prime[ddr_index][i][1]
							else:
								bottom = max(ddr_prime[ddr_index][i][1], safe_region[safe_index][i][1])
							# print("top    : " + str(top))
							# print("bottom : " + str(bottom))
							if(top != 'null' and bottom != 'null'):
								if(bottom > top):
									intersect_status = False
							#print("Inst s : " + str(intersect_status))
							max_min_value = [top, bottom]
							intersect_data.append(max_min_value)
						if(intersect_status == True):
							new_safe_region.append(intersect_data)
				print("I/ safe_region : " + str(safe_region))
				print("I/ new_safe_re : " + str(new_safe_region))
				if(len(new_safe_region) > 0):
					safe_region = list(new_safe_region)
				print("HASIL SAFE REGION " + str(safe_region))
	print("HASIL FINAL SAFE REGION : " + str(safe_region))
	return safe_region




def generate_ddr_prime_ct(ct):
	#This function will check if query_point is included to ct's skyline
	#It will return Ct DDR Prime and status of query point
	global product_list
	global node
	global local_skyline
	global candidate_skyline
	global global_skyline
	global shadow_skyline
	global virtual_point
	global bitmap
	global query_point
	global t
	global data_length
	#global safe_region 		#

	fp = open(product_list)
	#Harusnya disini menggunakan variabel global_skyline yang berbeda. (Karena nilai global disimpan dalam variabel lain, sepertinya boleh untuk dihapus)
	#Variabel local_skyline, candidate_skyline, shadow_skyline, dan virtual point harus diinisialisasi ulang
	local_skyline.clear()
	candidate_skyline.clear()
	global_skyline.clear()
	shadow_skyline.clear()
	virtual_point.clear()
	node.clear()
	for line in fp:
		bitmap = ""
		transformed_data = Prepare_Data(line, ct)
		is_skyline = insert_local_skyline(transformed_data, bitmap)
		if(is_skyline == True):
			insert_candidate_skyline(transformed_data, bitmap)
			if(len(candidate_skyline) > t):
				update_global_skyline()
				candidate_skyline.clear()
	update_global_skyline()
	candidate_skyline.clear()
	fp.close()

	#check if the QUERY POINT is part of DSL(ct)
	generate_query_point()	#The query point exist from here
	bitmap = ""
	transformed_query_point = Prepare_Data(query_point, ct)
	q_is_local_skyline = insert_local_skyline(transformed_query_point, bitmap)
	if(q_is_local_skyline == True):
		insert_candidate_skyline(transformed_query_point, bitmap)
		update_global_skyline()
		candidate_skyline.clear()
	q_is_dsl = False
	for i in range(0, len(global_skyline)):
		if(global_skyline[i][0] == "QP"):
			q_is_dsl = True
			break
	if(q_is_dsl == True):
		#HENTIKAN PROGRAM
		print("Tidak perlu dilakukan penyesuaian")
		change_status = 0
		exit()
	else:
		#create ddr prime of ct
		#print("ADA " + str(len(global_skyline)) + " DATA DI GLOBAL")
		#sorted_data = list(sorted(global_skyline, key=lambda newlist: newlist[1]))

		ddr_prime_ct = []
		print("CT GLOBAL SKYLINE : " + str(global_skyline))
		print("CT                : " + str(ct))
		for data_index in range(0, len(global_skyline)):
			#print("GLOBAL : " + str(global_skyline[data_index]))
			data = []
			for i in range(0, data_length):
				if(global_skyline[data_index][i+1] != 'null'):
					#difference = abs(global_skyline[data_index][i+1] - ct[i])
					top = ct[i] + global_skyline[data_index][i+1]
					bottom = ct[i] - global_skyline[data_index][i+1]
				else:
					top = 'null'
					bottom = 'null'
				max_min_value = [top, bottom]
				data.append(max_min_value)
			ddr_prime_ct.append(data)
	print("DDR PRIME CT : " + str(ddr_prime_ct))
	return ddr_prime_ct


# for data_index in range(0, len(sorted_data)-1):
# 	data = []
# 	for i in range(0, len(ct)):
# 		if(sorted_data[data_index][i+1] == 'null' and sorted_data[data_index+1][i+1] == 'null'):
# 			top = 'null'
# 			bottom = 'null'
# 		elif(sorted_data[data_index][i+1] == 'null'):
# 			top = ct[i] + sorted_data[data_index+1][i+1]
# 			bottom = ct[i] - sorted_data[data_index+1][i+1]
# 		elif(sorted_data[data_index+1][i+1] == 'null'):
# 			top = ct[i] + sorted_data[data_index][i+1]
# 			bottom = ct[i] - sorted_data[data_index][i+1]
# 		else:
# 			top = max((ct[i] + sorted_data[data_index][i+1]), (ct[i] + sorted_data[data_index+1][i+1]))
# 			bottom = min((ct[i] - sorted_data[data_index][i+1]), (ct[i] - sorted_data[data_index+1][i+1]))
# 		max_min_value = [top, bottom]
# 		data.append(max_min_value)
# 	ddr_prime_ct.append(data)





def check_intersection(safe_region, ddr_prime_ct):
	global intersection
	global data_length
	print("")
	print("")
	print("")
	print("")
	print("")
	print("")
	print("")
	print("RUNNING CHECK INTERSECTION")
	print("++++++++++++++++++++++++++")
	print("")
	print("SAFE REGION : " + str(safe_region))
	print("")
	print("DDR PRIME CT : " + str(ddr_prime_ct))
	print("")

	intersection = []
	for safe_index in range(0, len(safe_region)):
		for ddr_index in range(0, len(ddr_prime_ct)):
			intersect_data = []
			intersect_status = True
			for i in range(0, data_length):
				#top
				if(safe_region[safe_index][i][0] == 'null' and ddr_prime_ct[ddr_index][i][0] == 'null'):
					top = 'null'
				elif(safe_region[safe_index][i][0] == 'null'):
					top = ddr_prime_ct[ddr_index][i][0]
				elif(ddr_prime_ct[ddr_index][i][0] == 'null'):
					top = safe_region[safe_index][i][0]
				else:
					top = min(safe_region[safe_index][i][0], ddr_prime_ct[ddr_index][i][0])

				#bottom
				if(safe_region[safe_index][i][1] == 'null' and ddr_prime_ct[ddr_index][i][1] == 'null'):
					bottom = 'null'
				elif(safe_region[safe_index][i][1] == 'null'):
					bottom = ddr_prime_ct[ddr_index][i][1]
				elif(ddr_prime_ct[ddr_index][i][1] == 'null'):
					bottom = safe_region[safe_index][i][1]
				else:
					bottom = max(safe_region[safe_index][i][1], ddr_prime_ct[ddr_index][i][1])

				max_min_value = [top, bottom]
				intersect_data.append(max_min_value)

				if(top != 'null' and bottom != 'null'):
					if(bottom > top):
						intersect_status = False
			#print("Intersect Status : " + str(intersect_status))
			if(intersect_status == True):
				intersection.append(intersect_data)
	if(len(intersection) > 0):
		return True
	else:
		return False

def move_query_point():
	#Output : titik baru untuk query point q
	print("")
	print("")
	print("")
	print("")
	print("RUNNING MOVE QUERY POINT")
	print("")
	global intersection
	global query_point
	global q_cost
	global data_length
	print("Intersection : " + str(intersection))
	modified_value = []
	distance_value = []
	for data_index in range(0, len(intersection)):
		nearest_point = []
		nearest_distance = []
		for i in range(0, data_length):
			top_diff = abs(float(query_point[i+1]) - intersection[data_index][i][0])
			bottom_diff = abs(float(query_point[i+1]) - intersection[data_index][i][1])
			#minimal_distance = min(a,b)
			if(bottom_diff < top_diff):
				nearest_point.append(intersection[data_index][i][1])
				nearest_distance.append(bottom_diff)
			else:
				nearest_point.append(intersection[data_index][i][0])
				nearest_distance.append(top_diff)
		modified_value.append(nearest_point)
		distance_value.append(nearest_distance)
	#done, tinggal return kedua nilai ini untuk di analisa
	#atau, langsung olah disini, cari yang mana yang paling efisien

	#Mencari yang paling efisien:
	cheapest_index = None
	current_cost = 99999999999
	for data_index in range(0, len(modified_value)):
		total_cost = 0
		for i in range(0, data_length):
			total_cost += (distance_value[data_index][i] * q_cost[i])
		if(total_cost < current_cost):
			cheapest_index = data_index
	recommendation = modified_value[cheapest_index]
	#print(recommendation)
	print("Move query point to : " + str(recommendation))



def move_why_not_point(ct, q):		#q here is transformed q
	global data_length
	global ct_cost
	global node
	global local_skyline
	global candidate_skyline
	global global_skyline
	global shadow_skyline
	global virtual_point
	print("")
	print("RUNNING MOVE WHY NOT POINT")
	print("CT : " + str(ct))
	print("Q  : " + str(q))
	"""
	A = window_query(ct, q)
	F <- A
	for each e1 element F do:
		if e2 element F such e2 dominate e1 then:
			remove e1 from F
	M = initiate
	for each e1 element F do
		ul computation //new location
		add ul to M
	sort m based on dimension i
	for ul, ul+1 element M do:
		ul,l+1 = min (ul, ul+1) for all dimensions
		if ul is the first entry in M :
			replace ul+1 in M by ul,l+1
		else if ul+1 is the last entry in M :
			replace ul in M by ul,l+1
		else :
			replace ul and ul+1 in M by ul,l+1
		u1i <- cti //u1 is the first entry in M
		u|M|j <- ctj // u|M| is the last entry in M

	"""

	"""
	A = window_query(ct, q)
	"""
	#Mencari titik yang berada diantara dua buah titik, note : q sudah ditransformasikan
	# A = []
	# fp = open(product_list)

	# for line in fp:
	# 	product = line.split()
	# 	status_checker = 0
	# 	transformed_point = []
	# 	dimension_in_window = 0
	# 	for i in range(0, data_length):
	# 		if(product[i+1] != 'null'):
	# 			transformed_value = ct[i] + abs(ct[i] - float(product[i+1]))
	# 			transformed_point.append(transformed_value)
	# 			if(transformed_value <= q[i]):
	# 				dimension_in_window += 1
	# 		else:
	# 			transformed_point.append('null')
	# 			dimension_in_window += 1
	# 	if(dimension_in_window == data_length):
	# 		A.append(transformed_point)
	# print("A  : " + str(A))

	A = []
	fp = open(product_list)
	for line in fp:
		product = line.split()
		transformed_point = []
		for i in range(0, data_length):
			if(product[i+1] != 'null'):
				#memindahkan semua data ke kanan ct, agar bisa dijadikan sebagai acuan
				transformed_value = ct[i] + abs(ct[i] - float(product[i+1]))
				transformed_point.append(transformed_value)
			else:
				#ct dipindahkan karena ada suatu nilai yang membatasinya untuk mencapai q, jika tidak ada, ct tidak perlu dipindahkan
				transformed_point.append(ct[i])
		A.append(transformed_point)

	print("A awal : " + str(A))

	#PASTIKAN DATA DISINI SEMUA DIMENSINYA LENGKAP

	#hilangkan semua data yang berada diatas q, data yang berada diatas q sudah pasti letaknya bawah/kiri ct
	for data_index in range(0, len(A)):
		status = True
		for i in range(0, data_length):
			if(A[data_index][i] > q[i]):
				status = False
		if(status == False):
			A[data_index][-1] = 'delete'
	for i in reversed(A):
		if(i[-1] == 'delete'):
			A.remove(i)
	print("A filt : " + str(A))

	#Tidak perlu menggunakan metode i-skyline karena data di sini semua dimensinya lengkap
	for data_index in range(0, len(A)):		#transformasikan terhadap q
		for i in range(0, data_length):
			#cari jarak, bukan titik
			A[data_index][i] = abs(q[i] - A[data_index][i])
		A[data_index].append('ok')
	for data_index in range(0, len(A)):
		for data_index_2 in range(0, len(A)):
			greater = False
			smaller = False
			for i in range(0, data_length):
				if(A[data_index][i] < A[data_index_2][i]):
					smaller = True
				elif(A[data_index][i] > A[data_index_2][i]):
					greater = True
			if(smaller == True and greater == False):
				A[data_index_2][-1] = 'delete'
			elif(smaller == False and greater == True):
				A[data_index][-1] = 'delete'
	print("A mark : " + str(A))
	for i in reversed(A):
		if(i[-1] == 'delete'):
			A.remove(i)
	print("A delt : " + str(A))

	#######MENDAPATKAN TITIK BARU UNTUK ct 		//A masih dalam bentuk jarak dari q
	####Output : Titik
	M = []
	for data_index in range(0, len(A)):
		data = []
		for i in range(0, data_length):
			temp = q[i] - (A[data_index][i] / 2)
			data.append(temp)
		M.append(data)

	print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHh")
	print("M : " + str(M))

	#Cari cost terendah :
	current_cost = 99999999999
	cheapest_index = None
	for data_index in range(0, len(M)):
		total_cost = 0
		for i in range(0, data_length):
			if(M[data_index][i] != 'null'):
				total_cost += (abs(M[data_index][i] - ct[i]) * ct_cost[i])
		if(total_cost < current_cost):
			cheapest_index = data_index
	for i in range(0, data_length):
		if(M[cheapest_index][i] == 'null'):
			M[cheapest_index][i] = ct[i]
	print("Move q  TO : " + str(q))
	print("MOVE ct TO : " + str(M[cheapest_index])) 


	"""
	F <- A
	for each e1 element F do:
		if e2 element F such e2 dominate e1 then:
			remove e1 from F
	"""
	# F = list(A)
	# print("Fi : " + str(F))
	# for data_index in range(0, len(F)):
	# 	greater = False
	# 	smaller = False
	# 	for data_index_2 in range(0, len(F)):
	# 		for i in range(0, data_length):
	# 			if(F[data_index][i] != 'null' and F[data_index_2][i] != 'null'):
	# 				if(F[data_index][i] > F[data_index_2][i]):
	# 					greater = True
	# 				elif(F[data_index][i] < F[data_index_2][i]):
	# 					smaller = True
	# 	if(greater == True and smaller == False):
	# 		F[data_index_2][-1] = 'delete'
	# print("Fd : " + str(F))
	# for i in reversed(F):
	# 	if(i[-1] == 'delete'):
	# 		F.remove(i)
	# print("Fn : " + str(F))
	
	"""
	M = initiate
	for each e1 element F do
		ul computation //new location
		add ul to M
	"""
	# M = []
	# for data_index in range(0, len(F)):
	# 	new_point = []
	# 	for i in range(0, len(F[data_index])-2):
	# 		print("fx : " +str(F[data_index][i+1]))
	# 		if(F[data_index][i+1] != 'null'):
	# 			u = F[data_index][i+1] + (abs(F[data_index][i+1] - q[i]) / 2)
	# 		else:
	# 			u = 'null'
	# 		new_point.append(u)
	# 	M.append(new_point)
	# print("M  : " + str(M))
	# M = []
	# for data_index in range(0, len(F)):
	# 	new_point = []
	# 	print("F[data_index] : " + str(F[data_index]))
	# 	for i in range(0, data_length):
	# 		if(F[data_index][i] != 'null'):
	# 			u = F[data_index][i] + (abs(F[data_index][i] - q[i]) / 2)
	# 		else:
	# 			u = 'null'
	# 		new_point.append(u)
	# 	M.append(new_point)
	# print("M  : " + str(M))

	# #Cari cost terendah :
	# current_cost = 99999999999
	# cheapest_index = None
	# for data_index in range(0, len(M)):
	# 	total_cost = 0
	# 	for i in range(0, data_length):
	# 		if(M[data_index][i] != 'null'):
	# 			total_cost += (abs(M[data_index][i] - ct[i]) * ct_cost[i])
	# 	if(total_cost < current_cost):
	# 		cheapest_index = data_index
	# for i in range(0, data_length):
	# 	if(M[cheapest_index][i] == 'null'):
	# 		M[cheapest_index][i] = ct[i]
	# print("Move q  TO : " + str(q))
	# print("MOVE ct TO : " + str(M[cheapest_index])) 


	"""
	sort m based on dimension i 		//CANNOT SORT NULL DATA
	"""
	# sorted_data = list(sorted(M, key=lambda newlist: newlist[1]))
	# print("St : " + str(sorted_data))

	"""
	for ul, ul+1 element M do:
		ul,l+1 = min (ul, ul+1) for all dimensions
		if ul is the first entry in M :
			replace ul+1 in M by ul,l+1
		else if ul+1 is the last entry in M :
			replace ul in M by ul,l+1
		else :
			replace ul and ul+1 in M by ul,l+1
		u1i <- cti //u1 is the first entry in M
		u|M|j <- ctj // u|M| is the last entry in M
	"""
	# ull = []
	# for data_index in range(0, len(M)):
	# 	data = []
	# 	for i in range(0, data_length):
	# 		minimal = min(M[data_index][i], M[data_index+1][i])
	# 		data.append(minimal)
	# 	ull.append(data)
	# print("ULL : " + str(ull))



	# fp = open(product_list)
	# for line in fp:
	# 	product = line.split()
	# 	greater = False		#harus dibawah safe edge
	# 	smaller = False
	# 	transformed_data = []
	# 	for i in range(0, len(product) - 1):
	# 		if(product[i+1] != 'null'):
	# 			transformed_value = float(ct[i]) + abs(float(ct[i]) - float(product[i+1]))
	# 			transformed_data.append(transformed_value)
	# 			if(safe_edge[data_index][i] > transformed_value):
	# 				greater = True
	# 			elif(safe_edge[data_index][i] < transformed_value):
	# 				smaller = True
	# 		else:
	# 			transformed_value = 'null'
	# 			transformed_data.append(transformed_value)
	# 	transformed_data.append(data_index)
	# 	if(greater == True and smaller == False):
	# 		print("appended")
	# 		transformed_space.append(transformed_data)
	# fp.close()



def Move_Why_Not_And_Query_Point():
	global safe_region
	global query_point
	global ct
	global product_list
	global ct_cost
	global q_cost

	print("RUNNING MOVE WHY NOT AND QUERY POINT")

	#Find edge of SR(q)
	#Transform all point, ct is center
	#Remove all data point that dominated by each edge of SR(q)
	#Find frontier
	#Find cheapest modification

	###Paper : 
	"""
	E = initiate
	for each rec1 element SR do :
		E = E union corner_points(rec1)
	Q = transformed_space(E, ct)	/ct is origin
	for each e1,e2 element Q such that e1 dominate e2:
		remove e2
	Mc = initiate
	for each e1 element Q do:
		T -> move_why_not and query point /Alg 1
		Mc = Mc U T
	//compute score s1 of entries e1 element Mc
	"""
	
	print("")
	print("")
	print("")
	print("NEW")
	
	"""
	E = initiate
	for each rec1 element SR do :
		E = E union corner_points(rec1)
	"""
	E = []
	print("SR : " + str(safe_region))
	for safe_index in range(0, len(safe_region)):
		print("sr : " + str(safe_region[safe_index]))
		corner_points = []
		for i in range(0, len(safe_region[safe_index])):
			top_diff = abs(safe_region[safe_index][i][0] - float(ct[i]))
			bottom_diff = abs(safe_region[safe_index][i][1] - float(ct[i]))
			#mencari jarak terdekat ke ct sebagai corner value
			if(top_diff <= bottom_diff):
				corner_points.append(safe_region[safe_index][i][0])
			elif(top_diff > bottom_diff):
				corner_points.append(safe_region[safe_index][i][1])
		#E = E union corner point
		E.append(corner_points)
	print(ct)
	print("E  : " + str(E))
		

	"""
	Q = transformed_space(E, ct)	/ct is origin
	"""
	Q = []
	for data_index in range(0, len(E)):
		data = []
		for i in range(0, len(E[data_index])):
			transformed_value = float(ct[i]) + abs(float(ct[i]) - E[data_index][i])
			data.append(transformed_value)
		data.append('ok')
		Q.append(data)
	print("Q  : " + str(Q))

	"""
	for each e1,e2 element Q such that e1 dominate e2:
		remove e2
	"""
	for data_index in range(0, len(E)):
		greater = False
		smaller = False
		for data_index_2 in range(0, len(E)):
			for i in range(0, len(E[data_index])):
				if(Q[data_index][i] > Q[data_index_2][i]):
					greater = True
				elif(Q[data_index][i] < Q[data_index_2][i]):
					smaller = True
			if(greater == True and smaller == False):
				Q[data_index_2][-1] = 'delete'
	print("Qm : " + str(Q))
	for i in reversed(Q):
		if(i[-1] == 'delete'):
			Q.remove(i)
	print("Q- : " + str(Q))


	"""
	Mc = initiate
	for each e1 element Q do:
		T -> move_why_not and query point /Alg 1
		Mc = Mc U T
	"""
	Mc = []
	for data_index in range(0, len(Q)):
		T = move_why_not_point(ct, Q[data_index][:-1])




	# #Find edge of SR(q)
	# safe_edge = []
	# for data_index in range(0, len(safe_region)):
	# 	nearest = []
	# 	cost = 0
	# 	for i in range(0, len(safe_region[data_index])):
	# 		top_diff = abs(safe_region[data_index][i][0] - float(ct[i]))
	# 		bottom_diff = abs(safe_region[data_index][i][1] - float(ct[i]))
	# 		if(top_diff < bottom_diff):
	# 			nearest.append(safe_region[data_index][i][0])
	# 			cost += (top_diff * q_cost[i])
	# 		elif(top_diff > bottom_diff):
	# 			nearest.append(safe_region[data_index][i][1])
	# 			cost += (bottom_diff * q_cost[i])
	# 		else:	#jika jarak top dan bottom saama, pilih yang top karena data ditransformasikan ke atas
	# 			nearest.append(safe_region[data_index][i][0])
	# 	nearest.append(cost)
	# 	safe_edge.append(nearest)



	# print("SAFE EDGE         : " + str(safe_edge))
	# #Transform all point, ct is center, SEKALIAN : #Remove all data point that dominated by each edge of SR(q)
	# #Cari pasangan tansformasi dan safe_edge dimana hasil transformasi tidak mendominasi safe_edge (dominasi lebih besar yg mendominasi)
	# transformed_space = []
	# for data_index in range(0, len(safe_edge)):
	# 	print("masuk")
	# 	fp = open(product_list)
	# 	for line in fp:
	# 		product = line.split()
	# 		greater = False		#harus dibawah safe edge
	# 		smaller = False
	# 		transformed_data = []
	# 		for i in range(0, len(product) - 1):
	# 			if(product[i+1] != 'null'):
	# 				transformed_value = float(ct[i]) + abs(float(ct[i]) - float(product[i+1]))
	# 				transformed_data.append(transformed_value)
	# 				if(safe_edge[data_index][i] > transformed_value):
	# 					greater = True
	# 				elif(safe_edge[data_index][i] < transformed_value):
	# 					smaller = True
	# 			else:
	# 				transformed_value = 'null'
	# 				transformed_data.append(transformed_value)
	# 		transformed_data.append(data_index)
	# 		if(greater == True and smaller == False):
	# 			print("appended")
	# 			transformed_space.append(transformed_data)
	# 	fp.close()

	# print("TRANSFORMED SPACE : " + str(transformed_space))

	# #Find frontier
	# #BANDINGKAN SEMUA DATA HASIL SEBELUMNYA
	# frontier = list(transformed_space)
	# print("frontier init : " + str(frontier))
	# for data_index in range(0, len(frontier)):
	# 	#BRUTEFORCE, data disini lebih sedikit, kecuali datanya sama rata
	# 	for data_index_2 in range(0, len(frontier)):
	# 		greater = False
	# 		smaller = False
	# 		for i in range(0, len(frontier[data_index])-1):
	# 			#bandingkan
	# 			if(frontier[data_index][i] != 'null' and frontier[data_index_2][i] != 'null'):
	# 				if(frontier[data_index][i] > frontier[data_index_2][i]):
	# 					greater = True
	# 				elif(frontier[data_index][i] < frontier[data_index_2][i]):
	# 					smaller = True
	# 		if(greater == True and smaller == False):
	# 			frontier[data_index_2][-1] = 'delete'
	# eliminated = 0
	# for data_index in range(0, len(frontier)):
	# 	if(frontier[data_index][-1] == 'delete'):
	# 		eliminated += 1
	# #jika tidak ada skyline
	# if(eliminated == len(frontier)):
	# 	frontier = list(transformed_space)
	# print("frontier : " + str(frontier))

	# #dapatkan titik yang lebih dekat ke edge of safe point, setengah dari jarak (edge of safe point[i] - frontier[i])
	# cheapest_index = None
	# current_cost = 9999999999
	# for data_index in range(0, len(frontier)):
	# 	print('masuk frontier')
	# 	if(frontier[data_index][-1] != 'delete'):
	# 		total_cost = safe_edge[frontier[data_index][-1]][-1]
	# 		safe_index = frontier[data_index][-1]
	# 		for i in range(0, len(frontier[data_index])-1):
	# 			if(frontier[data_index][i] != 'null'):
	# 				origin_point = frontier[data_index][i]
	# 				frontier[data_index][i] += ((safe_edge[safe_index][i] - frontier[data_index][i]) * 0.5)
	# 				difference = abs(origin_point - frontier[data_index][i])
	# 				total_cost += difference * q_cost[i]
	# 		if(total_cost < current_cost):
	# 			cheapest_index = data_index
	# 			current_cost = total_cost
	# recommendation = list(frontier[cheapest_index][:-1])
	# print("///PERUBAHAN///")
	# print("frontier : " + str(frontier))
	# print("Q  : " + str(safe_edge[frontier[cheapest_index][-1]]))
	# print("CT : " + str(recommendation))



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
		node[bitmap].append(data)
		local_skyline[bitmap] = []
		shadow_skyline[bitmap] = []
		virtual_point[bitmap] = []
		n_updated_flag[bitmap] = False
	else:
		node[bitmap].append(data)
	return transformed_data


#PREPROCESSING
#THIS INITIAL PROGRAM WILL CALLED function Generate_All_Dynamic_Skyline

generate_ct()
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

	#Menyimpan semua skyline untuk tiap user
	#sisipkan nilai asli customer preference di akhir list untuk digunakan pada fungsi pembandingan q
	# print("test : " + str(list_customer[x]))
	# temp = list(global_skyline)
	if(len(global_skyline) > 0):
		customer_skyline[str(customer_index)] = list(global_skyline)
		customer_skyline[str(customer_index)].append(list(list_customer[x]))
		customer_skyline[str(customer_index)].append("ok")
		customer_index += 1
fu.close()

print("")
print("")
print("")
print("")
print("CUSTOMER SKYLINE CUSTOMER SKYLINE CUSTOMER SKYLINE CUSTOMER SKYLINE CUSTOMER SKYLINE CUSTOMER SKYLINE CUSTOMER SKYLINE CUSTOMER SKYLINE : ")
print("per user : ")
for i in customer_skyline:
	print(customer_skyline[i])
print("")
ddr_prime_ct = generate_ddr_prime_ct(ct)

safe_region = generate_safe_region_q()

generate_cost()

intersection_status = check_intersection(safe_region, ddr_prime_ct)
if(intersection_status == True):
	print("OPTION 1")
	print("Need to move query point : ")
	move_query_point()
else:
	print("OPTION 2")
	print("Need to move why-not and query point : ")
	recommendation =  Move_Why_Not_And_Query_Point()
#print(recommendation)
print("Jumlah RSL : " + str(jumlah_rsl))
print("List RSL   : " + str(list_rsl))