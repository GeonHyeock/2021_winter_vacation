#https://programmers.co.kr/learn/courses/30/lessons/67257

def solution(expression):
    def my_cal(A, oper):
        if oper == "*":
            answer = 1
            for i in A: answer *= float(i)
        if oper == "+":
            answer = 0
            for i in A: answer += float(i)
        if oper == "-":
            answer = float(A[0])
            for i in A[1:]: answer -= float(i)
        return answer
    
    def per(A, k = 3):
        result = []
        if k == 0:
            return [[]]

        for idx, value in enumerate(A):
            B = A[:idx] + A[idx+1:]
            for value2 in per(B, k-1):
                result += [[value] + value2]
        return result

    result = 0
    my_op = per(["*","-","+"])
    for oper in my_op:
        my_ex = expression.split(oper[0])
        my_ex = [express.split(oper[1]) for express in my_ex]
        
        for idx1, i in enumerate(my_ex):
            for idx2,j in enumerate(i):
                if oper[2] in j:
                    my_ex[idx1][idx2] = my_cal(j.split(oper[2]),oper[2])
            my_ex[idx1] = my_cal(i,oper[1])
        answer = my_cal(my_ex,oper[0]) if my_cal(my_ex,oper[0])>0 else -my_cal(my_ex,oper[0])
        
        if answer > result:
            result = answer
        
    return result