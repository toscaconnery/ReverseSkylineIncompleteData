#!/usr/bin/python

import sys
import time
from time import gmtime, strftime
import numpy as np

a = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
#sys.stdout = open("result_" + str(a) + ".txt", "wt")

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
#product_list = "random_specs.txt"
#product_list = "very_small_dataset2.txt"
product_list = "IND_D4_N1K.txt"
user_preference = "user_preference_D4_N100.txt"
intersection = []
ct_cost = []
q_cost = []
jumlah_rsl = 0
list_rsl = []


#here
def generate_query_point(): #NEW
	global query_point
	query_point = "QP 50 50 50 50"
	#query_point = "QP 45 45 45 45"
	#query_point = "QP 70 70 70 70"


def generate_ct():
	global ct

	ct.append(float(12))
	ct.append(float(15))
	ct.append(float(10))
	ct.append(float(12))
	#
	# ct.append(float(31))
	# ct.append(float(32.5))
	# ct.append(float(47.5))
	# ct.append(float(49.5))

	
	# ct.append(float(46))
	# ct.append(float(57.5))
	# ct.append(float(47))
	# ct.append(float(59.5))

	# ct.append(float(10))
	# ct.append(float(10))
	# ct.append(float(10))
	# ct.append(float(10))

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
	#insert
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



def calculate_rsl_q(customer_skyline, query_point):
	### - MENGHAPUS SEMUA SKYLINE DARI 'customer_skyline' YANG BUKAN RSL DARI Q, SEHINGGA HANYA TERSISA RSL Q
	### - PASTIKAN NILAI YANG DIPROSES ADALAH HASIL TRANSFORMASI DARI ASLINYA TERHADAP DATA POINT KONSUMEN
	global data_length
	print(">> CALCULATING RSL Q")
	# print("QUERY_POINT : " + str(query_point))
	# print("CUSTOMER SKYLINE PER USER : ")
	# print("-------------------------------------------^")
	# for i in customer_skyline:
	# 	print(customer_skyline[i])
	# print("-------------------------------------------v")
	for dict_index in customer_skyline:
		transformed_query_point = []
		for q in range(0, data_length):
			transformed_value = abs(float(query_point[q+1]) - customer_skyline[dict_index][-2][q])
			transformed_query_point.append(transformed_value)
		#print("q menjadi : " + str(transformed_query_point))
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
		if(len(customer_skyline[dict_index]) <= 2):
			customer_skyline[dict_index][-1] = 'delete'
	return customer_skyline




def generate_safe_region_q():
	### - SEMUA CUSTOMER SKYLINE HANYA YANG JADI RSL DARI Q, (PANGGIL FUNGSI GET RSL Q TERLEBIH DAHULU)
	#This function calculate all safe region areas from every DDR Prime of customer data
	global customer_skyline
	global query_point
	global safe_region
	global data_length
	global jumlah_rsl
	global ct


	query_point = query_point.split()
	calculate_rsl_q(customer_skyline, query_point)
	
	print(">> GENERATING SAFE REGION Q")
	
	q = []
	for i in range(0, data_length):
		q.append(float(query_point[i+1]))
	# print("AFTER CALCULATING RSL Q, CUSTOMER SKYLINE : ")
	# for i in customer_skyline:
	# 	print(customer_skyline[i])

	safe_region = []
	#SAFE REGION ADALAH JARAK DARI TIAP USER PREFERENCE KE DDR PRIME NYA MASING_MASING 
	for dict_index in customer_skyline:		#c is dictionary index
		# print("")
		# print("")
		# print("CUSTOMER SKYLINE KE : " + str(dict_index))
		if(customer_skyline[dict_index][-1] == 'ok' and len(customer_skyline)>2):
			jumlah_rsl += 1
			list_rsl.append(dict_index)
			#print("Data CS : " + str(customer_skyline[dict_index]))
			ddr_prime = []
			for data_index in range(0, len(customer_skyline[dict_index])-2):
				data = []
				for i in range(0, data_length):
					if(customer_skyline[dict_index][data_index][i+1] != 'null'):
						top = customer_skyline[dict_index][-2][i] + customer_skyline[dict_index][data_index][i+1]
						bottom = customer_skyline[dict_index][-2][i] - customer_skyline[dict_index][data_index][i+1]
					else:
						top = 'null'
						bottom = 'null'
					max_min_value = [top, bottom]
					data.append(max_min_value)
				ddr_prime.append(data)
			#q juga harus dibandingkan karena q juga adalah bagian RSL dari customer skyline ini
			data = []
			for i in range(0, data_length):
				diff = abs(float(q[i]) - customer_skyline[dict_index][-2][i])
				top = customer_skyline[dict_index][-2][i] + diff
				bottom = customer_skyline[dict_index][-2][i] - diff
				max_min_value = [top, bottom]
				data.append(max_min_value)
			ddr_prime.append(data)
			# print("this ddr_prime : " + str(ddr_prime))
			# print("q              : " + str(q))
			#filtering, mendapatkan semua safe region yang mengandung q di dalamnya
			used_ddr_prime = []
			for data_index in range(0, len(ddr_prime)):
				q_dimension_counter = 0
				#print("DDR PRIME : " + str(ddr_prime[data_index]))
				for i in range(0, data_length):
					# print("TOP    : " + str(ddr_prime[data_index][i][0]))
					# print("BOTTOM : " + str())
					if(ddr_prime[data_index][i][0] != 'null'):
						if(ddr_prime[data_index][i][0] >= float(q[i]) and ddr_prime[data_index][i][1] <= float(q[i])):
							q_dimension_counter += 1
					else:
						q_dimension_counter += 1


				if(q_dimension_counter == data_length):
					used_ddr_prime.append(ddr_prime[data_index])
			ddr_prime = list(used_ddr_prime)

			#print("DDR_PRIME x : " + str(ddr_prime))

			##NEED ADJUSTMENT AT THE END AND BEGINNING OF THE DATA ON DDR PRIME
			if(len(safe_region) == 0):
				#print("SAFE REGION BARU/////////")
				safe_region = list(ddr_prime)
				#print("SR    : " + str(safe_region))
			else:
				#checking intersection
				#print("SAFE REGION UPDATE///////")
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
				# print("I/ safe_region : " + str(safe_region))
				# print("I/ new_safe_re : " + str(new_safe_region))
				if(len(new_safe_region) > 0):
					safe_region = list(new_safe_region)
	# 			print("HASIL SAFE REGION " + str(safe_region))
	print("   SAFE REGION Q : " + str(safe_region))

	if(len(safe_region) == 0):
		print("## Q DOESN'T HAVE SAFE REGION, SPECIAL TREATMENT NEEDED, MOVING CT TO Q")
		# print("Y q : " + str(q))
		generate_cost()
		T = move_why_not_point(ct, q)

		print("")
		print("RESULT : MOVING WHY-NOT POINT")
		print("Q      : " + str(T["q"]))
		print("CT     : " + str(T["ct"]))

		exit()
	return safe_region




def generate_ddr_prime_ct(ct):
	print(">> GENERATING DDR PRIME CT")
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
	global ct_has_skyline
	#global safe_region 		#

	ct_has_skyline = True

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
	# Q cuman ada satu data, lebih baik dibandingkan dengan cara normal
	generate_query_point()	#The query point exist from here
	# print("Query point       : " + str(query_point))
	# print("Global Skyline CT : " + str(global_skyline))
	# print("CT                : " + str(ct))
	#mengubah q
	q = query_point.split()
	for i in range(0, data_length):
		q[i+1] = abs(float(q[i+1]) - ct[i])
	q.append("qp")
	q.append("ok")

	q_is_skyline = True
	for data_index in range(0, len(global_skyline)):
		smaller = False
		greater = False
		for i in range(0, data_length):
			if(q[i+1] < ct[i]):
				smaller = True
			elif(q[i+1] > ct[i]):
				greater = True
		if(smaller == True and greater == False):
			pass#tetap True
		elif(smaller == False and greater == True):
			q_is_skyline = False

	# q_is_dsl = False
	# for i in range(0, len(global_skyline)):
	# 	if(global_skyline[i][0] == "QP"):
	# 		q_is_dsl = True
	# 		break
	if(len(global_skyline) == 0):
		print("## CT DOESN'T HAVE ANY SKYLINE, SPECIAL TREATMENT NEEDED, MOVING CT TO Q")
		elapsed_time = time.time() - start_time
		ct_has_skyline = False
		# exit()
	print("   CT SKYLINE : " + str(global_skyline))
	if(q_is_skyline == True):
		#HENTIKAN PROGRAM
		print("   TIDAK PERLU DILAKUKAN PENYESUAIAN")
		elapsed_time = time.time() - start_time
		print("   TIME USED : " + str(elapsed_time))
		exit()
	else:
		#create ddr prime of ct
		#print("ADA " + str(len(global_skyline)) + " DATA DI GLOBAL")
		#sorted_data = list(sorted(global_skyline, key=lambda newlist: newlist[1]))

		ddr_prime_ct = []
		# print("CT GLOBAL SKYLINE : " + str(global_skyline))
		# print("CT                : " + str(ct))
		for data_index in range(0, len(global_skyline)):
			#print("GLOBAL : " + str(global_skyline[data_index]))
			data = []
			for i in range(0, data_length):
				if(global_skyline[data_index][i+1] != 'null'):
					top = ct[i] + global_skyline[data_index][i+1]
					bottom = ct[i] - global_skyline[data_index][i+1]
				else:
					top = 'null'
					bottom = 'null'
				max_min_value = [top, bottom]
				data.append(max_min_value)
			ddr_prime_ct.append(data)
	# print("DDR PRIME CT : " + str(ddr_prime_ct))
	return ddr_prime_ct


def check_intersection(safe_region, ddr_prime_ct):
	# print("")
	print(">> CHECKING INTERSECTION")
	# print("SAFE_REGION  : " + str(safe_region))
	# print("DDR_PRIME_CT : " + str(ddr_prime_ct))

	global intersection
	global data_length

	intersection = []
	for safe_index in range(0, len(safe_region)):
		for ddr_index in range(0, len(ddr_prime_ct)):
			intersect_data = []
			intersect_status = True
			null_counter = 0
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
				elif(top == 'null' and bottom == 'null'):
					null_counter += 1

			#print("Intersect Status : " + str(intersect_status))
			if(intersect_status == True and null_counter != data_length):
				intersection.append(intersect_data)
	if(len(intersection) > 0):
		return True
	else:
		return False

def move_query_point():
	#Output : titik baru untuk query point q
	# print("")
	print(">> MOVING QUERY POINT")
	# print("")
	global intersection
	global query_point
	global q_cost
	global data_length
	#print("Intersection : " + str(intersection))
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

			# top_diff = abs(float(query_point[i+1]) - intersection[data_index][i][0])
			# bottom_diff = abs(float(query_point[i+1]) - intersection[data_index][i][1])
			# #minimal_distance = min(a,b)
			# if(bottom_diff < top_diff):
			# 	nearest_point.append(intersection[data_index][i][1])
			# 	nearest_distance.append(bottom_diff)
			# else:
			# 	nearest_point.append(intersection[data_index][i][0])
			# 	nearest_distance.append(top_diff)
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
	print("   MOVING QUERY POINT TO : " + str(recommendation))



def move_why_not_point(ct, q):		#q here is transformed q
	global data_length
	global ct_cost
	global node
	global local_skyline
	global candidate_skyline
	global global_skyline
	global shadow_skyline
	global virtual_point
	# print("")
	print(">> MOVING WHY-NOT POINT")
	print("   CT : " + str(ct))
	print("   Q  : " + str(q))

	#Mentransformasikan semua titik (produk) yang ada terhadap ct
	A = []
	fp = open(product_list)
	for line in fp:
		product = line.split()
		transformed_point = []
		# print("product : " + str(product))
		for i in range(0, data_length):
			if(product[i+1] != 'null'):
				#memindahkan semua data ke kanan ct, agar bisa dijadikan sebagai acuan untuk perpindahan ct
				transformed_value = ct[i] + abs(ct[i] - float(product[i+1]))
				# print("**@ o : " + str(float(product[i+1])))
				# print("**  t : " + str(transformed_value))
				# print("-")
				transformed_point.append(transformed_value)
			else:
				#ct dipindahkan karena ada suatu nilai yang membatasinya untuk mencapai q, jika tidak ada, ct tidak perlu dipindahkan
				transformed_point.append(ct[i])
		A.append(transformed_point)

	# print("A awal : ")
	# for data_index in range(0, len(A)):
	# 	print(A[data_index])

	#PASTIKAN DATA DISINI SEMUA DIMENSINYA LENGKAP

	#hilangkan semua data yang berada diatas q, data yang berada diatas q sudah pasti letaknya bawah/kiri ct
	# print("Q : " + str(q))
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
	#print("A filt : ")
	# for data_index in range(0, len(A)):
	# 	print(A[data_index])

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
	#print("A mark for dominated : ")
	# for data_index in range(0, len(A)):
	# 	print(A[data_index])
	for i in reversed(A):
		if(i[-1] == 'delete'):
			A.remove(i)
	#print("A deletion for dominated : ")
	# for data_index in range(0, len(A)):
	# 	print(A[data_index])

	#######MENDAPATKAN TITIK BARU UNTUK ct 		//A masih dalam bentuk jarak dari q
	####Output : Titik
	M = []
	for data_index in range(0, len(A)):
		data = []
		for i in range(0, data_length):
			temp = q[i] - (A[data_index][i] / 2)
			data.append(temp)
		M.append(data)

	# print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHh")
	# print("M : " + str(M))

	#Cari cost terendah :
	print("   NUMBER OF CT' RECOMMENDATION : " + str(len(M)))
	print("   LIST OF RECOMMENDATION CT' : " + str(M))
	current_cost = 99999999999
	cheapest_index = None
	for data_index in range(0, len(M)):
		total_cost = 0
		for i in range(0, data_length):
			if(M[data_index][i] != 'null'):
				total_cost += (abs(M[data_index][i] - ct[i]) * ct_cost[i])
		if(total_cost < current_cost):
			cheapest_index = data_index
			current_cost = total_cost
	for i in range(0, data_length):
		if(M[cheapest_index][i] == 'null'):
			M[cheapest_index][i] = ct[i]
	# print("Move q  TO : " + str(q))
	# print("MOVE ct TO : " + str(M[cheapest_index])) 
	best_value = {}
	best_value["q"] = list(q)
	best_value["ct"] = list(M[cheapest_index])
	best_value["cost"] = current_cost
	return best_value






def Move_Why_Not_And_Query_Point():
	global safe_region
	global query_point
	global ct
	global product_list
	global ct_cost
	global q_cost

	print(">> MOVING WHY-NOT AND QUERY POINT")

	# E adalah corner point dengan jarak terdekat ke ct,
	# Bertujuan untuk mempersingkat jarak antara ct dan q
	# q yang dipindahkan dalam area ini tidak akan kehilangan satu RSL pun
	E = []		#corner_points
	#print("SR : " + str(safe_region))
	for safe_index in range(0, len(safe_region)):
		#print("sr : " + str(safe_region[safe_index]))
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
	#print(ct)
	#print("E  : " + str(E))
	

	# Q adalah transformed space semua perpindahan query_point terhadap ct, 
	Q = []
	for data_index in range(0, len(E)):
		data = []
		for i in range(0, len(E[data_index])):
			transformed_value = float(ct[i]) + abs(float(ct[i]) - E[data_index][i])
			data.append(transformed_value)
		data.append('ok')
		Q.append(data)
	#print("Q  : " + str(Q))

	"""
	for each e1,e2 element Q such that e1 dominate e2:
		remove e2
	"""
	# eliminasi semua titik perpindahan query point yang didominasi oleh hasil lainnya.
	# titik yang didominasi sudah pasti lebih jauh dari ct
	# KARENA DATANYA TIDAK LENGKAP, PERLU DIPIKIRKAN ULANG APAKAH PERLU DILAKUKAN HAL INI
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
	#print("Qm : " + str(Q))
	for i in reversed(Q):
		if(i[-1] == 'delete'):
			Q.remove(i)
	#print("Q- : " + str(Q))


	"""
	Mc = initiate
	for each e1 element Q do:
		T -> move why not and query point /Alg 1
		Mc = Mc U T
	"""
	print("   NUMBER OF Q' RECOMMENDATION : " + str(len(Q)))
	print("   LIST OF RECOMMENDATION Q'   : " + str(Q))
	Mc = []
	# print("NNNNNNNNNNNNNNNNN ")
	# print("CT : " + str(ct))
	# print("Q  : " + str(Q))
	for data_index in range(0, len(Q)):
		T = move_why_not_point(ct, Q[data_index][:-1])
		Mc.append(T)

	cheapest_index = None
	cheapest_cost = 99999999999
	for data_index in range(0, len(Mc)):
		if(Mc[data_index]["cost"] < cheapest_cost):
			cheapest_index = data_index
	print("")
	print("   RESULT : MOVING WHY-NOT AND QUERY-POINT")
	print("   Q      : " + str(Mc[cheapest_index]["q"]))
	print("   CT     : " + str(Mc[cheapest_index]["ct"]))






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
print(">> FINISHED CALCULATING GLOBAL")
print("   TIME USED : " + str(time.time() - start_time) + " SECONDS")

ddr_prime_ct = generate_ddr_prime_ct(ct)

safe_region = generate_safe_region_q()

generate_cost()

print(">> ORIGINAL DATA : ")
print("   Q  : " + str(query_point))
print("   CT : " + str(ct))
print("   UP : " + str(user_preference))
print("   PL : " + str(product_list))
print("   D  : " + str(data_length))

if(ct_has_skyline == True):
	intersection_status = check_intersection(safe_region, ddr_prime_ct)
else:
	intersection_status = False
if(intersection_status == True):
	move_query_point()
else:
	Move_Why_Not_And_Query_Point()
#print(recommendation)
print("   NUMBER OF RSL : " + str(jumlah_rsl))
print("   LIST RSL   : " + str(list_rsl))

elapsed_time = time.time() - start_time
print("   FINAL TIME USED : " + str(elapsed_time))