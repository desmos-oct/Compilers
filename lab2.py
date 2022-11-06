import re

def S():
    V()
    if matches('equal'):
        E()
    return True

def V():
    if matches('identifier'):
        return True
    return False

def E():
    T()
    E2()

def E2():
    A()
    T()
    E2()

def T():
    F()
    T2()

def T2():
    M()
    F()
    T2()

def F():
    if matches('identifier'):
        return True
    elif matches('left_paren'):
        E()
        if matches('right_paren'):
            return True
    return False

def A():
    if matches('plus'):
        return True
    elif matches('minus'):
        return True
    return False

def M():
    if matches('times'):
        return True
    elif matches('divide'):
        return True
    return False

def matches(str):
    with open("rst.txt","r") as f:
        if str == 'identifier':
            if f.readline()[1:3]=="1 ":
                return True
            else:
                return False
        elif str == 'number':
            if f.readline()[1:3]=="3 ":
                return True
            else:
                return False
        elif str == 'equal':
            if f.readline()[1:3]=="10":
                return True
            else:
                return False
        elif str == 'left_paren':
            if f.readline()=="(11 ()":
                return True
            else:
                return False
        elif str == 'right_paren':
            if f.readline()=="(11 ))":
                return True
            else:
                return False
        elif str == 'plus':
            if f.readline()=="(11 +)":
                return True
            else:
                return False
        elif str == 'minus':
            if f.readline()=="(11 -)":
                return True
            else:
                return False
        elif str == 'times':
            if f.readline()=="(11 *)":
                return True
            else:
                return False
        elif str == 'divide':
            if f.readline()=="(11 /)":
                return True
            else:
                return False

def main():
    S()