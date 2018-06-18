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
product_list = "random_specs.txt"
intersection = []
ct_cost = []
q_cost = []

def Insert_Local_Skyline(current_specs, current_bit):
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
				shadow_skyline[current_bit].remove(i)
		content = list(current_specs)
		content.append('ok');
		shadow_skyline[current_bit].append(content)
	return False


def Insert_Candidate_Skyline(current_specs, current_bit):
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



def Insert_Virtual_Point(current_specs, current_bit):
	global local_skyline
	global virtual_point
	global shadow_skyline
	#MEMBANDINGKAN DENGAN LOCAL SKYLINE
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
			shadow_skyline[current_bit].append(i)
			local_skyline[current_bit].remove(i)
			shadow_skyline[current_bit][-1][-1] = 'ok'
	
	#MEMBANDINGKAN DENGAN VIRTUAL POINT
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
			virtual_point[current_bit].remove(i)
	content = list(current_specs)
	content.append('ok')
	virtual_point[current_bit].append(content)


def Update_Global_Skyline():
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
			global_skyline.remove(i)
	for i in reversed(candidate_skyline):
		if(i[-1] == 'delete'):
			candidate_skyline.remove(i)
	for i in candidate_skyline:
		global_skyline.append(i)

	for i in n_updated_flag:
		n_updated_flag[i] == False


# def Generate_Query_Point(): #OLD
# 	global query_point
# 	query_point.append(6)
# 	query_point.append(2)
# 	query_point.append(1)
# 	query_point.append(3)

def Generate_Query_Point(): #NEW
	global query_point
	#query_point = "QP 6 2 1 3"		#SR(q) DAN DDR(ct) berpotongan
	#query_point = "QP 7 5 7 8"		#SR(q) DAN DDR(ct) tidak berpotongan -> KARENA TIDAK ADA SR
	query_point = "QP 15 15 15 15"

def Generate_Ct():
	global ct
	ct.append(2)
	ct.append(2)
	ct.append(2)
	ct.append(2)
	# ct.append(2)
	# ct.append(2)
	# ct.append(2)
	# ct.append(2)

def Generate_Cost():
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

def Calculate_RSL_Q(customer_skyline, query_point):
	### - MENGHAPUS SEMUA SKYLINE DARI 'customer_skyline' YANG BUKAN RSL DARI Q, SEHINGGA HANYA TERSISA RSL Q
	### - PASTIKAN NILAI YANG DIPROSES ADALAH HASIL TRANSFORMASI DARI ASLINYA TERHADAP DATA POINT KONSUMEN

	for dict_index in customer_skyline:
		transformed_query = []
		for q in range(0, len(customer_skyline[dict_index][-2])):
			transformed_value = abs(float(query_point[q+1]) - customer_skyline[dict_index][-2][q])
			transformed_query.append(transformed_value)
		for data_index in range(0, len(customer_skyline[dict_index]) - 2):
			dominating_q = False
			dominating_customer = False
			for i in range(1, len(customer_skyline[dict_index][-2])):
				if(customer_skyline[dict_index][data_index][i] != 'null'):
					if(customer_skyline[dict_index][data_index][i] < transformed_query[i]):
						dominating_q = True
					elif(customer_skyline[dict_index][data_index][i] > transformed_query[i]):
						dominating_customer = True
			if(dominating_q == True and dominating_customer == False):
				customer_skyline[dict_index][-1] = 'delete'
			elif(dominating_q == False and dominating_customer == True):
				customer_skyline[dict_index][data_index][-1] = 'delete'
		if(customer_skyline[dict_index][-1] == 'ok'):
			for i in range(len(customer_skyline[dict_index]) - 3, -1, -1):
				if(customer_skyline[dict_index][i][-1] == 'delete'):
					customer_skyline[dict_index].remove(customer_skyline[dict_index][i])
	return customer_skyline




def Generate_Safe_Region_Q():
	### - SEMUA CUSTOMER SKYLINE HANYA YANG JADI RSL DARI Q, (PANGGIL FUNGSI GET RSL Q TERLEBIH DAHULU)
	#This function calculate all safe region areas from every DDR Prime of customer data
	global customer_skyline
	global query_point
	global safe_region

	query_point = query_point.split()
	Calculate_RSL_Q(customer_skyline, query_point)

	safe_region = []
	###PERULANGAN UNTUK SETIAP SKYLINE DARI PENGGUNA
	for dict_index in customer_skyline:		#c is dictionary index
		if(customer_skyline[dict_index][-1] == 'ok'):
			print("ADA RSL        ADA RSL        ADA RSL        ADA RSL        ADA RSL        ADA RSL")
			#AAAA -> AT THIS PART, THE CUSTOMER SKYLINE SHOULD BE SORTED BY I'TH DIMENSIONS.
			#SORTING : 

			temp = list(customer_skyline[dict_index][:-2])
			sorted_data = list(sorted(temp, key=lambda newlist: newlist[1]))

			ddr_prime = []

			for data_index in range(0, len(sorted_data)-1):
				data = []
				for i in range(0, len(customer_skyline[dict_index][-2])):
					if(sorted_data[data_index][i+1] == 'null' and sorted_data[data_index+1][i+1] == 'null'):
						top = 'null'
						bottom = 'null'
					elif(sorted_data[data_index][i+1] == 'null'):
						top = customer_skyline[dict_index][-2][i] + sorted_data[data_index+1][i+1]
						bottom = customer_skyline[dict_index][-2][i] - sorted_data[data_index+1][i+1]
					elif(sorted_data[data_index+1][i+1] == 'null'):
						top = customer_skyline[dict_index][-2][i] + sorted_data[data_index][i+1]
						bottom = customer_skyline[dict_index][-2][i] - sorted_data[data_index][i+1]
					else:
						top = max((customer_skyline[dict_index][-2][i] + sorted_data[data_index][i+1]), (customer_skyline[dict_index][-2][i] + sorted_data[data_index+1][i+1]))
						bottom = min((customer_skyline[dict_index][-2][i] - sorted_data[data_index][i+1]), (customer_skyline[dict_index][-2][i] - sorted_data[data_index+1][i+1]))
					max_min_value = [top, bottom]
					data.append(max_min_value)
				ddr_prime.append(data)

			print("DDR : " + str(ddr_prime))
			##NEED ADJUSTMENT AT THE END AND BEGINNING OF THE DATA ON DDR PRIME

			if(len(safe_region) == 0):
				safe_region = list(ddr_prime)
			else:
				#checking intersection
				new_safe_region = []
				for safe_index in range(0, len(safe_region)):
					for ddr_index in range(0, len(ddr_prime)):
						intersect_status = True
						intersect_data = []
						#perulangan sebanyak dimensi
						for i in range(0, len(customer_skyline[dict_index][-2])):
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

							if(top != 'null' and bottom != 'null'):
								if(bottom > top):
									intersect_status = False
							max_min_value = [top, bottom]
							intersect_data.append(max_min_value)
						if(intersect_status == True):
							new_safe_region.append(intersect_data)
				safe_region = list(new_safe_region)
	print("PRINTED INSIDE SAFE REGION FUNCTION : " + str(safe_region))
	return safe_region




def Generate_DDR_Prime_Ct(ct):
	print("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
	#This function will check if query_point is included to ct's skyline
	#It will return Ct DDR Prime and status of query point
	global product_list
	global node
	global local_skyline
	global candidate_skyline
	global global_skyline
	global shadow_skyline
	global virtual_point
	global current_bit
	global query_point
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
		current_bit = ""
		transformed_data = Prepare_Data(line, ct)
		is_skyline = Insert_Local_Skyline(transformed_data, current_bit)
		if(is_skyline == True):
			Insert_Candidate_Skyline(transformed_data, current_bit)
			if(len(candidate_skyline) > t):
				Update_Global_Skyline()
				candidate_skyline.clear()
	Update_Global_Skyline()
	fp.close()

	#check if the QUERY POINT is part of DSL(ct)
	Generate_Query_Point()	#The query point exist from here
	print("QUERY POINT EXIST : " + str(query_point))
	current_bit = ""
	transformed_query_point = Prepare_Data(query_point, ct)
	q_is_local_skyline = Insert_Local_Skyline(transformed_query_point, current_bit)
	if(q_is_local_skyline == True):
		print(">>x Query Point inserted as Local")
		Insert_Candidate_Skyline(transformed_query_point, current_bit)
	Update_Global_Skyline()
	candidate_skyline.clear()

	q_is_dsl = False
	for i in range(0, len(global_skyline)):
		if(global_skyline[i][0] == "QP"):
			q_is_dsl = True
	if(q_is_dsl == True):
		#HENTIKAN PROGRAM
		print("Q is already part of DSL(ct), modification is not necessary")
		exit()
	else:
		#create ddr prime of ct
		#ANGGAPLAH INI BENAR
		#HARUS DIREVISI
		#INI MASIH SALAH
		ddr_prime_ct = []
		for g in range(0, len(global_skyline)):
			print(global_skyline[g])
			projected_value = []
			for i in range(1, len(global_skyline[g]) - 2):
				if(global_skyline[g][i] == 'null'):
					bottom = 'null'
					top = 'null'
				else: 
					bottom = ct[i-1] - global_skyline[g][i]
					top = ct[i-1] + global_skyline[g][i]
				max_min_value = [top, bottom]
				projected_value.append(max_min_value)
			ddr_prime_ct.append(projected_value)
		#BATAS AKHIR KESALAHAN
		# for g in range(0, len(global_skyline)):
		# 	print(global_skyline[g])
		

	# print("FINAL")
	# print("GLOBAL F : " + str(global_skyline))

	#print("SAFE : " + str(safe_region))
	return ddr_prime_ct




def Check_Intersection(safe_region, ddr_prime_ct):
	global intersection
	print("")
	print("")
	print("RUNNING CHECKING_INTERSECTION")
	print("SAFE : " + str(safe_region))
	print("DDR  : " + str(ddr_prime_ct))
	intersection = []
	for safe_index in range(0, len(safe_region)):
		for ddr_index in range(0, len(ddr_prime_ct)):
			intersect_data = []
			intersect_status = True
			for i in range(0, len(safe_region[safe_index])):
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

			if(intersect_status == True):
				intersection.append(intersect_data)
	print("INTERSECTION : " + str(intersection))
	if(len(intersection) > 0):
		return True
	else:
		return False

def Move_Query_Point():
	global intersection
	global query_point
	global ct_cost
	print("RUNNING MOVE QUERY POINT")
	print("QUERY POINT  : " +  str(query_point))
	print("intersection : " + str(intersection))
	print("ada " + str(len(intersection)) + " buah data")
	distance_value = []
	modified_value = []
	for data_index in range(0, len(intersection)):
		print(str(data_index) + " " + str(intersection[data_index]))
		nearest_distance = []
		nearest_point = []
		for i in range(0, len(intersection[data_index])):
			a = abs(float(query_point[i+1]) - intersection[data_index][i][0])
			b = abs(float(query_point[i+1]) - intersection[data_index][i][1])
			minimal_distance = min(a,b)
			if(b < a):
				nearest_point.append(intersection[data_index][i][1])
				nearest_distance.append(b)
			else:
				nearest_point.append(intersection[data_index][i][0])
				nearest_distance.append(a)
			# print("NEAREST POINT    : " + str(nearest_point))
			# print("NEAREST DISTANCE : " + str(nearest_distance))
		distance_value.append(nearest_distance)
		modified_value.append(nearest_point)
	#done, tinggal return kedua nilai ini untuk di analisa
	#atau, langsung olah disini, cari yang mana yang paling efisien

	#Mencari yang paling efisien:
	print("HASIL 443: ")
	print("A : " + str(modified_value))
	print("B : " + str(distance_value))
	cheapest_index = None
	current_cost = 99999999999
	for data_index in range(0, len(distance_value)):
		print("HEHE : " + str(distance_value[data_index]))
		total_cost = 0
		for i in range(0, len(distance_value[data_index])):
			total_cost += (distance_value[data_index][i] * ct_cost[i])
		if(total_cost < current_cost):
			cheapest_index = data_index
	print("TERMURAH : " + str(distance_value[cheapest_index]))
	#done, tinggal mengembalikan nilai hasil modifikasi yang paling efisien
	recommendation = modified_value[cheapest_index]
	return recommendation

def Move_Why_Not_And_Query_Point():
	global safe_region
	global query_point
	global ct
	global product_list
	global ct_cost
	global q_cost
	print("RUNNING MOVE WHY-NOT AND QUERY POINT")
	#print("query_point" + str(query_point))
	print("CT : " + str(ct))

	#Find edge of SR(q)
	#Transform all point, ct is center
	#Remove all data point that dominated by each edge of SR(q)
	#Find frontier
	#Find cheapest modification

	#Find edge of SR(q)
	safe_edge = []
	print("jumlah safe region = " + str(len(safe_region)))
	for data_index in range(0, len(safe_region)):
		nearest = []
		cost = 0
		for i in range(0, len(safe_region[data_index])):
			top_diff = abs(safe_region[data_index][i][0] - float(ct[i]))
			bottom_diff = abs(safe_region[data_index][i][1] - float(ct[i]))
			if(top_diff < bottom_diff):
				nearest.append(safe_region[data_index][i][0])
				cost += (top_diff * q_cost[i])
			elif(top_diff > bottom_diff):
				nearest.append(safe_region[data_index][i][1])
				cost += (bottom_diff * q_cost[i])
			else:	#jika jarak top dan bottom saama, pilih yang top karena data ditransformasikan ke atas
				nearest.append(safe_region[data_index][i][0])
		nearest.append(cost)
		safe_edge.append(nearest)

	
	#Transform all point, ct is center, SEKALIAN : #Remove all data point that dominated by each edge of SR(q)
	transformed_space = []
	print("SAFE_EDGE ADA " + str(len(safe_edge)) + " BUAH")
	for data_index in range(0, len(safe_edge)):
		print("START")
		fp = open(product_list)
		for line in fp:
			product = line.split()
			greater = False		#harus dibawah safe edge
			smaller = False
			transformed_data = []
			for i in range(0, len(product) - 1):
				if(product[i+1] != 'null'):
					transformed_value = float(ct[i]) + abs(float(ct[i]) - float(product[i+1]))
					transformed_data.append(transformed_value)
					if(transformed_value > safe_edge[data_index][i]):
						greater = True
					elif(transformed_value < safe_edge[data_index][i]):
						smaller = True
				else:
					transformed_value = 'null'
					transformed_data.append(transformed_value)
			transformed_data.append(safe_edge[data_index][-1])
			if(greater == False and smaller == True):
				transformed_space.append(transformed_data)
		fp.close()
	print("HASIL TS : " + str(transformed_space))

	#Find frontier
	#BANDINGKAN SEMUA DATA HASIL SEBELUMNYA
	for data_index in range(0, len(transformed_space)):
		#BRUTEFORCE, data disini lebih sedikit, kecuali datanya sama rata
		greater = False
		smaller = False
		for data_index_2 in range(0, len(transformed_space)):
			for i in range(0, len(transformed_space[data_index])):
				#bandingkan




	# transformed_space = []
	# fp = open(product_list)
	# node.clear()
	# local_skyline.clear()
	# candidate_skyline.clear()
	# global_skyline.clear()
	# shadow_skyline.clear()
	# virtual_point.clear()
	# for line in fp:
	# 	current_bit = ""
	# 	transformed_data = Prepare_Data(line, list_customer[x])
	# 	is_skyline = Insert_Local_Skyline(transformed_data, current_bit)
	# 	if is_skyline == True:
	# 		Insert_Candidate_Skyline(transformed_data, current_bit)
	# 		if(len(candidate_skyline) > t):
	# 			Update_Global_Skyline()
	# 			candidate_skyline.clear()
	# fp.close()
	#Update_Global_Skyline()

	# fp = open(product_list)
	# number_of_preference += 1
	# for line in fp:
	# 	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
	# 	print(line)

	return True



def Prepare_Data(line, customer):
	global current_bit
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
	data_length = len(current_spec)
	for i in range(1, data_length):
		if(current_spec[i] == "null"):
			current_bit += "0"
			data.append(current_spec[i])
			transformed_data.append(current_spec[i])
		else:
			current_bit += "1"
			difference = abs(float(current_spec[i]) - customer[i-1])
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
	return transformed_data


#product_specs = np.loadtxt('product_specs.txt', skiprows=1, unpack=True)
#user_preference = np.loadtxt('user_preference.txt', skiprows=1, unpack=True)
#current_product = np.loadtxt('current_product.txt', skiprows=1, unpack=True)


#PREPROCESSING
#THIS INITIAL PROGRAM WILL CALLED function Generate_All_Dynamic_Skyline
fu = open("unlabeled_user_preference2.txt")
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
		current_bit = ""
		transformed_data = Prepare_Data(line, list_customer[x])
		is_skyline = Insert_Local_Skyline(transformed_data, current_bit)
		if is_skyline == True:
			Insert_Candidate_Skyline(transformed_data, current_bit)
			if(len(candidate_skyline) > t):
				Update_Global_Skyline()
				candidate_skyline.clear()
	fp.close()
	Update_Global_Skyline()

	#Menyimpan semua skyline untuk tiap user
	#sisipkan nilai asli customer preference di akhir list untuk digunakan pada fungsi pembandingan q
	# print("test : " + str(list_customer[x]))
	# temp = list(global_skyline)
	customer_skyline[str(customer_index)] = list(global_skyline)
	customer_skyline[str(customer_index)].append(list(list_customer[x]))
	customer_skyline[str(customer_index)].append("ok")
	customer_index += 1

#Generate_Query_Point()		#Dihapus jika di fungsi Generate_DDR_Prime_Ct() telah berhasil digenerate
#Generate_Safe_Region_Q()

Generate_Ct()
ddr_prime_ct = Generate_DDR_Prime_Ct(ct)

safe_region = Generate_Safe_Region_Q()

Generate_Cost()

intersection_status = Check_Intersection(safe_region, ddr_prime_ct)
if(intersection_status == True):
	recommendation = Move_Query_Point()
else:
	print("RRRRRRRRRRRRRRRRRR Processing")
	recommendation =  Move_Why_Not_And_Query_Point()

print("INTERSECTION = " + str(intersection_status))

fu.close()