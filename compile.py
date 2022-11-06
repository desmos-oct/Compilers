while 1:
    try:
        str=input()
    except:
        break
    list = []

    maohao = str.find(":")
    point = str.rfind(".")
    if maohao!= -1 and point!=-1:
        list.append(str[:maohao])
        list.append(str[maohao+1:point])
        list.append(str[point+1:])
    elif maohao==-1 and point!=-1:
        list.append(str[:point])
        list.append(str[point+1:])
    elif maohao!=-1 and point==-1:
        list.append(str[:maohao])
        list.append(str[maohao+1:])
    else:
        list.append(str)
    flag=1
    print(list)
    for i in list:
        if not i.isalpha():
            print("error")
            flag=0
            break
    if flag:
        print("matched")