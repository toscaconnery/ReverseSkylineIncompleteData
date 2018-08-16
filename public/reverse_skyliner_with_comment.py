#!/usr/bin/python

import sys
import time
from time import gmtime, strftime
import numpy as np

a = strftime("%d%H-%M%S", gmtime())
sys.stdout = open("FC_TESTING_result_" + str(a) + ".txt", "wt")


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
product_list = "TESTING_FC_D3_N100.txt"
user_preference = "TESTING_USER_D3_N10.txt"
intersection = []
ct_cost = []
q_cost = []
jumlah_rsl = 0
list_rsl = []


#Query point ditentukan disini
def generate_query_point(): #NEW
	global query_point
	query_point = "QP 85 90 80"
	#query_point = "QP 45 45 45 45"
	#query_point = "QP 70 70 70 70"


#CT ditentukan disini, jumlah data sebanyak jumlah ct
def generate_ct():
	global ct

	ct.append(float(3))
	ct.append(float(3))
	ct.append(float(3))
	#ct.append(float(10))
	
#Cost untuk perubahan tiap dimensi ditentukan disini
def generate_cost():
	global ct_cost
	global q_cost
	ct_cost.append(3)
	ct_cost.append(3)
	ct_cost.append(3)
	# ct_cost.append(2)
	q_cost.append(4)
	q_cost.append(3)
	q_cost.append(2)
	# q_cost.append(3)

#Fungsi insersi local skyline. Fungsi ini akan mengecek apakah tiap data yang diinputkan layak
#menjadi local skyline dengan cara membandingkan tiap data yang masuk dengan local skyline dari
#bucket yang sama.
def insert_local_skyline(current_specs, bitmap):
	global local_skyline
	global shadow_skyline
	global virtual_point

	#Membandingkan dengan setiap data baru dengan seluruh local sklyline yang ada pada bucket yang sama.
	for i in range(0, len(local_skyline[bitmap])):
		dominating_local = False
		dominated_by_local = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and local_skyline[bitmap][i][j] != 'null'):
				if(current_specs[j] < local_skyline[bitmap][i][j]):
					dominating_local = True
				elif(current_specs[j] > local_skyline[bitmap][i][j]):
					dominated_by_local = True
		#Tiap data yang tidak terdominasi akan diberi tanda "ok" di akhir data, sedangkan data yang
		#terdominasi akan diberi tanda "delete" di ujung datanya. 
		if(dominating_local == True and dominated_by_local == False):
			local_skyline[bitmap][i][-1] = 'delete'
		elif(dominating_local == False and dominated_by_local == True):
			for k in range(0, i+1):
				local_skyline[bitmap][k][-1] = 'ok'
			return False
	#Jika data tidak didominasi oleh local skyline lainnya, maka data akan dibandingankan dengan virtual 
	#point dari bucket yang sama.
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
	#Jika data berhasil bertahan tanpa terdominasi, maka data tersebut akan dijadikan local skyline.
	#Semua data yang telah ditandai sebagai data yang terdominasi akan dihapus disini.
	if(dominated == 0):
		content = list(current_specs)
		content.append('ok')
		local_skyline[bitmap].append(content)
		#Menghapus local skyline yang terdominasi.
		for i in sorted(local_skyline[bitmap], reverse=True):
			if (i[-1] == 'delete'):
				local_skyline[bitmap].remove(i)
		#Data yang diperiksa masih harus dibandingkan dengan shadow skyline dari bucket yang sama.
		#Shadow skyline yang terdominasi akan ditandai.
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
		#Menghapus shadow skyline yang terdominasi
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
		#Semua shadow skyline yang terdominasi dihapus disini
		for i in sorted(shadow_skyline[bitmap], reverse=True):
			if (i[-1] == 'delete'):
				shadow_skyline[bitmap].remove(i)
		#jika data yang ditinjau terdominasi oleh shadow skyline, maka data tersebut akan dimasukkan ke shadow skyline.
		content = list(current_specs)
		content.append('ok');
		shadow_skyline[bitmap].append(content)
	return False

#Fungsi insersi candidate skyline. Fungsi ini akan membandingkan data yang ditinjau dengan seluruh candidate skyline.
def insert_candidate_skyline(current_specs, bitmap):
	global candidate_skyline
	list_bit_inserted = []
	dominated = 0
	#Membandingkan dengan seluruh candidate skyline
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
		#Jika candidate skyline berhasil mendominasi data yang ditinjau, maka data tersebut akan dimasukkan kedalam virtual point
		elif(dominating_candidate == False and dominated_by_candidate == True):
			content = list(candidate_skyline[i][:-2])
			insert_virtual_point(content, bitmap)
			dominated = 1
	candidate_skyline = [i for i in candidate_skyline if i[-1] == 'ok']
	#Jika data tidak terdominasi, maka data akan dimasukkan ke candidate skyline
	if(dominated == 0):
		content = list(current_specs)
		content.append(bitmap)
		content.append('ok')
		candidate_skyline.append(content)


#Fungsi insersi virtual point, virtual point akan digunakan untuk menyaring local skyline
def insert_virtual_point(current_specs, bitmap):
	global local_skyline
	global virtual_point
	global shadow_skyline
	#Membandingkan data yang akan dijadikan virtual point dengan local skyline. Semua local skyline
	#yang terdominasi akan dipindahkan ke shadow skylne.
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
	#Pemindahan local skyline yang terdominasi ke shadow skyline
	for i in reversed(local_skyline[bitmap]):
		if (i[-1] == 'delete'):
			shadow_skyline[bitmap].append(i)
			local_skyline[bitmap].remove(i)
			shadow_skyline[bitmap][-1][-1] = 'ok'
	
	#Membandingkan data yang ditinjau dengan virtual point. Semua virtual point yang terdominasi dan
	#memiliki representasi bitmap yang sama atau bagian dari bitmap data yang ditinjau akan dihapus
	for i in range(0, len(virtual_point[bitmap])):
		dominating_virtual = False
		dominated_by_virtual = False
		superset_check = 0
		#Membandingkan dengan semua virtual point.
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
		#Menandai virtual point yang terdominasi dan memenuhi syarat penghapusan
		if(dominating_virtual == True and dominated_by_virtual == False and superset_check == len(current_specs)):
			virtual_point[bitmap][i][-1] = 'delete'
	#Menghapus virtual point yang terdominasi
	for i in reversed(virtual_point[bitmap]):
		if(i[-1] == 'delete'):
			virtual_point[bitmap].remove(i)
	content = list(current_specs)
	content.append('ok')
	virtual_point[bitmap].append(content)


#Fungsi update global skyline. Fungsi ini dijalankan ketika jumlah data dalam candidate skyline
#telah melewati batas yang telah ditentukan. Data yang berhasil bertahan pada proses ini adalah
#skyline sebenarnya dari seluruh kumpulan incomplete data yang ditinjau.
def update_global_skyline():
	global global_skyline
	global candidate_skyline
	global shadow_skyline
	global data_length
	#Membandingkan seluruh candidate skyline dengan global skyline
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
			#Candidate dan global skyline yang terdominasi akan ditandai untuk dihapus.
			if(dominating_global == True and dominating_candidate == False):
				global_skyline[g][-1] = 'delete'
			elif(dominating_global == False and dominating_candidate == True):
				candidate_skyline[c][-1] = 'delete'
	#Penghapusan global dan candidate skyline
	for i in reversed(global_skyline):
		if(i[-1] == 'delete'):
			global_skyline.remove(i)
	for i in reversed(candidate_skyline):
		if(i[-1] == 'delete'):
			candidate_skyline.remove(i)
	#Membandingkan  dengan shadow skyline dari bucket yang n_updated flag-nya bernilai True
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
	#Membandingkan dengan candidate skyline.
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



#Fungsi ini akan menentukan konsumen mana saja yang akan menjadikan data point yang sedang diperiksa sebagai bagian dari skylinenya.
#Nilai spesifikasi produk yang diproses dalam fungsi ini merupakan nilai yang telah ditransformasikan terhadap titik query point
#yang telah dilakukan dalam fungsi-fungsi sebelumnya
def calculate_rsl_q(customer_skyline, query_point):
	global data_length
	for dict_index in customer_skyline:
		transformed_query_point = []
		#Mentransformasikan query point terhadap preferensi pengguna sehingga query point bisa dibandingkan data lain dari 
		#produk yang berhasil menjadi skyline bagi preferensi pengguna tersebut.
		for q in range(0, data_length):
			transformed_value = abs(float(query_point[q+1]) - customer_skyline[dict_index][-2][q])
			transformed_query_point.append(transformed_value)
		#Membandingkan query point dengan seluruh produk yg berhasil menjadi skyline dari preferensi pengguna
		for data_index in range(0, len(customer_skyline[dict_index]) - 2):
			dominating_q = False
			dominating_customer = False
			for i in range(0, data_length):
				if(customer_skyline[dict_index][data_index][i+1] != 'null'):
					if(customer_skyline[dict_index][data_index][i+1] < transformed_query_point[i]):
						dominating_q = True
					elif(customer_skyline[dict_index][data_index][i+1] > transformed_query_point[i]):
						dominating_customer = True
			#Jika query point terdominasi, maka kumpulan skyline ini akan ditandai dan tidak dianggap sebagai reverse skyline dari query point q
			if(dominating_q == True and dominating_customer == False):
				customer_skyline[dict_index][-1] = 'delete'
			#Jika query point tidak terdominasi, maka semua data dari skyline yang berhasil didominasi oleh q akan ditandai untuk dihapus
			elif(dominating_q == False and dominating_customer == True):
				customer_skyline[dict_index][data_index][-1] = 'delete'
		#Menghapus kumpulan skyline yang tidak berhasil menjadi reverse skyline dari query point
		if(customer_skyline[dict_index][-1] == 'ok'):
			for i in range(len(customer_skyline[dict_index]) - 3, -1, -1):
				if(customer_skyline[dict_index][i][-1] == 'delete'):
					customer_skyline[dict_index].remove(customer_skyline[dict_index][i])
		#Menghapus semua kumpulan skyline yang tidak memiliki anggota. Kumpulan skyline yang tidak memiliki anggota tidak termasuk reverse skyline dari q
		if(len(customer_skyline[dict_index]) <= 2):
			customer_skyline[dict_index][-1] = 'delete'
	return customer_skyline



#Fungsi untuk menentukan safe region. Query point akan bebas bergerak dalam wilayah safe region.
#Fungsi ini akan mengambil irisan dari semua wilayah ddr prime dari setiap kumpulan skyline.
#Kumpulan skyline yang diolah adalah skyline yang menjadi RSL dari q
def generate_safe_region_q():
	global customer_skyline
	global query_point
	global safe_region
	global data_length
	global jumlah_rsl
	global ct
	global start_time

	query_point = query_point.split()
	calculate_rsl_q(customer_skyline, query_point)
	
	#Mengubah tipe query point menjadi float
	q = []
	for i in range(0, data_length):
		q.append(float(query_point[i+1]))

	#Safe region adalah jarak dari tiap user preference ke DDR Prime nya masing-masing untuk tiap dimensi
	safe_region = []
	for dict_index in customer_skyline:
		#Hanya mengolah himpunan data skyline yang memiliki data lebih dari dua. Dua data terakhir adalah keterangan dari himpunan tersebut.
		#Hanya mengolah himpunan data skyline yang ditandai 'ok' (menjadi RSL dari query point)
		if(customer_skyline[dict_index][-1] == 'ok' and len(customer_skyline)>2):
			jumlah_rsl += 1
			list_rsl.append(dict_index)
			ddr_prime = []
			for data_index in range(0, len(customer_skyline[dict_index])-2):
				data = []
				#Untuk mempermudah, wilayah safe region akan diinterpretasikan sebagai garis lurus dalam tiap dimensi
				#Wilayah safe region merupakan wilayah diantara nilai tranformasi minimum dan maximum dari tiap data terhadap preferensi pengguna
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
			#query point q juga harus dibandingkan karena q juga adalah bagian RSL dari customer skyline ini
			data = []
			for i in range(0, data_length):
				diff = abs(float(q[i]) - customer_skyline[dict_index][-2][i])
				top = customer_skyline[dict_index][-2][i] + diff
				bottom = customer_skyline[dict_index][-2][i] - diff
				max_min_value = [top, bottom]
				data.append(max_min_value)
			ddr_prime.append(data)
			#filtering, mendapatkan semua safe region yang mengandung q di dalamnya
			used_ddr_prime = []
			for data_index in range(0, len(ddr_prime)):
				q_dimension_counter = 0
				for i in range(0, data_length):
					if(ddr_prime[data_index][i][0] != 'null'):
						if(ddr_prime[data_index][i][0] >= float(q[i]) and ddr_prime[data_index][i][1] <= float(q[i])):
							q_dimension_counter += 1
					else:
						#Nilai 'null' tidak bisa dihitung namun tidak bisa mendominasi data lain. Atau dengan kata lain, nilai 'null' tidak memberikan
						#efek terhadap luas wilayah yang akan digunakan. Nilai 'null' akan mingikuti batasan wilayah yang ditentutkan oleh data lainnya.
						q_dimension_counter += 1
				#Hanya wilayah yang memenuhi kriteria yang telah ditentukan yang akan dijadikan safe region baru. Wilayah ini akan mengecil tiap kali
				#dibandingkan dengan data lainnya.
				if(q_dimension_counter == data_length):
					used_ddr_prime.append(ddr_prime[data_index])
			ddr_prime = list(used_ddr_prime)

			#penentuan safe region untuk data pertama
			if(len(safe_region) == 0):
				safe_region = list(ddr_prime)
			#penentuan safe region jika sudah ada safe region sebelumnya. safe region berikutnya adalah irisan dari ddr prime data berikutnya dengan
			#wilayah safe region yang lama.
			else:
				#Melakukan pengecekan irisan 
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
							if(top != 'null' and bottom != 'null'):
								if(bottom > top):
									intersect_status = False
							max_min_value = [top, bottom]
							intersect_data.append(max_min_value)
						if(intersect_status == True):
							new_safe_region.append(intersect_data)
				#Hanya data irisan baru yang meliki jumlah lebih dari 0 yang bisa dikatakan beririsan. Maka hanya new_safe_region dengan panjang lebih dari 0
				#yang bisa dijadikan safe region baru. List new_safe_region dengan panjang 0 mengindikasikan tidak terjadinya irisan sehingga tidak perlu
				#dianggap sebagai safe region baru.
				if(len(new_safe_region) > 0):
					safe_region = list(new_safe_region)
	# print("   NUMBER OF RSL : " + str(jumlah_rsl))
	# print("   SAFE REGION Q : " + str(safe_region))

	#Bisa saja terjadi kondisi dimana query point q tidak memiliki safe region. Jika hal ini terjadi, maka cukup memindahkan data point ct ke dekat q
	if(len(safe_region) == 0):
		print("## Q DOESN'T HAVE SAFE REGION, SPECIAL TREATMENT NEEDED, MOVING CT TO Q")
		generate_cost()
		T = move_why_not_point(ct, q)

		print("")
		print("   RESULT : MOVING WHY-NOT POINT")
		print("   Q      : " + str(T["q"]))
		print("   CT     : " + str(T["ct"]))

		elapsed_time = time.time() - start_time
		print("   FINAL TIME USED : " + str(elapsed_time))

		exit()
	return safe_region




def generate_ddr_prime_ct(ct):
	print(">> GENERATING DDR PRIME CT")
	#This function will check if query_point is included to ct's skyline
	#It will return Ct DDR Prime and status of query point
	#Di fungsi ini juga akan ditentukan apakah query point q merupakan bagian skyline dari ct atau tidak.
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
	#global global_skyline
	ct_has_skyline = True

	fp = open(product_list)
	#Karena nilai global skyline dari tiap customer skyline berbeda-beda, maka disini tidak menggunakan variabel global dari global skyline
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
	#Karena query point q hanya ada satu data, maka akan dibandingkan dengan cara normal tanpa perlu menggunakan metode iskyline 
	#mengubah q
	q = query_point.split()
	for i in range(0, data_length):
		q[i+1] = abs(float(q[i+1]) - ct[i])
	q.append("qp")		#tanda bahwa data ini adalah query point
	q.append("ok")		#status dari query point

	#Menentukan apakah query point termasuk skyline dari ct
	#Semua penyesuaian hanya perlu dijalankan jika query point tidak termasuk sebagai skyline dari ct
	q_is_skyline = True
	for data_index in range(0, len(global_skyline)):
		smaller = False
		greater = False
		for i in range(0, data_length):
			if(q[i+1] < ct[i]):
				smaller = True
			elif(q[i+1] > ct[i]):
				greater = True
		if(smaller == False and greater == True):
			q_is_skyline = False

	if(len(global_skyline) == 0):
		print("## CT DOESN'T HAVE ANY SKYLINE, SPECIAL TREATMENT NEEDED, MOVING CT TO Q")
		elapsed_time = time.time() - start_time
		ct_has_skyline = False
	#print("   CT SKYLINE : " + str(global_skyline))
	if(q_is_skyline == True):
		#Jika query point merupakan bagian dari skyline, tidak ada perubahan yang perlu dilakukan.
		#Program akan dihentikan sampai disini.
		print("   TIDAK PERLU DILAKUKAN PENYESUAIAN")
		elapsed_time = time.time() - start_time
		print("   TIME USED : " + str(elapsed_time))
		exit()
	else:
		#Menentukan wilayah DDR Prime CT (maksimum dan minimum dari tiap dimensi)
		ddr_prime_ct = []
		for data_index in range(0, len(global_skyline)):
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
	return ddr_prime_ct


#Fungsi ini digunakan untuk menentukan apakah Safe Region dan DDR Prime CT memiliki intersection.
#Hal ini akan menentukan tindakan apa yang akan dilakukan demi meenjadikan query point q sebagai skyline ct
def check_intersection(safe_region, ddr_prime_ct):
	global intersection
	global data_length

	#Melakukan perulangan didalam safe region q dan ddr prime ct
	intersection = []
	for safe_index in range(0, len(safe_region)):
		for ddr_index in range(0, len(ddr_prime_ct)):
			intersect_data = []
			intersect_status = True
			null_counter = 0
			for i in range(0, data_length):
				#Membandingkan nilai maximum dari kedua variabel
				#Nilai yang akan digunakan adalah nilai terendah dari kedua nilai maximum
				#top
				if(safe_region[safe_index][i][0] == 'null' and ddr_prime_ct[ddr_index][i][0] == 'null'):
					top = 'null'
				elif(safe_region[safe_index][i][0] == 'null'):
					top = ddr_prime_ct[ddr_index][i][0]
				elif(ddr_prime_ct[ddr_index][i][0] == 'null'):
					top = safe_region[safe_index][i][0]
				else:
					top = min(safe_region[safe_index][i][0], ddr_prime_ct[ddr_index][i][0])

				#Membandingkan nilai minimum dari kedua variabel
				#Nilai yang akan digunakan adalah nilai tertinggi dari kedua minimum
				#bottom
				if(safe_region[safe_index][i][1] == 'null' and ddr_prime_ct[ddr_index][i][1] == 'null'):
					bottom = 'null'
				elif(safe_region[safe_index][i][1] == 'null'):
					bottom = ddr_prime_ct[ddr_index][i][1]
				elif(ddr_prime_ct[ddr_index][i][1] == 'null'):
					bottom = safe_region[safe_index][i][1]
				else:
					bottom = max(safe_region[safe_index][i][1], ddr_prime_ct[ddr_index][i][1])
				#Menyimpan nilai minimum dan maximum yang terpilih untuk dihitung jumlahnya
				max_min_value = [top, bottom]
				intersect_data.append(max_min_value)

				#Mengecek apakah terjadi intersection dari kedua variabel. 
				if(top != 'null' and bottom != 'null'):
					if(bottom > top):
						intersect_status = False
				elif(top == 'null' and bottom == 'null'):
					null_counter += 1

			if(intersect_status == True and null_counter != data_length):
				intersection.append(intersect_data)
	if(len(intersection) > 0):
		#Jika terdapat intersection
		return True
	else:
		#Jika tidak terdapat intersection
		return False

#Fungsi ini memberikan rekomendasi titik baru untuk query point yang paling optimal
def move_query_point():
	global intersection
	global query_point
	global q_cost
	global data_length

	modified_value = []
	distance_value = []
	#Perulangan untuk setiap intersection yang ada
	for data_index in range(0, len(intersection)):
		nearest_point = []
		nearest_distance = []
		for i in range(0, data_length):
			top_diff = abs(float(query_point[i+1]) - intersection[data_index][i][0])
			bottom_diff = abs(float(query_point[i+1]) - intersection[data_index][i][1])
			if(bottom_diff < top_diff):
				nearest_point.append(intersection[data_index][i][1])
				nearest_distance.append(bottom_diff)
			else:
				nearest_point.append(intersection[data_index][i][0])
				nearest_distance.append(top_diff)
		modified_value.append(nearest_point)
		distance_value.append(nearest_distance)

	#Mencari perubahan query point yang paling efisien, dengan cara mentotalkan nilai distance * weight
	#Hasil sum yang paling rendah akan disimpan indexnya sebagai penanda bahwa perubahan tersebut adalah yang paling efisien.
	cheapest_index = None
	current_cost = 99999999999
	for data_index in range(0, len(modified_value)):
		total_cost = 0
		for i in range(0, data_length):
			total_cost += (distance_value[data_index][i] * q_cost[i])
		if(total_cost < current_cost):
			cheapest_index = data_index
	recommendation = modified_value[cheapest_index]
	print("   MOVING QUERY POINT TO : " + str(recommendation))



#Fungsi ini menentukan perubahan paling efisien pada why-not point ct
def move_why_not_point(ct, q):		#q here is transformed q
	global data_length
	global ct_cost
	global node
	global local_skyline
	global candidate_skyline
	global global_skyline
	global shadow_skyline
	global virtual_point

	#Mentransformasikan semua titik (produk) yang ada terhadap ct
	A = []
	fp = open(product_list)
	for line in fp:
		product = line.split()
		transformed_point = []
		for i in range(0, data_length):
			if(product[i+1] != 'null'):
				#memindahkan semua data ke kanan ct, agar bisa dijadikan sebagai acuan untuk perpindahan ct
				transformed_value = ct[i] + abs(ct[i] - float(product[i+1]))
				transformed_point.append(transformed_value)
			else:
				#ct dipindahkan karena ada suatu nilai yang membatasinya untuk mencapai q, jika tidak ada, ct tidak perlu dipindahkan
				transformed_point.append(ct[i])
		A.append(transformed_point)


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
	for i in reversed(A):
		if(i[-1] == 'delete'):
			A.remove(i)

	#Mendapatkan titik baru untuk CT
	#Variabel A masih dalam bentuk jarak dari q
	#Output : titik
	M = []
	for data_index in range(0, len(A)):
		data = []
		for i in range(0, data_length):
			temp = q[i] - (A[data_index][i] / 2)
			data.append(temp)
		M.append(data)

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
	global start_time


	# E adalah corner point dengan jarak terdekat ke ct,
	# Bertujuan untuk mempersingkat jarak antara ct dan q
	# q yang dipindahkan dalam area ini tidak akan kehilangan satu RSL pun
	E = []		#corner_points
	for safe_index in range(0, len(safe_region)):
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
	for i in reversed(Q):
		if(i[-1] == 'delete'):
			Q.remove(i)


	"""
	Mc = initiate
	for each e1 element Q do:
		T -> move why not and query point /Alg 1
		Mc = Mc U T
	"""
	# print("   NUMBER OF Q' RECOMMENDATION : " + str(len(Q)))
	# print("   LIST OF RECOMMENDATION Q'   : " + str(Q))
	Mc = []
	for data_index in range(0, len(Q)):
		T = move_why_not_point(ct, Q[data_index][:-1])
		Mc.append(T)

	#Mencari cost perubahan terendah
	cheapest_index = None
	cheapest_cost = 99999999999
	for data_index in range(0, len(Mc)):
		if(Mc[data_index]["cost"] < cheapest_cost):
			cheapest_index = data_index
	print("")
	print("   RESULT : MOVING WHY-NOT AND QUERY-POINT")
	print("   Q      : " + str(Mc[cheapest_index]["q"]))
	print("   CT     : " + str(Mc[cheapest_index]["ct"]))

	elapsed_time = time.time() - start_time
	print("   FINAL TIME USED : " + str(elapsed_time))



#Mempersiapkan data untuk diolah.
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
	#Data produk disekitar yang diproses akan ditransformasikan terhadap spesifikasi produk yang akan ditinjau (ct)
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


#Program dasar
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
	if(len(global_skyline) > 0):
		customer_skyline[str(customer_index)] = list(global_skyline)
		customer_skyline[str(customer_index)].append(list(list_customer[x]))
		customer_skyline[str(customer_index)].append("ok")
		customer_index += 1
fu.close()
print(">> FINISHED CALCULATING GLOBAL")
print("   TIME USED : " + str(time.time() - start_time) + " SECONDS")

generate_query_point()

print(">> ORIGINAL DATA : ")
print("   Query Pnt : " + str(query_point))
print("   CT Point  : " + str(ct))
print("   User Pref : " + str(user_preference))
print("   Prod List : " + str(product_list))
print("   Dimension : " + str(data_length))

ddr_prime_ct = generate_ddr_prime_ct(ct)

safe_region = generate_safe_region_q()

generate_cost()


if(ct_has_skyline == True):
	intersection_status = check_intersection(safe_region, ddr_prime_ct)
else:
	intersection_status = False
if(intersection_status == True):
	move_query_point()
else:
	Move_Why_Not_And_Query_Point()
print("   NUMBER OF RSL : " + str(jumlah_rsl))
print("   LIST RSL   : " + str(list_rsl))

elapsed_time = time.time() - start_time
print("   FINAL TIME USED : " + str(elapsed_time))