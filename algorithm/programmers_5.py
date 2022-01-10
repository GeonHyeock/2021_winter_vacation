#https://programmers.co.kr/learn/courses/30/lessons/12910

def solution(arr, divisor):
    answer = sorted([x for x in arr if x%divisor == 0])
    return answer if len(answer) != 0 else [-1]