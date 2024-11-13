###################################################################################################################

def generate_lists_with_sum_15():
    result = []
    for i in range(1, 10):
        for j in range(1, 10):
            for k in range(1, 10):
                if i != j and i != k and j != k and i + j + k == 15:
                    result.append([i, j, k])
    return result


lists_with_sum_15 = generate_lists_with_sum_15()
# print(len(lists_with_sum_15))


def generate_combinations(array):
    combinations = []
    n = len(array)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                combinations.append([array[i], array[j], array[k]])
                combinations.append([array[i], array[k], array[j]])
                combinations.append([array[j], array[i], array[k]])
                combinations.append([array[j], array[k], array[i]])
                combinations.append([array[k], array[i], array[j]])
                combinations.append([array[k], array[j], array[i]])
    return combinations


main_list = []

for lst in lists_with_sum_15:
	otherlst = generate_combinations(lst)
	for lst2 in otherlst:
		main_list.append(lst2)
# print(len(main_list))


def magicProblem(main_list):
	matrix = [[0]*3]*3

	for i in range(len(main_list)):
		for j in range(i+1,len(main_list)):
			for m in range(j+1, len(main_list)):
				matrix[0] = main_list[i]
				matrix[1] = main_list[j]
				matrix[2] = main_list[m]

				col1 = matrix[0][0] + matrix[1][0] + matrix[2][0]
				col2 = matrix[0][1] + matrix[1][1] + matrix[2][1]
				col3 = matrix[0][2] + matrix[1][2] + matrix[2][2]
				dia1 = matrix[0][0] + matrix[1][1] + matrix[2][2]
				dia2 = matrix[0][2] + matrix[1][1] + matrix[2][0]
				check = [matrix[i][j] for i in range(3) for j in range(3)]
				if col1 == 15 and col2 == 15 and col3 == 15 and dia1 == 15 and dia2 == 15 and len(check) == len(set(check)):
					return matrix
		
print(magicProblem(main_list))
 
