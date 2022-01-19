#괄호 검사

ex1 = "({})"
ex2 = "({)}"

def sol(s):
    my_match = {"(" : ")", "{" : "}"}
    open_str = my_match.keys()
    my_stack = []

    for i in s:
        if i in open_str:
            my_stack.append(i)
        else:
            if my_match[my_stack.pop()] != i:
                return -1
    return 1

print("ex1의 결과입니다. : ",sol(ex1)) 
print("ex2의 결과입니다. : ",sol(ex2))
