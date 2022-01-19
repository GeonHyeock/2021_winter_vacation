# 순열 구하기

def sol(arr,n):
    result = []
    if n == 0:
        return [[]]
    
    for idx, i in enumerate(arr):
        for j in sol(arr[:idx]+arr[idx+1:],n-1):
            result += [[i]+j]

    return result

print(sol([1,2,3],3))