#https://programmers.co.kr/learn/courses/30/lessons/42583

def solution(bridge_length, weight, truck_weights):
    time = 0
    bridge = [0] * bridge_length
    
    while len(truck_weights) > 0:
        if sum(bridge[:-1]) + truck_weights[0] <= weight:
            bridge = [truck_weights.pop(0)] + bridge[:-1]
            time += 1
        else:
            bridge = [0] + bridge[:-1]
            time += 1
    return time + bridge_length


def solution2(bridge_length, weight, truck_weights):
    time = 0
    bridge = [0] * bridge_length
    
    while len(truck_weights) > 0:
        end = bridge.pop()
        if sum(bridge) + truck_weights[0] <= weight:
            bridge = [truck_weights.pop(0)] + bridge
            time += 1
        else:
            count = 0
            for i in bridge[::-1]:
                if i == 0:
                    count += 1
                else: break
            bridge = [0] * (count + 1) + bridge[:bridge_length - count - 1]
            time += count+1
    return time + bridge_length


