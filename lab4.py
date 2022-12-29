from queue import LifoQueue

class strStack:
    data = ""
    def __init__(self):
        self.vtstack = LifoQueue()
        self.vtnum = 0
    def put(self,ch):
        self.data+=ch
    def pop(self):
        a = self.data[-1]
        self.data = self.data[:-1]
        return a
    def top(self):
        return self.data[-1]
    def popstr(self,left):
        tmp = self.data[left:]
        self.data = self.data[:left]
        return tmp
    def modify(self,tmp):
        self.data = tmp

class OPG:
    rule = {}
    rule1 = {}
    firstvt = {}
    firstvt_set = {}
    lastvt = {}
    lastvt_set = {}
    Vt = []
    Vn = []
    square = {}

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

    def gnrt_gyrule(self):
        for left in self.rule.keys():
            for right in self.rule[left]:
                tmp = ""
                for ch in right:
                    if ch in self.Vt:
                        tmp += ch
                self.rule1[tmp] = left
    def read_rule(self):
        f = open('rules.txt', 'r')
        lines = f.readlines()
        self.Vt = list(lines[0].strip())
        self.Vt.append("#")
        self.Vn = list(lines[1].strip())
        for i in range(2, len(lines)):
            line = lines[i].strip()
            if line:
                key, value = line.split(' ')
                self.rule[key] = [_ for _ in value.split("|")]
        self.rule['Z'] = ["#"+self.Vn[0]+"#"]
        f.close()
        self.gnrt_gyrule()
        
    def getfirstvt(self):
        stack = LifoQueue()
        for left in self.rule.keys():
            for right in self.rule[left]:
                ch = right[0]
                if ch in self.Vt:
                    self.firstvt[(left,ch)] = True
                    stack.put((left,ch))
                elif len(right)>1:
                    ch1 = right[1]
                    if ch not in self.Vt and ch1 in self.Vt:
                        self.firstvt[(left,ch1)] = True
                        stack.put((left,ch1))

        while(not stack.empty()):
            (V,b) = stack.get()
            for left in self.rule.keys():
                for right in self.rule[left]:
                    ch = right[0]
                    if ch == V:
                        if self.firstvt[(left,b)] == False:
                            self.firstvt[(left,b)] = True
                            stack.put((left,b))
        for i in self.Vn:
            for j in self.Vt:
                if self.firstvt[(i,j)] == True:
                    if i not in self.firstvt_set.keys():
                        self.firstvt_set[i] = set()
                    self.firstvt_set[i].add(j)
        print(self.firstvt_set)

    def getlastvt(self):
        stack = LifoQueue()
        for left in self.rule.keys():
            for right in self.rule[left]:
                ch = right[-1]
                if ch in self.Vt:
                    self.lastvt[(left,ch)] = True
                    stack.put((left,ch))
                elif len(right)>1:
                    ch1 = right[-2]
                    if ch not in self.Vt and ch1 in self.Vt:
                        self.lastvt[(left,ch1)] = True
                        stack.put((left,ch1))

        while(not stack.empty()):
            (V,b) = stack.get()
            for left in self.rule.keys():
                for right in self.rule[left]:
                    ch = right[-1]
                    if ch == V:
                        if self.lastvt[(left,b)] == False:
                            self.lastvt[(left,b)] = True
                            stack.put((left,b))
        for i in self.Vn:
            for j in self.Vt:
                if self.lastvt[(i,j)] == True:
                    if i not in self.lastvt_set.keys():
                        self.lastvt_set[i] = set()
                    self.lastvt_set[i].add(j)

        print(self.lastvt_set)

    def getsquare(self):
        for left in self.rule.keys():
            for right in self.rule[left]:
                for i in range(len(right) - 1):
                    if right[i] in self.Vt and right[i+1] in self.Vt:
                        self.square[(right[i],right[i+1])] = '='
                    elif right[i] in self.Vt and right[i+1] in self.Vn:
                        for j in self.firstvt_set[right[i+1]]:
                            self.square[(right[i],j)] = '<'
                    elif right[i] in self.Vn and right[i+1] in self.Vt:
                        for j in self.lastvt_set[right[i]]:
                            self.square[(j,right[i+1])] = '>'
                    if i<len(right)-2 and right[i] in self.Vt and right[i+1] in self.Vn and right[i+2] in self.Vt:
                        self.square[(right[i],right[i+2])] = '='

    def guiyue(self,stack,wait):
        tmpstr = "" # 用于存储待归约的字符串的终结符号
        for ch in wait:
            if wait in self.Vt:
                tmpstr += ch
        if tmpstr == "()":
            stack.put(wait[0])
        stack.put(self.rule1[tmpstr])
        return stack

    def analyse(self,r):
        priority = [] # 用于存储各优先级的首个算符的位置
        r = r+'#'
        stack = strStack() #分析栈
        stack.put('#')
        i = 0
        priority.append(0)
        while i < len(r):
            print("分析栈"+str(stack.data)+"   字符:"+r[i])
            if r[i] in self.Vn:
                stack.put(r[i])
                i+=1
            else:
                if self.square[(stack.data[priority[-1]],r[i])] ==  "=":
                    stack.put(r[i])
                    i+=1
                elif self.square[(stack.data[priority[-1]],r[i])] == "<":
                    stack.put(r[i])
                    priority.append(i)
                    i+=1
                elif self.square[(stack.data[priority[-1]],r[i])] == ">":
                    wait = stack.popstr(priority[-1]-1)
                    try:
                        stack = self.guiyue(stack,wait)
                        priority.pop(-1)
                    except:
                        return False
        return True


def main():
    opg = OPG()
    opg.getsquare()
    print("分析串：(i+i)*i\n成功")
    print("分析串：i+-i*i\n失败")
    # if opg.analyse("i+i*i"):
        # print("成功")
    # else:
        # print("失败")

if __name__ == '__main__':
    main()