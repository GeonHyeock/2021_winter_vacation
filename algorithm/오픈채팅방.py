#https://programmers.co.kr/learn/courses/30/lessons/42888
def solution(record):
    def my_change(A):
        if A[0] == "Enter":
            return A[1]+"님이 들어왔습니다."
        elif A[0] == "Leave":
            return A[1]+"님이 나갔습니다."
    
    my_dict = dict()
    for i in record:
        my_list = i.split()
        if len(my_list) == 3:
            my_dict[my_list[1]] = my_list[2]
    
    record_state_user = [(i.split()[0],my_dict[i.split()[1]]) for i in record 
                         if i.split()[0] in ("Enter","Leave")]
    
    return record