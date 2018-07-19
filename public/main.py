#!/usr/bin/python

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
	
	q = []
	for i in range(0, data_length):
		q.append(float(query_point[i+1]))

	safe_region = []
	for dict_index in customer_skyline:		#c is dictionary index
		if(customer_skyline[dict_index][-1] == 'ok' and len(customer_skyline)>2):
			jumlah_rsl += 1
			list_rsl.append(dict_index)
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
			data = []
			for i in range(0, data_length):
				diff = abs(float(q[i]) - customer_skyline[dict_index][-2][i])
				top = customer_skyline[dict_index][-2][i] + diff
				bottom = customer_skyline[dict_index][-2][i] - diff
				max_min_value = [top, bottom]
				data.append(max_min_value)
			ddr_prime.append(data)
			used_ddr_prime = []
			for data_index in range(0, len(ddr_prime)):
				q_dimension_counter = 0
				for i in range(0, data_length):
					if(ddr_prime[data_index][i][0] != 'null'):
						if(ddr_prime[data_index][i][0] >= float(q[i]) and ddr_prime[data_index][i][1] <= float(q[i])):
							q_dimension_counter += 1
					else:
						q_dimension_counter += 1


				if(q_dimension_counter == data_length):
					used_ddr_prime.append(ddr_prime[data_index])
			ddr_prime = list(used_ddr_prime)

			if(len(safe_region) == 0):
				safe_region = list(ddr_prime)
			else:
				new_safe_region = []
				for safe_index in range(0, len(safe_region)):
					for ddr_index in range(0, len(ddr_prime)):
						intersect_status = True
						intersect_data = []
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
				if(len(new_safe_region) > 0):
					safe_region = list(new_safe_region)
	if(len(safe_region) == 0):
		generate_cost()
		T = move_why_not_point(ct, q)

		print("")
		print("   RESULT : MOVING WHY-NOT POINT")
		print("   Q      : " + str(T["q"]))
		print("   CT     : " + str(T["ct"]))

		exit()
	return safe_region




def generate_ddr_prime_ct(ct):
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

	ct_has_skyline = True

	fp = open(product_list)
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

	if(len(global_skyline) == 0):
		elapsed_time = time.time() - start_time
		ct_has_skyline = False
	if(q_is_skyline == True):
		#HENTIKAN PROGRAM
		print("   TIDAK PERLU DILAKUKAN PENYESUAIAN")
		exit()
	else:
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


def check_intersection(safe_region, ddr_prime_ct):
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

			if(intersect_status == True and null_counter != data_length):
				intersection.append(intersect_data)
	if(len(intersection) > 0):
		return True
	else:
		return False

def move_query_point():
	global intersection
	global query_point
	global q_cost
	global data_length
	modified_value = []
	distance_value = []
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
	cheapest_index = None
	current_cost = 99999999999
	for data_index in range(0, len(modified_value)):
		total_cost = 0
		for i in range(0, data_length):
			total_cost += (distance_value[data_index][i] * q_cost[i])
		if(total_cost < current_cost):
			cheapest_index = data_index
	recommendation = modified_value[cheapest_index]



def move_why_not_point(ct, q):		#q here is transformed q
	global data_length
	global ct_cost
	global node
	global local_skyline
	global candidate_skyline
	global global_skyline
	global shadow_skyline
	global virtual_point

	A = []
	fp = open(product_list)
	for line in fp:
		product = line.split()
		transformed_point = []
		for i in range(0, data_length):
			if(product[i+1] != 'null'):
				transformed_value = ct[i] + abs(ct[i] - float(product[i+1]))
				transformed_point.append(transformed_value)
			else:
				transformed_point.append(ct[i])
		A.append(transformed_point)

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
	M = []
	for data_index in range(0, len(A)):
		data = []
		for i in range(0, data_length):
			temp = q[i] - (A[data_index][i] / 2)
			data.append(temp)
		M.append(data)
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


	E = []		#corner_points
	for safe_index in range(0, len(safe_region)):
		corner_points = []
		for i in range(0, len(safe_region[safe_index])):
			top_diff = abs(safe_region[safe_index][i][0] - float(ct[i]))
			bottom_diff = abs(safe_region[safe_index][i][1] - float(ct[i]))
			if(top_diff <= bottom_diff):
				corner_points.append(safe_region[safe_index][i][0])
			elif(top_diff > bottom_diff):
				corner_points.append(safe_region[safe_index][i][1])
		E.append(corner_points)
	Q = []
	for data_index in range(0, len(E)):
		data = []
		for i in range(0, len(E[data_index])):
			transformed_value = float(ct[i]) + abs(float(ct[i]) - E[data_index][i])
			data.append(transformed_value)
		data.append('ok')
		Q.append(data)
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

	Mc = []
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
