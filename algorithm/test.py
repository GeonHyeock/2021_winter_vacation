def solution(s):
    a=""
    for i in range(len(s)):
        a += s[i].upper() if i%2 == 0 else s[i].lower()
    return s

print(int(3.7))