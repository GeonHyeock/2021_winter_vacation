#https://programmers.co.kr/learn/courses/30/lessons/72411
def solution(orders, course):
    
    def my_count(s,A):
        count = 0
        s = set([value for value in s])
        A = [set([value for value in a]) for a in A]
        for a in A:
            if s & a == s : count += 1
        return count
    
    def my_combi(A,n):
        if n==0: return [[]]
        result = []
        for idx,value in enumerate(A):
            for value2 in my_combi(A[idx+1:],n-1):
                result += [[value] + value2]
        return result
    orders = [sorted(value) for value in orders]
    
    result = []
    for num in course:
        my_menu = []
        for menu in orders:
            my_menu += ["".join(value) for value in my_combi(menu,num)]
        my_menu = list(set(my_menu))
        
        best_menu,best_count = [],1
        for menu in my_menu:
            count = my_count(menu,orders)
        
            if count > best_count:
                best_count = count
                best_menu = [menu]
            elif count == max(2,best_count):
                best_menu.append(menu)
        result += best_menu
        
    
    return sorted(result)