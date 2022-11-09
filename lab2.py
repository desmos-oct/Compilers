import re

i = 0

lines = []

with open("rst.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        if line.split()[0] == "wrong":
            lines.remove(line)
        elif line == '\n':
            lines.remove(line)
    print(lines)


def S():
    if i > len(lines) - 1:
        return False
    if V() and matches('equal') and E():
        return True
    # assert()
    return False


def V():
    if i > len(lines) - 1:
        return False
    if matches('identifier'):
        return True
    # assert()
    return False


def E():
    if i > len(lines) - 1:
        return False
    if T() and E2():
        return True
    # assert()
    return False


def E2():
    global i
    preI = i
    if i > len(lines) - 1:
        # print("match eps")
        return True
    if A() and T() and E2():
        return True
    else:
        i = preI
        # print("match eps")
        return True


def T():
    if i > len(lines) - 1:
        return False
    if F() and T2():
        return True
    else:
        # assert()
        return False


def T2():
    global i
    preI = i
    if i > len(lines) - 1:
        # print("match eps")
        return True
    if M() and F() and T2():
        return True
    else:
        i = preI
        # print("match eps")
        return True


def F():
    global i
    preI = i
    if i > len(lines) - 1:
        return False
    if matches('identifier'):
        return True
    i = preI
    if matches('left_paren') and E() and matches("right_paren"):
        return True
    # assert()
    return False


def A():
    global i
    preI = i
    if i > len(lines) - 1:
        return False
    if matches('plus'):
        return True
    i = preI
    if matches('minus'):
        return True
    # assert()
    return False


def M():
    global i
    preI = i
    if i > len(lines) - 1:
        return False
    if matches('times'):
        return True
    i = preI
    if matches('divide'):
        return True
    return False


def matches(str):
    dic = {"identifier": r"(1 .*)","number": r"(3 \d+)","equal": "(10 _)","left_paren": "(11 ()","right_paren": "(11 ))","plus": "(11 +)","minus": "(11 -)","times": "(11 *)","divide": "(11 /)","semicolon": "(11 ;)"}
    rv = False
    global i

    if str in dic.keys():
        if re.search(dic[str], lines[i]):
            # print("match "+str)
            rv = True
    elif str in ['if', 'then', 'else', 'while', 'do', 'begin', 'end']:
        if lines[i] == "(2 " + str + ")\n":
            # print("match "+str)
            rv = True
    i += 1
    return rv


def L():
    global i
    if i > len(lines) - 1:
        return False
    if G():
        preI = i
        while i < len(lines) and matches("semicolon") and G():
            preI = i
            pass
        i = preI
        return True
    return False


def G():
    global i
    preI = i
    if i > len(lines) - 1:
        return False
    if matches("if") and E() and matches("then") and G():
        while i < len(lines) and matches("else") and G():
            preI = i
            pass
        i = preI
        return True
    i = preI
    if matches("while") and E() and matches("do") and G():
        return True
    i = preI
    if matches("begin") and L() and matches("end"):
        return True
    i = preI
    if S():
        return True
    return False


def main():
    rst = G()
    print(rst)


if __name__ == "__main__":
    main()