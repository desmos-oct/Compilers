rule = {}
first = {}
follow = {}

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
                while i < len(right) and "$" in get_first(right[i]) and right[i].isupper():
                    first[left].append("$")
                    tmp = get_first(right[i+1])
                    first[left] = first[left].union(tmp)

def get_first(item):
    if len(item) == 1:
        return first[item]
    else:
        if not "$" in first[item[0]]:
            return first[item[0]]
        else:
            rt = first[item[0]]
            return rt.union(get_first(item[1:0]))

def follow_set():
    global first
    global rule
    global follow
    lastfollow = {}
    follow[rule.keys[0]] = {'#'}