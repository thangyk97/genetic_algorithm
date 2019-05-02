import numpy as np 

def split_base_decode(routes, c, q):
    Q = 9
    N = len(routes)
    F = [0] + [float('inf')] * (N)
    P = [0] * (N + 1)

    for i in range(1, N + 1):
        demand = 0
        cost = 0
        j = i
        print("====================================")
        while j <= N and demand < Q:
            demand += q[routes[j-1]]
            if i == j:
                cost = c[0, routes[j-1]] + c[routes[j-1], 0]
            else:
                cost += c[routes[j-2], routes[j-1]] + c[routes[j-1], 0] - c[routes[j-2], 0]

            if demand < Q:
                print(F[i-1] + cost)
                if F[i-1] + cost < F[j]:
                    F[j] = F[i-1] + cost
                    P[j] = i - 1
            j += 1
    # split
    print(F)
    print(P)

    return routes

routes = [1, 2, 3, 4, 5]
c = np.zeros((6, 6))
c[0, 1] = c[1, 0] = 15
c[0, 2] = c[2, 0] = 20
c[0, 3] = c[3, 0] = 35
c[0, 4] = c[4, 0] = 45
c[0, 5] = c[5, 0] = 40
c[1, 2] = c[2, 1] = 10
c[2, 3] = c[3, 2] = 25
c[3, 4] = c[4, 3] = 30
c[4, 5] = c[5, 4] = 20
c[5, 1] = c[1, 5] = 38

q = [0, 5, 4, 4, 2, 7]

print(c)

split_base_decode(routes, c, q)