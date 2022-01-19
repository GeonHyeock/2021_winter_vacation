#https://programmers.co.kr/learn/courses/30/lessons/12921#


def solution(n):
    pr = [2]
    for i in range(3,n+1,2):
        for_stop = False
        
        for j in pr:
            if i % j == 0:
                for_stop = True
                break
        if for_stop:
            continue
        pr.append(i)
    return len(pr)