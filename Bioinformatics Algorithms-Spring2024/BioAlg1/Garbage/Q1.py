def check_feasible(assignment):
    global N, K, shop_orders
    for i in range(N):
        for k in range(K):
            need = shop_orders[i][k]
            total_supply = sum(assignment[i][j][k] for j in range(M))
            if need > total_supply:
                return False
    return True

def calculate_cost(assignment):
    global N, M, K
    total_cost = 0
    for i in range(N):
        for k in range(K):
            for j in range(M):
                total_cost += assignment[i][j][k] * costs[k][i][j]
    return total_cost

while True:
    insplit = [ch for ch in input().split(" ") if len(ch) > 0]
    N, M, K = tuple(map(int, insplit))
    if N == 0 and M == 0 and K == 0:
        break
    shop_orders = [[0 for j in range(K)] for i in range(N)]
    for i in range(N):
        shop_orders[i] = list(map(int, input().split(" ")))
    supply_storage = [[0 for j in range(K)] for i in range(M)]
    for i in range(M):
        supply_storage[i] = list(map(int, input().split(" ")))
    costs = [[[0 for l in range(M)] for j in range(N)] for i in range(K)]
    for i in range(K):
        for j in range(N):
            costs[i][j] = list(map(int, input().split(" ")))


    min_cost = float('inf')
    for mask in range(1, 1 << (N * M)):
        assignment = [[[0 for _ in range(K)] for _ in range(M)] for _ in range(N)]
        for i in range(N):
            for k in range(K):
                remaining_order = shop_orders[i][k]
                for j in range(M):
                    if (mask >> (i * M + j)) & 1:
                        assigned = min(remaining_order, supply_storage[j][k])
                        assignment[i][j][k] = assigned
                        remaining_order -= assigned
                        supply_storage[j][k] -= assigned

        if check_feasible(assignment):
            min_cost = min(min_cost, calculate_cost(assignment))

    if min_cost == float('inf'):
        print(-1)
    else:
        print(min_cost)
    dummy = input()
