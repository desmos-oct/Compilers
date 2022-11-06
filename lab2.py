import re

i = 0

lines = []

with open("rst.txt","r") as f:
    lines = f.readlines()
    for line in lines:
        if line.split()[0]=="wrong":
            lines.remove(line)

def S():
    if V() and matches('equal') and E():
        return True
    return False

def V():
    if matches('identifier'):
        return True
    return False

def E():
    if T() and E2():
        return True

def E2():
    preI = i
    if A() and T() and E():
        return True
    else:
        i = preI
        return True

def T():
    if F() and T2():
        return True
    else:
        return False

def T2():
    preI = i
    if M() and F() and T2():
        return True
    else:
        i = preI
        return True

def F():
    preI = i
    if matches('identifier'):
        return True
    i = preI
    if matches('left_paren') and E() and matches("right_paren"):
        return True
    return False

def A():
    preI = i
    if matches('plus'):
        return True
    i = preI
    if matches('minus'):
        return True
    return False

def M():
    preI = i
    if matches('times'):
        return True
    i = preI
    if matches('divide'):
        return True
    return False

def matches(str):
    rv = False
    if str == 'identifier':
        if lines[i][1:3] == "1 ":
            rv = True
    elif str == 'number':
        if lines[i][1:3] == "3 ":
            rv = True
    elif str == 'equal':
        if lines[i][1:3] == "10":
            rv = True
    elif str == 'left_paren':
        if lines[i] == "(11 ()":
            rv = True
    elif str == 'right_paren':
        if lines[i] == "(11 ))":
            rv = True
    elif str == 'plus':
        if lines[i] == "(11 +)":
            rv = True
    elif str == 'minus':
        if lines[i]=="(11 -)":
            rv =  True
    elif str == 'times':
        if lines[i]=="(11 *)":
            rv =  True
    elif str == 'divide':
        if lines[i]=="(11 /)":
            rv =  True
    i += 1
    return rv

def main():
    rst = S()
    print(rst)