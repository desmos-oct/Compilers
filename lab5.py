import re

class PROJECT:
    type = 'normal'
    def __init__(self,left,right,place):
        self.left = left
        self.right = right
        self.place = place
        if self.place == len(self.right):
            self.type = 'reduce' #归约
        else:
            self.type = 'shift' #移进

    def copy(self,place):
        return PROJECT(self.left,self.right,place)

    def __repr__(self):
        return  (self.left+self.right+str(self.place))

    def __eq__(self,other):
        if self.left == other.left and self.right == other.right and self.place == other.place:
            return True
        else:
            return False

class STATUS:
    def __init__(self):
        self.projects = []

    def append(self,project):
        self.projects.append(project)
    
    @classmethod
    def createByList(self,projects):
        status = STATUS()
        for item in projects:
            status.append(item)
        return status
    
    def print(self):
        for item in self.projects:
            item.print()
    
    def __contains__(self,project):
        for item in self.projects:
            if item == project:
                return True
        return False

    def __len__(self):
        return len(self.projects)

    def __eq__(self, __o: object) -> bool:
        if len(self.projects) != len(__o.projects):
            return False
        for item1 in self.projects:
            flag = False
            for item2 in __o.projects:
                if item1 == item2:
                    flag = True
                    break
            if flag == False:
                return False
        return True

class SYMBOL:
    def __init__(self, name, source):
        self.name = name
        self.source = source
        
anastr = []
rule = {} #{'s':['i','V+E']...}
ruleByIndex = []
gotoList = {} #{(0,'V'):1,(0,'E'):2,(1,'V'):-1...)} -1表示归约
Vn = []
Vt = []
first = {}
follow = {}

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
    follow[Vn[0]]=set("#")

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


def readrule():
    global Vn,Vt,rule,ruleByIndex
    with open("rules.txt", 'r') as f:
        lines = f.readlines()
        for index,line in enumerate(lines):
            if index == 0:
                Vt = list(line.strip())
            elif index == 1:
                Vn = list(line.strip())
            else:
                left = line.strip().split(' ')[0]
                right = line.strip().split(' ')[1].split('|')
                rule[left] = right
                ruleByIndex += [(left, item) for item in right]


def readdst():
    global anastr
    with open("rst.txt", "r") as f:
        pattern = re.compile(r"\((\d+) (.*)\)")
        for line in f.readlines():
            data = pattern.search(line).groups()
            if data[0] == '1':
                anastr.append(SYMBOL('i', data[1]))
            elif data[0] == '10':
                anastr.append(SYMBOL('=','='))
            else:
                anastr.append(SYMBOL(data[1], data[1]))

    anastr.append(SYMBOL('#', '#'))


def closure(projList):
    added = [] #已经加入的所有初始项目
    rst = []
    rst += projList

    #初始化added
    for item in rst:
        if item.place == 0 and item.left not in added:
            added.append(item.left)

    for item in rst:
        if item.type == 'reduce':
            continue

        #若X是终结符号就不做任何操作
        X = item.right[item.place]
        if X not in Vn:
            continue

        #检查所有项目
        if item.right[item.place] not in added:
            added.append(item.right[item.place])
            tmp = [PROJECT(X,i,0) for i in rule[X]]
            rst += tmp
            
    if rst == projList:
        return rst
    else:
        return closure(rst)


def contains(statusSet, status):
    for item in statusSet:
        if item == status:
            return True
    return False


statusNum = 0
def goto():
    global gotoList,statusNum,follow
    # 初始化状态
    StatusSet = []
    StatusSet.append(STATUS())

    StatusSet[0].append(PROJECT('$',Vn[0],0))

    StatusSet[0] = STATUS.createByList(closure(StatusSet[0].projects))

    #对每一个状态进行操作
    tmp = 1
    for index,pstStatus in enumerate(StatusSet):
        for projIndex,proj in enumerate(pstStatus.projects):
            if proj.type != 'reduce' and (index,proj.right[proj.place]) not in gotoList.keys():
                tSSet = [] #临时项目集合
                tSSet.append(proj.copy(proj.place+1))
                for tmp_index in range(projIndex+1,len(pstStatus)):
                    othProject = pstStatus.projects[tmp_index]
                    if proj.type != 'reduce' and othProject.right[othProject.place] == proj.right[proj.place]:
                        tSSet.append(othProject.copy(othProject.place+1))

                tmpStatus = STATUS.createByList(closure(tSSet))

                if not contains(StatusSet,tmpStatus):
                    StatusSet.append(tmpStatus)
                    #修改goto表
                    if (index,proj.right[proj.place]) not in gotoList.keys():
                        gotoList[(index,proj.right[proj.place])] = tmp
                        #print("({},{}):{}".format(index,proj.right[proj.place],tmp))
                    else:
                        assert()
                    tmp += 1
                else:
                    if (index,proj.right[proj.place]) not in gotoList.keys():
                        gotoList[(index,proj.right[proj.place])] = StatusSet.index(tmpStatus)
                        #print("({},{}):{}".format(index,proj.right[proj.place],StatusSet.index(tmpStatus)))
                    else:
                        assert()
            elif proj.type == 'reduce':
                if proj.right == 'S':
                    continue
                status = ruleByIndex.index((proj.left,proj.right))
                for followch in follow[proj.left]:
                    if (index,followch) not in gotoList.keys():
                        gotoList[(index,followch)] = -status-1
                    else:
                        assert()
    statusNum = len(StatusSet)
    gotoList[1,'#'] = 100
                    

import pandas as pd
import numpy as np

def createSLRTable():
    table = pd.DataFrame(columns=Vn+Vt,index=range(statusNum))

    for item in gotoList.keys():
        table.loc[item[0],item[1]] = gotoList[item]

    table.to_csv("AutoSLRTable.csv")


tVariableIndex = 0

f = open("quarternion.txt",'w')
def meaningAction(symbolList):
    global tVariableIndex
    if len(symbolList) == 1:
        return symbolList[0].source
    elif symbolList[1].name == '=':
        f.write("(=,{},_,{})\n".format(symbolList[2].source,symbolList[0].source))
        return ''
    elif symbolList[0].name == '(':
        return symbolList[1].source
    elif len(symbolList) == 3:
        f.write("({},{},{},{})\n".format(symbolList[1].source,symbolList[0].source,symbolList[2].source,'T'+str(tVariableIndex)))
        tVariableIndex += 1
        return 'T'+str(tVariableIndex-1)
            
            
def analyzeBySLRList():
    global anastr
    SLRList = pd.read_csv('AutoSLRTable.csv',index_col=0)

    statusStack = []
    symbolStack = []

    statusStack.append(0)
    symbolStack.append(SYMBOL('#','#'))

    while True:
        inputSymbol = anastr[0]
        pstStatus = statusStack[-1] 

        action = SLRList.loc[pstStatus,inputSymbol.name]

        if action == 100:
            print('accept')
            break
        elif np.isnan(action):
            print('unaccept')
            break
        elif action > 0:
            action = int(action)
            statusStack.append(action)
            symbolStack.append(inputSymbol)
            anastr.pop(0)
        elif action < 0:
            action = int(action)
            print('reduce',ruleByIndex[-action-1][0],'<-',ruleByIndex[-action-1][1])
            lenth = len(ruleByIndex[-action-1][1])
            statusStack = statusStack[:-lenth]
            subSymbol = symbolStack[-lenth:]
            symbolStack = symbolStack[:-lenth]

            newSrc = meaningAction(subSymbol)
            newSymble = SYMBOL(ruleByIndex[-action-1][0],newSrc)
            symbolStack.append(newSymble)
            newStatus = SLRList.loc[statusStack[-1],symbolStack[-1].name]
            if newStatus == 100:
                print('\naccept')
                break

            statusStack.append(newStatus)
        else:
            print('error')
            break

def main():
    readrule()
    readdst()
    first_set()
    follow_set()
    for item in anastr:
        print(item.source,end='')
    print()
    goto()
    createSLRTable()
    try:
        analyzeBySLRList()
    except:
        print("error")
    f.close()

if __name__ == '__main__':
    main()