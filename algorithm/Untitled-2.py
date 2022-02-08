#https://programmers.co.kr/learn/courses/30/lessons/67256

def solution(numbers, hand):
    
    def grid(num):
        if num == 0:
            return 2,4
        elif num % 3 == 0:
            return 3,num//3
        else: return num%3,num//3+1
    
    def L2_sqr(a,b): return (a[0]-b[0])**2 + (a[1]-b[1])**2
    
    L =1,4; R = 3,4
    answer = ''
    sol = ["R","L"]
    
    for i in numbers:
        if i == 0 or i%3 == 2:
            if L2_sqr(grid(i),L) > L2_sqr(grid(i),R):
                answer += "R"
                R = grid(i)
            elif L2_sqr(grid(i),L) < L2_sqr(grid(i),R):
                answer += "L"
                L = grid(i)
            else:
                if hand == "right":
                    answer += "R"
                    R = grid(i)
                else:
                    answer += "L"
                    L = grid(i)
        else:
            answer += sol[i % 3]
            if i % 3 == 1:
                L = grid(i)
            else:
                R = grid(i)
    return answer