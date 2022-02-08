#https://programmers.co.kr/learn/courses/30/lessons/87377

def solution(line):
    def vertex(K) -> list:
        A,B = K
        mo = A[0]*B[1] - A[1]*B[0] # AD-BC
        if mo == 0:
            return True
        x = A[1]*B[2] - A[2]*B[1]
        y = A[2]*B[0] - A[0]*B[2] 
        return x/mo,y/mo
    
    def combi(A,k=2):
        if k == 0:
            return [[]]
        result = []
        for idx, value in enumerate(A):
            for value2 in combi(A[idx+1:],k-1):
                result += [[value] + value2]
        return result
    
    my_line = combi(line)
    my_vertex = list(map(vertex,my_line))
    my_dict = dict()
    
    for i in my_vertex:
        if i==True:
            continue
        elif (i[0] % 1 == 0) and (i[1] % 1 == 0):
            a, b = int(i[0]), int(i[1])
            my_dict[str(a)+","+str(b)] = "*"
    
    x_value = [int(i.split(",")[0]) for i in list(my_dict.keys())]
    y_value = [int(i.split(",")[1]) for i in list(my_dict.keys())]
    x_max, x_min = max(x_value), min(x_value)
    y_max, y_min = max(y_value), min(y_value)
    
    answer = []
    for i in range(y_min,y_max+1):
        my_str = ""
        for j in range(x_min,x_max+1):
            loc = ",".join([str(j),str(i)])
            my_str += my_dict.get(loc,".")
        answer.append(my_str)
    return answer[::-1]