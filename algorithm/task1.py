import collections # sol_2
import re # sol_3

class task1:
    # 리스트로 변환
    def sol_1(self, s:str) -> bool:
        strs = []
        for char in s:
            if char.isalnum():
                strs.append(char.lower())
        
        while len(strs) > 1:
            if strs.pop(0) != strs.pop():
                return False
        return True

    # 데크 자료형을 이용한 최적화
    def sol_2(self, s:str) -> bool:
        strs: Deque = collections.deque()

        for char in s:
            if char.isalnum():
                strs.append(char.lower())
        
        while len(strs) > 1:
            if strs.popleft() != strs.pop():
                return False
        return True

    #슬라이싱 사용
    def sol_3(self, s:str) -> bool:
        s = s.lower()
        s = re.sub('[^a-z0-9]', "", s)
        return s == s[::-1]



if __name__ == "__main__":
    str1 = "A man, a plan, a canal: Panama"
    str2 = "race a car"

    sol = task1()
    print(sol.sol_1(str1), sol.sol_1(str2))
    print(sol.sol_2(str1), sol.sol_2(str2))
    print(sol.sol_3(str1), sol.sol_3(str2))