rule = {} # 读入的规则
first = {} # first集,元组，无重复，
follow = {} # follow集
Vn = set()# 非终结符号集
Vt = set() # 终结符号集
analist = {} # 分析表


# 读入文法
def read_rule():
    global rule
    global Vt, Vn
    f = open('rules1.txt', 'r')
    lines = f.readlines()
    Vt = set(lines[0].strip())
    Vn = set(lines[1].strip())
    for i in range(2, len(lines)):
        line = lines[i].strip()
        if line:
            key, value = line.split(' ')
            rule[key] = [_ for _ in value.split("|")]
    f.close()


# 产生单个first集
import copy
def first_set():
    global first
    global rule,Vn,Vt
    lastfirst = {}

    for ch in Vt:
        first[ch] = set(ch)
    for ch in Vn:
        first[ch] = set()

    for left in rule.keys():
        for right in rule[left]:
            if not right[0].isupper():
                first[left] = first[left].union(right[0])

    while lastfirst != first:
        lastfirst = copy.deepcopy(first)
        for left in rule.keys():
            for right in rule[left]:
                if right[0] in Vn:
                    tmp = copy.deepcopy(get_first(right[0]))
                    if "$" in tmp:
                        tmp.remove("$")
                    first[left] = first[left].union(tmp)
                i = 0
                while i < len(right) - 1 and "$" in first[right[i]]:
                    tmp = copy.deepcopy(first[right[i + 1]])
                    if "$" in tmp:
                        tmp.remove("$")
                    first[left] = first[left].union(tmp)
                    i += 1
                if right[i] != "$" and "$" in first[right[i]]:
                    first[left] = first[left].union("$")

#获取字符串的first集
def get_first(item):
    global first
    rt = set()
    rt = rt.union(first[item[0]])
    if "$" in rt:
        rt.remove("$")
    i=0
    for i in range(len(item)- 1):
        if "$" in first[item[i]]:
            rt = rt.union(first[item[i + 1]])
        else:
            break
    if i == len(item) - 1 and "$" in first[item[i]]:
        rt = rt.union("$")
    return rt

#产生follow集
def follow_set():
    global first,rule,follow
    lastfollow = {}

    for ch in Vn:
        follow[ch] = set()

    #print(rule.keys())
    follow["S"]=set("#")

    for left in rule.keys():
        for right in rule[left]:
            for i in range(0, len(right) - 1):
                if not right[i].isupper():
                    continue
                tmp = copy.deepcopy(get_first(right[i + 1:]))
                if "$" in tmp:
                    tmp.remove("$")
                follow[right[i]] = follow[right[i]].union(tmp)

    while lastfollow != follow:
        lastfollow = follow
        for left in rule.keys():
            for right in rule[left]:
                if right[-1] in Vn:
                    follow[right[-1]] = follow[right[-1]].union(follow[left])
                for i in range(2,len(right)+1):
                    if not right[-i] in Vn:
                        continue
                    elif "$" in get_first(right[-i + 1:]):
                        follow[right[-i]] = follow[right[-i]].union(follow[left])
        # print(follow)


# 产生分析表
def generateAnalist():
    for left in rule.keys():
        for right in rule[left]:
            for tmp in get_first(right):
                analist[(left,tmp)] = (left,right)
            if '$' in get_first(right):
                for tmp in follow[left]:
                    if not tmp.isupper():
                        analist[(left,tmp)] = (left,"$")


#分析过程
from queue import Queue,LifoQueue
def analyze(inst):
    stack = LifoQueue() # 分析栈
    stack.put('#')
    stack.put('S')
    des = Queue() # 输入串
    for ch in inst:
        des.put(ch)
    des.put("#")
    while not stack.empty() and not des.empty():
        print("分析栈：",end="")
        print(stack.queue,end="")
        print("输入串：",end="")
        print(des.queue)
        try:
            top = stack.get()
            if top.isupper():
                _,tmp = analist[(top,des[0])]    
                for i in len(tmp):
                    stack.put(tmp[-i-1])
            elif top == '#':
                if des.get() == '#':
                    return True    
                else:
                    assert()
            else:
                if top == des.get():
                    continue
                else:
                    assert()
        except:
            print("error")
            break


def main():
    read_rule()
    # print(rule)
    # print(Vn)
    # print(Vt)

    first_set()
    #print(first)
    follow_set()
    #print(follow)
    generateAnalist()
    #print(analist)
if __name__ == '__main__':
    main()