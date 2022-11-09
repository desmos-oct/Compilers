i = 0

lines = []

with open("rst.txt","r") as f:
    lines = f.readlines()
    for line in lines:
        if line.split()[0]=="wrong":
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
    rv = False
    global i
    if str == 'identifier':
        if lines[i][1:3] == "1 ":
            # print("match identifier")
            rv = True
    elif str == 'number':
        if lines[i][1:3] == "3 ":
            # print("match number")
            rv = True
    elif str == 'equal':
        if lines[i][1:3] == "10":
            # print("match equal")
            rv = True
    elif str == 'left_paren':
        if lines[i] == "(11 ()\n":
            # print("match lp")
            rv = True
    elif str == 'right_paren':
        if lines[i] == "(11 ))\n":
            # print("match rp")
            rv = True
    elif str == 'plus':
        if lines[i] == "(11 +)\n":
            # print("match plus")
            rv = True
    elif str == 'minus':
        if lines[i]=="(11 -)\n":
            # print("match minus")
            rv = True
    elif str == 'times':
        if lines[i]=="(11 *)\n":
            # print("match times")
            rv = True
    elif str == 'divide':
        if lines[i]=="(11 /)\n":
            # print("match divide")
            rv = True
    elif str == 'semicolon':
        if lines[i]=="(11 ;)\n":
            # print("match semicolon")
            rv = True
    elif str in ['if','then','else','while','do','begin','end']:
        if lines[i] == "(2 "+str+")\n":
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