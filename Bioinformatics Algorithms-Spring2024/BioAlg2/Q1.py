import numpy as np
# import time
n, p, q = map(int, input().split())
my_matrix = np.zeros((n + 1, n + 2 + 1 + 1), dtype=float)

for i in range(n):
    ai, bi = map(int, input().split())
    my_matrix[i][0] = ai
    my_matrix[i][1] = bi
    my_matrix[i][1 + (i + 1)] = 1
    my_matrix[i][-1] = 1

my_matrix[-1][0] = -1 * p
my_matrix[-1][1] = -1 * q
my_matrix[-1][n + 2] = 1
# print("initial matrix\n", my_matrix)

while True:
    last_row = my_matrix[-1]
    chosen_col = np.argmin(last_row[:-1])
    if last_row[chosen_col] >= 0:
        break
    # print(chosen_col)
    bottleneck_val = 10**6
    chosen_row = 0
    for i in range(n):
        if my_matrix[i][chosen_col] == 0:
            continue
        val = my_matrix[i][-1] / my_matrix[i][chosen_col]
        if val < bottleneck_val:
            bottleneck_val = val
            chosen_row = i
    # print((chosen_col, chosen_row))
    my_matrix[chosen_row] /= my_matrix[chosen_row][chosen_col]
    for j in range(n + 1):
        if j == chosen_row:
            continue
        my_matrix[j] += (-1 * my_matrix[j][chosen_col]) * my_matrix[chosen_row]
    # print(my_matrix)
    # time.sleep(0.25)

print(my_matrix[-1][-1])