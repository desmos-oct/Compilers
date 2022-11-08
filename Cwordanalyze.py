import re
reserve = ["include","void","int","float","double","if","else","for","do","while"]
dic = {'indentifier':'1','reserve':'2','number':'3','<>':'4','<=':'5','>=':'6','<':'7','>':'8','==':'9','=':'10','single':'11'}

rst = open("rst.txt",'w')

def indetifier(word):
    if not word in reserve:
        rst.write("({} {})\n".format(dic['indentifier'],word))
    else:
        rst.write("({} {})\n".format(dic['reserve'],word))

def number(word):
    rst.write("({} {})\n".format(dic['number'],word))

def lt(next):
    if next == '>':
        rst.write("({} _)\n".format(dic['<>']))
        return 1
    elif next == '=':
        rst.write("({} _)\n".format(dic['<=']))
        return 0
    else:
        rst.write("({} _)\n".format(dic['<']))
        return 0

def gt(next):
    if next == '=':
        rst.write("({} _)\n".format(dic['>=']))
        return 1
    else:
        rst.write("({} _)\n".format(dic['>']))
        return 0

def eq(next):
    if next == '=':
        rst.write("({} _)\n".format(dic['==']))
        return 1
    else:
        rst.write("({} _)\n".format(dic['=']))
        return 0

def symbol(word,next):
    if word in ['+','-','*',';','(',')']:
        rst.write("({} {})\n".format(dic['single'],word))
        return 0
    elif word == '<':
        return lt(next)
    elif word == '>':
        return gt(next)
    elif word == '=':
        return eq(next)
    return 0

program = ''
# 预处理
with open("source.c","r") as f:
    lines = f.readlines()
    #去//注释
    for line in lines:
        program+=re.sub(r"//.*?\n",'',line)
    #去/* */注释
    program = re.sub(r"/\*.*\*/",'',program)
    program = re.sub("/\\*[\\s\\S]*\\*/",'',program)

#检测
i = 0
row = 0
last = 0
while i < len(program):
    if program[i].isalpha():
        tmp=i
        while i<len(program) and program[i].isalnum():
            i+=1
        indetifier(program[tmp:i])
    elif program.isdigit():
        tmp=i
        while i<len(program) and program[i].isdigit():
            i+=1
        number(program[tmp:i])
    elif program[i] in ['+','-','*',';','(',')','<','>','=']:
        if i+1<len(program):
            i=symbol(program[i],program[i+1])+i+1
        else:
            rst.write("({} {})\n".format(dic['single'],program[i]))
            i+=1
    elif program[i] in [' ','\t','\n']:
        if program[i]=='\n':
            row+=1
            last = i
        i+=1
    else:
        rst.write("wrong character in row"+str(row+1)+':'+str(i-last)+'\n')
        i+=1

rst.close()