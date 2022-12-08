from queue import LifoQueue

class strStack:
    def __init__(self):
        self.data = ""
        self.vtstack = LifoQueue()
        self.vtnum = 0
    def push(self,ch):
        self.data+=ch
    def pop(self):
        a = self.data[-1]
        self.data = self.data[:-1]
        return a
    def top(self):
        return self.data[-1]
    def popstr(self,left,right):
        tmp = self.data[left:right]
        return tmp
    def modify(self,tmp):
        self.data = tmp

class OPG:
    rule = {}
    firstvt = {}
    firstvt_set = {}
    lastvt = {}
    Vt = []
    Vn = []

    def __init__(self):
        self.read_rule()
        for i in self.Vt:
            for j in self.Vn:
                self.firstvt[(j,i)] = False
        self.getfirstvt()
        for i in self.Vt:
            for j in self.Vn:
                self.lastvt[(j,i)] = False
        self.getlastvt()

    def read_rule(self):
        f = open("rule.txt")
        line1 = f.readline()
        line2 = f.readline()
        for i in line1:
            self.Vt.append(i)
        for i in line2:
            self.Vn.append(i)
        lines = f.readlines()
        for i in range(2,len(lines)):
            tmpstr="" # 用于存储产生式右部的终结符号
            tmplist = [] # 用于存储产生式右部的非终结符号
            tmp1 = lines[i].split("->")[0] #用于存储产生式左符号
            secondlist = lines[i].split("->")[1] #用于存储产生式右部
            for tmp2 in secondlist:
                for ch in tmp2:
                    if ch in self.Vt:
                        tmpstr += ch
                tmplist.append(tmpstr)
            self.rule[tmp1] = tmplist
        
    def getfirstvt(self):
        stack = LifoQueue()
        for left in self.rule.keys():
            for right in self.rule[left]:
                for ch in right:
                    if ch in self.Vt:
                        self.firstvt[(left,ch)] = True
                        stack.put((left,ch))
                        break

        while(stack.empty()):
            (V,b) = stack.get()
            for left in self.rule.keys():
                for right in self.rule[left]:
                    for ch in right:
                        if ch == V:
                            if self.firstvt[(left,b)] == False:
                                self.firstvt[(left,b)] = True
                                stack.put((left,b))
        for i in self.Vn:
            for j in self.Vt:
                if self.firstvt[(i,j)] == True:
                    self.firstvt_set[i].add(j)
    def getlastvt(self):
        stack = LifoQueue()

    def getsquare(self):
        for left in self.rule.keys():
            for right in self.rule[left]:
                for i in range(len(right) - 1):
                    if right[i] in self.Vt and right[i+1] in self.Vt:
                        self.square[(right[i],right[i+1])] = '='
                    elif i<len(right)-1 and right[i] in self.Vt and right[i+1] in self.Vn and right[i+2] in self.Vt:
                        self.square[(right[i],right[i+2])] = '='
                    elif right[i] in self.Vt and right[i+1] in self.Vn:
                        for j in self.firstvt_set[right[i+1]]:
                            self.square[(right[i],j)] = '<'
                    elif right[i] in self.Vn and right[i+1] in self.Vt:
                        for j in self.lastvt_set[right[i]]:
                            self.square[(j,right[i+1])] = '>'

    def guiyue(self,stack,wait):
        tmpstr = "" # 用于存储待归约的字符串的终结符号
        for ch in wait:
            if wait in self.Vt:
                tmpstr += ch
        stack.put(self.rule[tmpstr])

    def analyse(self,r):
        priority = []
        r = r+'#'
        stack = strStack()
        stack.put('#')
        i = 0
        priority.append(0)
        j = 0
        while i < len(r):
            if r[i] in self.Vn:
                stack.put(r[i])
            else:
                if self.square[(stack.top(),r[i])] ==  "=":
                    stack.put(r[i])
                elif self.square[(stack.top(),r[i])] == "<":
                    stack.put(r[i])
                    priority.append(j)
                elif self.square[(stack.top(),r[i])] == ">":
                    wait = stack.popstr(priority[-1]-1,j)
                    self.guiyue(wait,wait)
            if self.square[(stack.top(),r[i])] != ">":
                j += 1
                i += 1
        return True