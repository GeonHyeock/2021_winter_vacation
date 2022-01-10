#https://programmers.co.kr/learn/courses/30/lessons/81301

def solution(s):
    my_dict = {
        "zero" : "0",
        "one" : "1",
        "two" : "2",
        "three" : "3",
        "four" : "4",
        "five" : "5",
        "six" : "6",
        "seven" : "7",
        "eight" : "8",
        "nine" : "9"}

    for x in my_dict.keys():
        if x in s:
            s = s.replace(x,my_dict[x])
    answer = int(s)
    return answer

print(solution("one4seveneight"))