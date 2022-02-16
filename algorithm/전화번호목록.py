#https://programmers.co.kr/learn/courses/30/lessons/42577
def solution(phone_book):
    max_iter = max(map(len,phone_book))
    for i in range(1,max_iter):
        A = [phone[:i] for phone in phone_book if len(phone) > i ]
        B = [phone for phone in phone_book if len(phone) == i ]
        if bool(set(B) & set(A)):
            return False
    return True