dic = {0: 1, 1: 1, 2: 2, 3: 2, 4: 5, 5: 5}


def readD(str, int):
    if len(str) == 1:
        return 0
    else:
        return dic[int]


def judger(str, int):
    if int == 0:
        if str[0].isdigit():
            return readD(str, int)
        elif str[0] == '.':
            return 3
    elif int == 1:
        if str[0].isdigit():
            return readD(str, int)
        elif str[0] == '.':
            return 2
        elif str[0] == 'E' or str[0] == 'e':
            return 4
    elif int == 2:
        if str[0].isdigit():
            return readD(str, int)
        elif str[0] == 'e' or str[0] == 'E':
            return 4
    elif int == 3:
        if str[0].isdigit():
            return readD(str, int)
    elif int == 4:
        if str[0].isdigit():
            return readD(str, int)
        elif str[0] == '+' or str[0]=='-':
            return 5
    elif int == 5:
        if str[0].isdigit():
            return readD(str, int)
    else:
        return -1


def main():
    while 1:
        try:
            str = input()
        except:
            break
        i = 0
        status = 0
        while i <= len(str):
            if i == len(str):
                print("error")
                break
            status = judger(str[i:], status)
            if status == -1:
                print("error")
                break
            elif status == 0:
                print("success")
                break
            else:
                i += 1
        

if __name__ == "__main__":
    main()