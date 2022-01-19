#퀵 정렬

def sol(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    new = arr[1:]

    left_arr = [i for i in new if i <= pivot ]
    right_arr = [i for i in new if i > pivot]
    return sol(left_arr) + [pivot] + sol(right_arr)

print(sol([5, 7, 9, 0, 3, 1, 6, 2, 4, 8]))

import math
print(math.ceil(1/60))