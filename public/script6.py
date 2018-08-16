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


#Fungsi insersi local skyline. Fungsi ini akan mengecek apakah tiap data yang diinputkan layak
#menjadi local skyline dengan cara membandingkan tiap data yang masuk dengan local skyline dari
#bucket yang sama.
def Insert_Local_Skyline(current_specs, current_bit, dict_index):
	print("Insert_Local_Skyline : " + str(current_specs))
	global local_skyline
	global shadow_skyline
	global virtual_point

	#Membandingkan dengan setiap data baru dengan seluruh local sklyline yang ada pada bucket yang sama.
	for i in range(0, len(local_skyline[current_bit])):
		dominating_local = False
		dominated_by_local = False
		for j in range(0, len(current_specs)):
			if(current_specs[j] != 'null' and local_skyline[current_bit][i][j] != 'null'):
				if(current_specs[j] < local_skyline[current_bit][i][j]):
					dominating_local = True
				elif(current_specs[j] > local_skyline[current_bit][i][j]):
					dominated_by_local = True
		#Tiap data yang tidak terdominasi akan diberi tanda "ok" di akhir data, sedangkan data yang
		#terdominasi akan diberi tanda "delete" di ujung datanya. 
		if(dominating_local == True and dominated_by_local == False):
			local_skyline[current_bit][i][-1] = 'delete'
		elif(dominating_local == False and dominated_by_local == True):
			for k in range(0, i+1):
				local_skyline[current_bit][k][-1] = 'ok'
			return False
	#Jika data tidak didominasi oleh local skyline lainnya, maka data akan dibandingankan dengan virtual point dari bucket yang sama.
	dominated = 0
	for i in range(0, len(virtual_point[current_bit])):
		dominating_virtual = False
		dominated_by_virtual = False

		for j in range(0, len(current_specs)):
			if(current_specs[j] != 'null' and virtual_point[current_bit][i][j] != 'null'):
				if(current_specs[j] < virtual_point[current_bit][i][j]):
					dominating_virtual = True
				elif(current_specs[j] > virtual_point[current_bit][i][j]):
					dominated_by_virtual = True
		if(dominating_virtual == False and dominated_by_virtual == True):
			dominated = 1
			break
	#Jika data berhasil bertahan tanpa terdominasi, maka data tersebut akan dijadikan local skyline.
	#Semua data yang telah ditandai sebagai data yang terdominasi akan dihapus disini.
	if(dominated == 0):
		content = list(current_specs)
		content.append('ok')
		local_skyline[current_bit][dict_index].append(content)
		#Menghapus local skyline yang terdominasi.
		for i in sorted(local_skyline[current_bit], reverse=True):
			if (i[-1] == 'delete'):
				local_skyline[current_bit].remove(i)
		#Data yang diperiksa masih harus dibandingkan dengan shadow skyline dari bucket yang sama.
		#Shadow skyline yang terdominasi akan ditandai.
		for i in range(0, len(shadow_skyline[current_bit])):
			dominating_shadow = False
			dominated_by_shadow = False
			for j in range(0, len(current_specs)):
				if(current_specs[j] != 'null' and shadow_skyline[current_bit][i][j] != 'null'):
					if(current_specs[j] < shadow_skyline[current_bit][i][j]):
						dominating_shadow = True
					elif(current_specs[j] > shadow_skyline[current_bit][i][j]):
						dominated_by_shadow = True
			if(dominating_shadow == True and dominated_by_shadow == False):
				shadow_skyline[current_bit][i][-1] = 'delete'
		#Menghapus shadow skyline yang terdominasi
		for i in sorted(shadow_skyline[current_bit], reverse=True):
			if (i[-1] == 'delete'):
				shadow_skyline[current_bit].remove(i)
		return True
	elif(dominated == 1):
		n_updated_flag[current_bit] = True
		for i in range(0, len(shadow_skyline[current_bit])):
			dominating_shadow = False
			dominated_by_shadow = False
			for j in range(0, len(current_specs)):
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
		#jika data yang ditinjau terdominasi oleh shadow skyline, maka data tersebut akan dimasukkan ke shadow skyline.
		content = list(current_specs)
		content.append('ok');
		shadow_skyline[current_bit].append(content)
	return False


#Fungsi insersi candidate skyline. Fungsi ini akan membandingkan data yang ditinjau dengan seluruh candidate skyline.
def Insert_Candidate_Skyline(current_specs, current_bit):
	global candidate_skyline
	list_bit_inserted = []
	dominated = 0
	#Membandingkan dengan seluruh candidate skyline
	for i in range(0, len(candidate_skyline)):
		dominating_candidate = False
		dominated_by_candidate = False
		for j in range(0, len(current_specs)):
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
		#Jika candidate skyline berhasil mendominasi data yang ditinjau, maka data tersebut akan dimasukkan kedalam virtual point
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
	#Move all dominated local_skyline N to shadow_skyline
	for i in range(0, len(local_skyline[current_bit])):
		dominating_local = False
		dominated_by_local = False
		for j in range(0, len(current_specs)):
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
	
	#Remove all dominated virtual_point that has same bit
	for i in range(0, len(virtual_point[current_bit])):
		dominating_virtual = False
		dominated_by_virtual = False
		superset_check = 0

		for j in range(0, len(current_specs)):
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
			for i in range(0, data_length):
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
					for j in range(0, data_length):
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
				for j in range(0, data_length):
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


product_specs = np.loadtxt('product_specs.txt', skiprows=1, unpack=True)
user_preference = np.loadtxt('user_preference.txt', skiprows=1, unpack=True)
current_product = np.loadtxt('current_product.txt', skiprows=1, unpack=True)

product_data = {}

for x in range(0, len(user_preference[0])):
	fp = open("labeled_unsorted_paper_data.txt")
	#Membersihkan semua variabel yang akan digunakan untuk tiap proses penentuan skyline.
	node.clear()
	local_skyline.clear()
	candidate_skyline.clear()
	global_skyline.clear()
	shadow_skyline.clear()
	virtual_point.clear()
	
	number_of_preference += 1
	for line in fp:
		#Mempersiapkan data yang akan diolah.
		current_bit = ""
		current_spec = line.split()
		data_length = len(current_spec)
		dict_index = current_spec[0]
		data = []
		#Menentukan representasi bitmap dari kelengkapan data yang akan diolah. Data yang hilang akan digantikan dengan "null".
		for i in range(1, data_length):
			if(current_spec[i] == "null"):
				current_bit += "0"
				data.append("null")
			else:
				current_bit += "1"
				difference = abs(int(current_spec[i]) - user_preference[i-1][x])
				data.append(difference)
		#Inisialisasi bucket. Berlaku untuk tiap data pertama dari setiap bucket.
		if current_bit not in node:
			node[current_bit] = {}
			node[current_bit][dict_index] = []
			node[current_bit][dict_index].append(data)
			local_skyline[current_bit] = {}
			shadow_skyline[current_bit] = []
			virtual_point[current_bit] = []
			n_updated_flag[current_bit] = False
		#Memasukkan data ke bucket yang telah ada.
		else:
			node[current_bit][dict_index] = []
			node[current_bit][dict_index].append(data)

		#Proses insersi local skyline.
		is_skyline = Insert_Local_Skyline(data, current_bit, dict_index)
		if is_skyline == True:
			#Jika sebuah data berhasil menjadi local skyline, akan langsung dicek apakah data tersebut layak untuk
			#menjadi candidate skyline. Jumlah candidate skyline akan dibatasi oleh variabel t. Jika jumlah candidate
			#skyline melewati jumlah t, maka akan dilakuan proses pengecekan global skyline.
			Insert_Candidate_Skyline(data, current_bit)
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
	