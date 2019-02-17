import sys
import heapq
import numpy as np
sys.setrecursionlimit(1000000)


def bleedingInk(rows, cols, inks):
    grids = [[0] * cols for _ in range(rows)]
    # Start from the ink point with the maximal value.
    heap = []
    for i, j, val in inks:
        heapq.heappush(heap, (-val, i, j))

    # Recursion for every ink point in the heap
    while heap:
        val, i, j = heapq.heappop(heap)
        # if the current value is greater or equal to the ink, continue
        if grids[i][j] >= -val:
            continue

        dfs(grids, i, j, -val)

    #return np.sum(grids)
    return sum(sum(i) for i in grids)


def dfs(grids, i, j, val):
    if 0 <= i < len(grids) and 0 <= j < len(grids[0]) and grids[i][j] < val:
        grids[i][j] = val
        dfs(grids, i, j + 1, val - 1)
        dfs(grids, i, j - 1, val - 1)
        dfs(grids, i + 1, j, val - 1)
        dfs(grids, i - 1, j, val - 1)


if __name__ == '__main__':
    # get a integer
    N = int(input())

    for i in range(N):
        # get two integers separated with half-width break
        H, W = map(int, input().split())
        # get a string
        inks = []
        numDots = int(input())
        for j in range(numDots):
            ink = list(map(int, input().split()))
            inks.append(ink)
            res = bleedingInk(rows=H, cols=W, inks=inks)
            pass
        print(res)
        pass

    pass