#https://programmers.co.kr/learn/courses/30/lessons/77485#
def solution(rows, columns, queries):
    def my_rot(A):
        x1,y1,x2,y2 = A
        a,b = x1,y1
        result = []
        
        while b != y2:
            result.append(f'{a},{b}')
            b += 1
        
        while a != x2:
            result.append(f'{a},{b}')
            a += 1
            
        while b != y1:
            result.append(f'{a},{b}')
            b -= 1
            
        while a != x1:
            result.append(f'{a},{b}')
            a -= 1
        
        return result
         
    my_dict = dict()
    result = []
    for querie in queries:
        rot = my_rot(querie)
        my_key, my_value = [], []
        
        for value in rot:
            x,y = map(int,value.split(","))
            my_key.append(value)
            my_value.append(my_dict.get(value,(x-1)*columns + y))
        
        result.append(min(my_value))
        my_value = [my_value[-1]] + my_value[:-1]
        my_dict.update(zip(my_key,my_value))
    return result