
import copy
def solution(rows, columns, queries):
    def my_rot(A):
        x1,y1,x2,y2 = A
        a,b = x1,y1
        result = []
        
        while b != y2:
            result.append((a,b))
            b += 1
        
        while a != x2:
            result.append((a,b))
            a += 1
            
        while b != y1:
            result.append((a,b))
            b -= 1
            
        while a != x1:
            result.append((a,b))
            a -= 1
        
        return result
         
    my_dict = dict()
    
    result = []
    for querie in queries:
        rot = my_rot(querie)
        my_key = [value for value in rot]
        my_value = [my_dict.get(value,(value[0]-1)*columns + value[1])
                    for value in rot]
        
        result.append(min(my_value))
        my_dict = dict(zip(my_key,my_value))
    return my_dict

print(solution(6,6,[[2, 2, 5, 4], [3, 3, 6, 6], [5, 1, 6, 3]]))