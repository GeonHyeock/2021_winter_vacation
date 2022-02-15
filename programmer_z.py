
import copy
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
         
    my_dict = dict(zip(
        [f'{a},{b}' for a in range(1,rows+1) for b in range(1,columns+1)],
        [i for i in range(1,rows*columns+1)]))
    
    result = []
    for i in queries:
        rot = my_rot(i)
        result.append(min([my_dict[mat] for mat in rot]))
        my_dict2 = copy.deepcopy(my_dict)
        
        for j in range(len(rot)-1):
            my_dict[rot[j+1]] = my_dict2[rot[j]]
        my_dict[rot[0]] = my_dict2[rot[len(rot)-1]]
        
    return result