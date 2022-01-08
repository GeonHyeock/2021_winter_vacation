#https://programmers.co.kr/learn/courses/30/lessons/77484

def solution(lottos, win_nums):
    count = len([x for x in lottos if x in win_nums])
    blank = lottos.count(0)
    f = lambda x : 6 if x==7 else x
    
    max = f(7 - count - blank)
    min = f(7 - count)
    answer = [max, min]
    return answer



if __name__ == "__main__":
    lottos = [0, 0, 0, 0, 0, 0]
    win_nums = [44, 1, 2, 3, 31, 25]
    print(solution(lottos, win_nums))