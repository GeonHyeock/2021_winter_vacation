#https://programmers.co.kr/learn/courses/30/lessons/12977

def solution(nums):
    def isprime(n : int) -> bool:
        k = 2
        while k <= n ** 1/2:
            if n % k == 0:
                return False
            k += 1
        return True

    def combi(n : list[int], r : int = 3):
        for i in range(len(n)):
            if r == 1:
                yield [n[i]]
            else:
                for next in combi(n[i+1:], r-1):
                    yield [n[i]] + next
    
    num_list = list(map(sum,list(combi(nums))))
    num_bool = list(map(isprime,num_list))
    return sum(num_bool)

