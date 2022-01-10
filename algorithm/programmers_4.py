#https://programmers.co.kr/learn/courses/30/lessons/42840

def solution(answers):
    A = [1,2,3,4,5]
    B = [2,1,2,3,2,4,2,5]
    C = [3,3,1,1,2,2,4,4,5,5]
    a = sum([1 for i in range(len(answers)) if answers[i] == A[i%5]])
    b = sum([1 for i in range(len(answers)) if answers[i] == B[i%8]])
    c = sum([1 for i in range(len(answers)) if answers[i] == C[i%10]])
    d = max(a,b,c)
    T = [a,b,c]
    answer = []
    for i in range(3):
        if T[i] == d:
            answer.append(i+1)
    return answer