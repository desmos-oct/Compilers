rule = {}
first = {}
follow = {}
Vn = []
Vt = []
analist = {}

def read_rule():
    global rule
    f = open('rule.txt', 'r')
    for line in f:
        line = line.strip()
        if line:
            key, value = line.split(' ')
            rule[key] = [_ for _ in value.split("|")]
    f.close()


def first_set():
    global first
    global rule
    lastfirst = {}

    for left in rule.keys():
        for right in rule[left]:
            if not right[0].isupper():
                first[right[0]] = {}.append(right[0])
            else:
                first[right[0]] = {}
    for left in rule.keys():
        for right in rule[left]:
            if not right[0].isupper():
                first[left] = first[left].union(get_first(right[0]))

    while lastfirst != first:
        lastfirst = first
        for left in rule.keys():
            for right in rule[left]:
                if right[0].isupper():
                    tmp = get_first(right)
                    tmp.remove("$")
                    first[left] = first[left].union(tmp)
                i = 0
                while i < len(right) and "$" in get_first(
                        right[i]) and right[i].isupper():
                    first[left].append("$")
                    tmp = get_first(right[i + 1])
                    first[left] = first[left].union(tmp)
                    i += 1


def get_first(item):
    if len(item) == 1:
        return first[item]
    else:
        if not "$" in first[item[0]]:
            return first[item[0]]
        else:
            rt = first[item[0]]
            return rt.union(get_first(item[1:]))


def follow_set():
    global first
    global rule
    global follow
    lastfollow = {}
    follow[rule.keys[0]] = {'#'}

    for left in rule.keys():
        for right in rule[left]:
            if not right[i].isupper():
                i += 1
                continue
            for i in range(0, len(right) - 1):
                tmp = get_first(right[i + 1])
                tmp.remove("$")
                follow[right[i]] = follow[right[i]].union(tmp)
                i += 1

    while lastfollow != follow:
        for left in rule.keys():
            for right in rule[left]:
                if right[-1].isupper():
                    follow[right[-1]] = follow[right[-1]].union(follow[left])
                if "$" in get_first(right[-1]):
                    i = 2
                    while i <= len(right) and "$" in get_first(
                            right[-i + 1:]) and right[i].isupper():
                        i += 1
                        follow[-i] = follow[-i].union(follow[left])

def generateAnalist():
    for left in rule.keys():
        for right in rule[left]:
            for tmp in get_first(right):
                analist.append((left, tmp),(left,right))
            if '$' in get_first(right):
                for tmp in follow[left]:
                    if not tmp.isupper():
                        analist.append((left, tmp),(left,'$'))

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