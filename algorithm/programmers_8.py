#https://programmers.co.kr/learn/courses/30/lessons/92341

import math
def solution(fees, records):
    
    def money(time_diff): # time_diff : 단위(분)
        if time_diff < fees[0]:
            return fees[1]
        else:
            print(round((time_diff-fees[0])/fees[2]))
            return fees[1] + fees[3] * math.ceil((time_diff-fees[0])/fees[2])

    def change_time(s): # hh:mm 꼴의 str을 단위가 분인 int로 변환
        h = s[:2]
        m = s[3:]
        return int(h) * 60 + int(m)
    
    
    car = [i.split()[1] for i in records] # records : 차량 번호
    car_keys = sorted(list(set(car)))
    
    my_list = []
    for key in car_keys:
        time = [i.split()[0] for i in records if i.split()[1] == key]
        in_out = [i.split()[2] for i in records if i.split()[1] == key]
        my_list.append(list(zip(time,in_out)))
    
    result = []
    for i in my_list:
        if len(i)%2 == 1:
            i.append(["23:59","OUT"])
        use_time = 0
        for j in i:
            if j[1] == "IN":
                in_time = j[0]
            else:
                out_time = j[0]
                time_diff = change_time(out_time) - change_time(in_time)
                use_time += time_diff
        print(use_time)
        result.append(money(use_time))
            
    return result