#https://programmers.co.kr/learn/courses/30/lessons/92334

def solution(id_list, report, k):
    my_report = [0] * len(id_list)
    
    #누적 정지 횟수
    A = list(set([(i.split()[0], i.split()[1]) for i in report]))
    for a in A:
        my_report[id_list.index(a[1])] += 1
        
    #정지된 유저.
    B = [id_list[idx] for idx, i in enumerate(my_report) if i >= k]
    
    #결과
    my_result = [0] * len(id_list)
    for a in A:
        if a[1] in B:
            my_result[id_list.index(a[0])] += 1
        
    return my_result