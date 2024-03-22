from 词法分析器 import get_data
end_of_row, Word = get_data()
signal_stack = {'name':[],'type':[],'value':[],'address':[],'ad':0,'level':0}

# 记录函数的参数，解决调用参数不匹配的问题
# 栈符号表,previous用来标记每个模块的结束位置（0）
# address对于proc来说，记录的是其在P代码中的代码标号（理论上可行
# ad可以看作一个全局变量，它记录某个变量在当前模块中关于基地址的偏移量
# level记录的是var和proc所在的层次
# level在每次出现函数名定义时就+1
display = []  # 符号display表，用来记录模块在栈符号表中的起始位置
p_code={'F':[],'L':[],'A':[]}  # 存储生成的中间代码
def find_mistake(indicator):  # 返回错误的位置
    indicator-=1
    indicator = Word[indicator]-len(word[indicator])+1 # 得到开始位置
    row = 0
    for i in range(len(end_of_row)):
        if (indicator >= end_of_row[i]):
            row += 1
        else:
            break
    col = indicator - end_of_row[row - 1]
    return row, col
def enter(name,type,value):
    signal_stack['name'].append(name)
    signal_stack['type'].append(type)
    signal_stack['value'].append(value)
    if type=='var': # 仅仅针对var，因为var要写入活动记录
        signal_stack['address'].append(signal_stack['ad'])
        signal_stack['ad']+=1
    else:
        signal_stack['address'].append('')
    return 0
def Pop():  # 在过程结束后，即body结束后，需要将对应内容从栈符号表中吐出来
    start=display[-1]  #display记录的最新内容，即为这个模块的起始位置编号
    end=len(signal_stack['name'])
    # display.pop(-1)
    for i in range(start,end):
        signal_stack['name'].pop()
        signal_stack['type'].pop()
        signal_stack['value'].pop()
        signal_stack['address'].pop()
    display.pop()
    return 0
def find_name(name):  #检查使用的变量名是否在栈符号表中定义
    for i in range(len(signal_stack['name'])-1,-1,-1):
        if signal_stack['name'][i]==name:
            return i
    return -1
def gen(F,L,A):
    p_code['F'].append(F)
    p_code['L'].append(L)
    p_code['A'].append(A)
    return len(p_code['F'])-1  # 返回当前最新指令编号
def backpatch(L,target): # L是一个list，target是跳转目标的编号，为字符串
    for i in range(len(L)):
        p_code['A'][L[i]]=target

def get_pcode():
    return p_code
def show_code():
    for i in range(len(p_code['F'])):
        print(p_code['F'][i],' ',p_code['L'][i],' ',p_code['A'][i])
def write_code():
    f = open("p_code.txt", 'w', encoding="utf-8")
    for i in range(len(p_code['F'])):
        f.write(str(i)+' '+p_code['F'][i]+' '+p_code['L'][i]+' '+str(p_code['A'][i])+'\n')
def get_num(): # 它的作用是返回层次总形参和var的数量,并按顺序返回一个序列供后续查找
    L=[]
    num_var=0
    for i in range(display[-1],len(signal_stack['name'])):
        if signal_stack['type'][i]=='var':
            num_var+=1
            L.append(signal_stack['name'][i])
    return num_var,L
def get_la(name): # 返回name所在的层次和相对地址
    idx=signal_stack['name'][::-1].index(name)
    idx=len(signal_stack['name'])-idx-1
    return signal_stack['value'][idx],signal_stack['address'][idx]

def find_op(op):
    if op=='=':
        return 7
    if op == '<>':
        return 8
    if op == '<':
        return 9
    if op == '<=':
        return 12
    if op == '>':
        return 10
    if op == '>=':
        return 11

def show_stack():
    for i in range(len(signal_stack['name'])):
        print(signal_stack['name'][i],' ',signal_stack['type'][i],' ',str(signal_stack['value'][i]),' ',str(signal_stack['address'][i]))
print(end_of_row)
word = list()
Type = list()
print(len(word))
# 打开文件
file = open("result.txt", "r", encoding="utf-8")
# 按行读入
for line in file:
    # print(line)
    word.append(line[0:line.rfind(' ')])  # 读空格前的连续部分
    Type.append(line[line.rfind(' ') + 1:line.rfind('\n')])
# 关闭文件
file.close()
print(Type)

def find_loc(name):  # 找到name在符号表中定义的层级以及其在符号表的偏移量
    address=find_name(name)  #返回name在符号表的全局地址
    for i in range(len(display)):  # 找到这个name处于哪一个层次
        if address<display[i]:
            return i - 1,address-display[i-1]
    return i,address-display[i] # 如果整个循环结束都没返回，那么就说明它在最顶层

def load_word(Word, indicator):
    indicator += 1
    if indicator < len(Word):
        word = Word[indicator]
        word_type = Type[indicator]
    else:
        print("分析结束")
        indicator = -1
        word = str()
        word_type = str()
    return word, word_type, indicator
def block(strToken, str_type, indicator):
    # display.append(len(signal_stack['name']))
    # 在block内进行append，此时函数名已经存在上一个模块里面了
    # signal_stack['ad']=0 #出现了新的模块，ad置为0
    # signal_stack['level']+=1
    if strToken == 'const' or strToken == 'var' or strToken == 'procedure':
        if strToken == 'const':
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = condecl(strToken, str_type, indicator)

        if strToken == 'var':
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = vardecl(strToken, str_type, indicator)

        if strToken == 'procedure':
            strToken, str_type, indicator = proc(strToken, str_type, indicator)
    gen('opr','0','0')
    if strToken == 'begin':
        num, _ = get_num()
        idx=display[-1]-1
        if idx>=0:
            signal_stack['address'][idx]=len(p_code['F'])
        gen('int', '0', str(3 + num))
        if signal_stack['level']==0:
            p_code['A'][0]=len(p_code['F'])-1 #回填

        strToken, str_type, indicator = body(strToken, str_type, indicator)
    else:
        row, col = find_mistake(indicator)
        print("缺少： begin  (", row, ",", col,")")
    return strToken, str_type, indicator


def condecl(strToken, str_type, indicator):  # 已判断出第一个是const
    strToken, str_type, indicator = const(strToken, str_type, indicator)
    while (strToken == ','):
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = const(strToken, str_type, indicator)
    if strToken == ';':
        strToken, str_type, indicator = load_word(word, indicator)
    else:
        # print("缺少: ;")
        row, col = find_mistake(indicator)
        print("缺少： ;  (", row, ",", col,")")
    return strToken, str_type, indicator


def const(strToken, str_type, indicator):
    name=strToken # 存入栈符号表
    if str_type == '标识符':
        strToken, str_type, indicator = load_word(word, indicator)
        if strToken == ':=':
            strToken, str_type, indicator = load_word(word, indicator)
            if str_type == "常数":
                value=strToken
                strToken, str_type, indicator = load_word(word, indicator)
                enter(name,'const',value)
            else:
                # print("缺少： 常数")
                row, col = find_mistake(indicator)
                print("缺少： 常数  (", row, ",", col, ")")
        else:
            # print("缺少: :=")
            row, col = find_mistake(indicator)
            print("缺少： :=  (", row, ",", col, ")")
    else:
        # print("缺少： 标识符")
        row, col = find_mistake(indicator)
        print("缺少： 标识符  (", row, ",", col,")")
    return strToken, str_type, indicator


def vardecl(strToken, str_type, indicator):  # 已判断出第一个是var
    name=strToken
    if str_type == '标识符':
        strToken, str_type, indicator = load_word(word, indicator)
        enter(name,'var',str(signal_stack['level']))
    else:
        # print("缺少：标识符")
        row, col = find_mistake(indicator)
        print("缺少： 标识符  (", row, ",", col,")")
    while strToken == ',':
        strToken, str_type, indicator = load_word(word, indicator)
        if str_type == '标识符':
            name=strToken
            enter(name, 'var', str(signal_stack['level']))
            strToken, str_type, indicator = load_word(word, indicator)
        else:
            # print("缺少： 标识符")
            row, col = find_mistake(indicator)
            print("缺少： 标识符  (", row, ",", col, ")")
    if strToken == ';':
        strToken, str_type, indicator = load_word(word, indicator)
    else:
        # print("缺少： ;")
        row, col = find_mistake(indicator)
        print("缺少： ;  (", row, ",", col,")")

    return strToken, str_type, indicator


def proc(strToken, str_type, indicator):

    if strToken == 'procedure':
        # display.append(len(signal_stack['name']))  # 子模块，创建对应的符号表
        signal_stack['ad'] = 0  # 出现了新的模块，ad置为0

        strToken, str_type, indicator = load_word(word, indicator)
    else:
        # print("缺少： procedure")
        row, col = find_mistake(indicator)
        print("缺少： procedure  (", row, ",", col,")")
    if str_type == '标识符':
        para_num=0 #记录个数重置
        enter(strToken,'proc',str(signal_stack['level']))
        signal_stack['level'] += 1 # 定义完函数名level就增加
        display.append(len(signal_stack['name'])) # 定义完函数名就要划分符号表，因为有形参
        signal_stack['ad'] = 0  # 定义完函数名，就出现了新的模块，ad置为0
        strToken, str_type, indicator = load_word(word, indicator)
    else:
        # print("缺少： 标识符")
        row, col = find_mistake(indicator)
        print("缺少： 标识符  (", row, ",", col,")")
    if strToken == '(':
        strToken, str_type, indicator = load_word(word, indicator)
    else:
        # print("缺少: (")
        row, col = find_mistake(indicator)
        print("缺少： (  (", row, ",", col,")")
    if str_type == '标识符':
        para_num+=1
        enter(strToken,'var',str(signal_stack['level']))  # 函数名中的形参
        strToken, str_type, indicator = load_word(word, indicator)
        while strToken == ',':
            strToken, str_type, indicator = load_word(word, indicator)
            if str_type == '标识符':
                para_num+=1
                enter(strToken, 'var', str(signal_stack['level']))  # 函数名中的形参
                strToken, str_type, indicator = load_word(word, indicator)
                while str_type == '标识符':
                    # print("缺少： ,")
                    row, col = find_mistake(indicator)
                    print("缺少： ,  (", row, ",", col, ")")
                    strToken, str_type, indicator = load_word(word, indicator)
            elif strToken == ',':
                # print("缺少： 标识符")
                row, col = find_mistake(indicator)
                print("缺少： 标识符  (", row, ",", col, ")")
        if strToken == ')':
            strToken, str_type, indicator = load_word(word, indicator)
            if strToken == ';':
                strToken, str_type, indicator = load_word(word, indicator)
                strToken, str_type, indicator = block(strToken, str_type, indicator)
                while strToken == ';':
                    strToken, str_type, indicator = proc(strToken, str_type, indicator)
            else:
                # print("缺少： ;")
                row, col = find_mistake(indicator)
                print("缺少： ;  (", row, ",", col, ")")
                strToken, str_type, indicator = block(strToken, str_type, indicator)
                while strToken == ';':
                    strToken, str_type, indicator = proc(strToken, str_type, indicator)
        else:
            # print("缺少： )")
            row, col = find_mistake(indicator)
            print("缺少： )  (", row, ",", col, ")")
    elif strToken == ')':
        strToken, str_type, indicator = load_word(word, indicator)

    elif strToken == ',':
        # print("缺少: 标识符")
        row, col = find_mistake(indicator)
        print("缺少： 标识符  (", row, ",", col, ")")
        while strToken == ',':
            strToken, str_type, indicator = load_word(word, indicator)
            if str_type == '标识符':
                strToken, str_type, indicator = load_word(word, indicator)
                while str_type == '标识符':
                    # print("缺少： ,")
                    row, col = find_mistake(indicator)
                    print("缺少： ,  (", row, ",", col, ")")
                    strToken, str_type, indicator = load_word(word, indicator)
            elif strToken == ',':
                # print("缺少： 标识符")
                row, col = find_mistake(indicator)
                print("缺少： 标识符  (", row, ",", col, ")")
        if strToken == ')':
            strToken, str_type, indicator = load_word(word, indicator)
            if strToken == ';':
                strToken, str_type, indicator = load_word(word, indicator)
                strToken, str_type, indicator = block(strToken, str_type, indicator)
                while strToken == ';':
                    strToken, str_type, indicator = proc(strToken, str_type, indicator)
            else:
                # print("缺少： ;")
                row, col = find_mistake(indicator)
                print("缺少： ;  (", row, ",", col, ")")
        else:
            # print("缺少： )")
            row, col = find_mistake(indicator)
            print("缺少： )  (", row, ",", col, ")")
    else:
        # print(strToken + " 应该是标识符，但你输入的是: " + str_type)
        row, col = find_mistake(indicator)
        print(strToken + " 应该是标识符，但你输入的是: " + str_type, row, ",", col, ")")
    Pop()  # 该模块定义结束，将栈符号表和display更新。有误，此处模型不一定定义结束，可能在statment里面
    signal_stack['level'] -= 1
    return strToken, str_type, indicator


def body(strToken, str_type, indicator): # body结束以后，需要把栈符号表的相应内容吐出去
    if strToken == 'begin':
        # body表示当前函数的主体，我们需要生成int代码
        # num,_=get_num()
        # gen('int','0',str(3+num))

        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = statment(strToken, str_type, indicator)  # 传入的strToken判断是否为开始字符
        while strToken == ';':
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = statment(strToken, str_type, indicator)
            while strToken != ';' and strToken != 'end' and (
                    str_type == '标识符' or strToken == 'if' or strToken == 'while' or strToken == 'call' or strToken == 'read' or strToken == 'write' or strToken == 'begin'):
                # print("缺少： ;")  # 为statment的first集
                row, col = find_mistake(indicator)
                print("缺少： ;  (", row, ",", col, ")")
                strToken, str_type, indicator = statment(strToken, str_type, indicator)
        if strToken == 'end':
            strToken, str_type, indicator = load_word(word, indicator)

        else:
            # print("缺少： end")
            row, col = find_mistake(indicator)
            print("缺少： end  (", row, ",", col, ")")
        # Pop()  # 该模块定义结束，将栈符号表和display更新。有误，此处模型不一定定义结束，可能在statment里面
        # signal_stack['level'] -= 1
    else:
        # print("缺少： begin")
        row, col = find_mistake(indicator)
        print("缺少： begin  (", row, ",", col, ")")
    return strToken, str_type, indicator


def statment(strToken, str_type, indicator):
    if str_type == "标识符":
        name=strToken  #记录当前语句左侧的变量名
        if find_name(strToken)==-1:
            row, col = find_mistake(indicator)
            print(strToken,'未定义',"(", row, ",", col, ")")
        strToken, str_type, indicator = load_word(word, indicator)
        if strToken == ':=':
            strToken, str_type, indicator = load_word(word, indicator)
            if strToken==';':
                row, col = find_mistake(indicator)
                print("缺少： 标识符  (", row, ",", col, ")")
                strToken, str_type, indicator = load_word(word, indicator)
            elif strToken=='else':
                row, col = find_mistake(indicator)
                print("缺少： 标识符  (", row, ",", col, ")")

            else:
                strToken, str_type, indicator = exp(strToken, str_type, indicator)

                level,a=get_la(name) # 查找name在模块中是第几个
                gen('sto',str(signal_stack['level']-int(level)),str(a+1+3)) # 将exp的结果送回
        else:
            # print("缺少: :=")
            row, col = find_mistake(indicator)
            print("缺少： :=  (", row, ",", col, ")")
            strToken, str_type, indicator = exp(strToken, str_type, indicator)

    elif strToken == 'if':
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = lexp(strToken, str_type, indicator)
        if strToken == 'then':
            M_1=len(p_code['F']) # 用于回填
            # M_1-1应该是一条jpc指令,跳出if
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = statment(strToken, str_type, indicator)
            if strToken == 'else':
                N_next= len(p_code['F'])
                gen('jmp','0','0') # 存在else的话，上面的语句需要有出口
                M_2=len(p_code['F'])
                strToken, str_type, indicator = load_word(word, indicator)
                strToken, str_type, indicator = statment(strToken, str_type, indicator)
                backpatch([M_1-1],M_2)
                backpatch([N_next],len(p_code['F']))
                return strToken, str_type, indicator
            else:
                if str_type == '标识符' or strToken == 'if' or strToken == 'while' or strToken == 'call' or strToken == 'begin' or strToken == 'read' or strToken == 'write':
                    # print("缺少： else")
                    row, col = find_mistake(indicator)
                    print("缺少： else  (", row, ",", col, ")")
                else:
                    backpatch([M_1-1],len(p_code['F']))
                    return strToken, str_type, indicator

            # elif strToken == 'end':
            #     strToken, str_type, indicator = load_word(word, indicator)
            # else:
            #     print("缺少：end")
        else:
            # print("缺少： then")
            row, col = find_mistake(indicator)
            print("缺少： then  (", row, ",", col, ")")
    elif strToken == 'while':
        M_1=len(p_code['F'])
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = lexp(strToken, str_type, indicator)
        n = len(p_code['F'])-1
        if strToken == 'do':
            M_2 = len(p_code['F'])
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = statment(strToken, str_type, indicator)
            backpatch([M_2-1],len(p_code['F']))
            gen('jmp','0',str(M_1))
            backpatch([n],len(p_code['F']))
            return strToken, str_type, indicator
        else:
            # print("缺少： do")
            row, col = find_mistake(indicator)
            print("缺少： do  (", row, ",", col, ")")
            strToken, str_type, indicator = statment(strToken, str_type, indicator)

    elif strToken == 'call':
        A=4 # 传递的目标参数在它自己的函数中的偏移量
        strToken, str_type, indicator = load_word(word, indicator)
        if str_type == '标识符':
            name=strToken # 把函数名存起来
            if find_name(strToken) == -1:
                row, col = find_mistake(indicator)
                print(strToken, '函数未定义', "(", row, ",", col, ")")
            else:
                strToken, str_type, indicator = load_word(word, indicator)
            if strToken == '(':
                strToken, str_type, indicator = load_word(word, indicator)
                if strToken == ')':
                    strToken, str_type, indicator = load_word(word, indicator)

                else:
                    strToken, str_type, indicator = exp(strToken, str_type, indicator)
                    # 参数需要被传入,结果在栈顶
                    # 形参肯定在活动记录最前面，按顺序放进去即可,但这是关于栈顶的偏移量
                    # 显然它永远是3，因为每一个
                    # 返回定义层级和调用层级的差
                    level,_=get_la(name)
                    b=int(level)-int(signal_stack['level'])
                    if b==0:
                        gen('sto',str(-1),str(A))
                        A+=1
                    else:
                        gen('sto', str(b), str(A))
                        A += 1
                    while strToken == ',':
                        strToken, str_type, indicator = load_word(word, indicator)
                        strToken, str_type, indicator = exp(strToken, str_type, indicator)
                        if b == 0:
                            gen('sto', str(-1), str(A))
                            A += 1
                        else:
                            gen('sto', str(b), str(A))
                            A += 1
                    if strToken == ')':
                        strToken, str_type, indicator = load_word(word, indicator)
                        idx=signal_stack['name'].index(name)
                        a=signal_stack['address'][idx]  # 找到存在符号表的真正地址
                        gen('cal','0',str(a))  # call的目标代码，第三位表示name跳转到的地址
                    else:
                        # print("缺少： )")
                        row, col = find_mistake(indicator)
                        print("缺少： )  (", row, ",", col, ")")

            else:
                # print("缺少： (")
                row, col = find_mistake(indicator)
                print("缺少： (  (", row, ",", col, ")")
                if strToken == ')':
                    strToken, str_type, indicator = load_word(word, indicator)
                else:
                    strToken, str_type, indicator = exp(strToken, str_type, indicator)
                    while strToken == ',':
                        strToken, str_type, indicator = load_word(word, indicator)
                        strToken, str_type, indicator = exp(strToken, str_type, indicator)
                    if strToken == ')':
                        strToken, str_type, indicator = load_word(word, indicator)
                    else:
                        # print("缺少： )")
                        row, col = find_mistake(indicator)
                        print("缺少： )  (", row, ",", col, ")")
        else:
            # print("缺少： 标识符")
            row, col = find_mistake(indicator)
            print("缺少： 标识符  (", row, ",", col, ")")
    elif strToken == 'read':
        strToken, str_type, indicator = load_word(word, indicator)
        if strToken == '(':
            strToken, str_type, indicator = load_word(word, indicator)
            if strToken == ')':
                # print("缺少： 标识符")
                row, col = find_mistake(indicator)
                print("缺少： 标识符  (", row, ",", col, ")")
            elif str_type == '标识符':
                name=strToken
                if find_name(strToken) == -1:
                    row, col = find_mistake(indicator)
                    print(strToken, '未定义', "(", row, ",", col, ")")
                else:  # 在符号表中已经定义
                    level,a=get_la(name)  # 查找name在模块中是第几个
                    # a表示偏移量,从0开始
                    gen('red','0','0')
                    gen('sto',str(signal_stack['level']-int(level)),str(3+a+1))
                # 第二句gen，是把读入的值放到定义的地方，那么就需要确定这个变量在什么地方被定义的，也就是它的层差（当前层和它的
                # 定义层的差，以及对应的偏移量）
                strToken, str_type, indicator = load_word(word, indicator)
                if strToken==')':
                    strToken, str_type, indicator = load_word(word, indicator)
                elif strToken!=',' and str_type!='标识符':
                    row, col = find_mistake(indicator)
                    print("read中不应该出现除了标识符和逗号的内容  (", row, ",", col, ")")
                    while strToken!=')':
                        strToken, str_type, indicator = load_word(word, indicator)
                    strToken, str_type, indicator = load_word(word, indicator)
                else:
                    while strToken == ',':
                        strToken, str_type, indicator = load_word(word, indicator)
                        name=strToken
                        if str_type == '标识符':
                            level, a = get_la(name)  # 查找name在模块中是第几个
                            # a表示偏移量,从0开始
                            gen('red', '0', '0')
                            gen('sto', str(signal_stack['level'] - int(level)), str(3 + a + 1))
                            strToken, str_type, indicator = load_word(word, indicator)
                        else:
                            # print("缺少： 标识符")
                            row, col = find_mistake(indicator)
                            print("缺少： 标识符  (", row, ",", col, ")")
                    if strToken == ')':
                        strToken, str_type, indicator = load_word(word, indicator)
                    else:
                        # print("缺少： )")
                        row, col = find_mistake(indicator)
                        print("缺少： )  (", row, ",", col, ")")
        else:
            # print("缺少： (")
            row, col = find_mistake(indicator)
            print("缺少： (  (", row, ",", col, ")")
            if strToken == ')':
                # print("缺少： 标识符")
                row, col = find_mistake(indicator)
                print("缺少： 标识符  (", row, ",", col, ")")
            elif str_type == '标识符':
                strToken, str_type, indicator = load_word(word, indicator)
                while strToken == ',':
                    strToken, str_type, indicator = load_word(word, indicator)
                    if str_type == '标识符':
                        strToken, str_type, indicator = load_word(word, indicator)
                    else:
                        # print("缺少： 标识符")
                        row, col = find_mistake(indicator)
                        print("缺少： 标识符  (", row, ",", col, ")")
                if strToken == ')':
                    strToken, str_type, indicator = load_word(word, indicator)
                else:
                    # print("缺少： )")
                    row, col = find_mistake(indicator)
                    print("缺少： )  (", row, ",", col, ")")


    elif strToken == 'write':
        strToken, str_type, indicator = load_word(word, indicator)
        if strToken == '(':
            strToken, str_type, indicator = load_word(word, indicator)
            if strToken == ')':
                # print("缺少： exp")
                row, col = find_mistake(indicator)
                print("缺少： exp  (", row, ",", col, ")")
            else:
                # strToken, str_type, indicator = load_word(word, indicator)
                strToken, str_type, indicator = exp(strToken, str_type, indicator)
                gen('wrt','0','0')
                gen('opr','0','13')
                # 这两个gen紧跟exp之后，表示将栈顶元素输出并且换行
                while strToken == ',':
                    strToken, str_type, indicator = load_word(word, indicator)
                    strToken, str_type, indicator = exp(strToken, str_type, indicator)
                    gen('wrt', '0', '0')
                    gen('opr', '0', '13')
                    # 这两个gen紧跟exp之后，表示将栈顶元素输出并且换行
                if strToken == ')':
                    strToken, str_type, indicator = load_word(word, indicator)
                else:
                    # print("缺少： )")
                    row, col = find_mistake(indicator)
                    print("缺少： )  (", row, ",", col, ")")
        else:
            # print("缺少： (")
            row, col = find_mistake(indicator)
            print("缺少： (标识符)  (", row, ",", col, ")")
            if strToken == ')':
                # print("缺少： exp")
                row, col = find_mistake(indicator)
                print("缺少： exp  (", row, ",", col, ")")
            else:
                # strToken, str_type, indicator = load_word(word, indicator)
                strToken, str_type, indicator = exp(strToken, str_type, indicator)
                while strToken == ',':
                    strToken, str_type, indicator = load_word(word, indicator)
                    strToken, str_type, indicator = exp(strToken, str_type, indicator)
                if strToken == ')':
                    strToken, str_type, indicator = load_word(word, indicator)
                else:
                    # print("缺少： )")
                    row, col = find_mistake(indicator)
                    print("缺少： )  (", row, ",", col, ")")


    elif strToken == 'begin':  # body
        # strToken, str_type, indicator = load_word(word, indicator)
        # strToken, str_type, indicator= statment(strToken, str_type, indicator)
        # while strToken == ';':
        #     strToken, str_type, indicator = statment(strToken, str_type, indicator)
        # if strToken == 'end':
        #     strToken, str_type, indicator = load_word(word, indicator)
        # else:
        #     # print("缺少： end")
        #     row, col = find_mistake(indicator)
        #     print("缺少： end  (", row, ",", col, ")")
        strToken, str_type, indicator = body(strToken, str_type, indicator)
    else:
        print("statement非法")
    return strToken, str_type, indicator


def lexp(strToken, str_type, indicator):
    if strToken == 'odd':
        a=6
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = exp(strToken, str_type, indicator)
        gen('opr','0',str(a))
        gen('jpc','0','')  # 在statment中会回填
    else:
        strToken, str_type, indicator = exp(strToken, str_type, indicator)
        if strToken == '=' or strToken == '<>' or strToken == '<' or strToken == '<=' or strToken == '>' or strToken == '>=':
            op=strToken # 记录这个操作，用于生成目标代码
            a=find_op(op)
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = exp(strToken, str_type, indicator)
            gen('opr','0',str(a))
            gen('jpc', '0', '')  # 在statment中会回填
        else:
            # 有两种情况，缺少odd或者缺少lop，分别对应产生式的两种可能
            if strToken != ')' and strToken != ';' and strToken != 'do' and strToken != 'then' and strToken != ',':
                # print("缺少： odd")
                row, col = find_mistake(indicator)
                print("缺少： odd  (", row, ",", col, ")")
            else:
                # print("缺少： lop")
                row, col = find_mistake(indicator)
                print("缺少： lop  (", row, ",", col, ")")
                strToken, str_type, indicator = exp(strToken, str_type, indicator)

    return strToken, str_type, indicator


def exp(strToken, str_type, indicator):
    if strToken == '+' or strToken == '-':
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = term(strToken, str_type, indicator)
        if strToken=='-':
            gen('opr','0','1')
        while strToken == '+' or strToken == '-':
            op=strToken
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = term(strToken, str_type, indicator)
            if op == '-':
                gen('opr', '0', '3')
            else:
                gen('opr', '0', '2')
            # 可能漏打了一个aop
            while strToken != '+' and strToken != '-' and strToken != ')' and strToken != ';' and strToken != 'do' and strToken != 'then' and strToken != ',':
                # 只是忘记打aop了，后面一个还是term
                # print("缺少： aop")
                row, col = find_mistake(indicator)
                print("缺少： aop  (", row, ",", col, ")")
                strToken, str_type, indicator = term(strToken, str_type, indicator)

    else:
        strToken, str_type, indicator = term(strToken, str_type, indicator)
        while strToken == '+' or strToken == '-':
            op=strToken
            strToken, str_type, indicator = load_word(word, indicator)
            if strToken==';' or strToken=='else' or strToken=='end' or strToken==')': #exp的follow集合
                row, col = find_mistake(indicator)
                print("缺少： 标识符  (", row, ",", col, ")")
            else:
                strToken, str_type, indicator = term(strToken, str_type, indicator)
                if op == '-':
                    gen('opr', '0', '3')
                else:
                    gen('opr', '0', '2')

                # 可能漏打了一个aop
                while strToken != '+' and strToken != '-' and strToken != ')' and strToken != ';' and strToken != 'do' and strToken != 'then' and strToken!='else' and strToken!='end':
                    # 只是忘记打aop了，后面一个还是term
                    strToken, str_type, indicator = term(strToken, str_type, indicator)

    return strToken, str_type, indicator


def factor(strToken, str_type, indicator):
    if str_type == '标识符':
        name=strToken
        ad=find_name(strToken) #ad 表示标识符的位置，我们需要根据它确定标识符是var还是const
        if ad == -1:
            row, col = find_mistake(indicator)
            print(strToken, '未定义', "(", row, ",", col, ")")
        else:
            if signal_stack['type'][ad]=='const':
                gen('lit','0',signal_stack['value'][ad])  # const直接传数字
            elif signal_stack['type'][ad]=='var':
                level,a=get_la(name)
                gen('lod',str(int(signal_stack['level'])-int(level)),str(3+a+1))
        strToken, str_type, indicator = load_word(word, indicator)
    elif str_type == '常数':
        gen('lit', '0', strToken)  # 直接传数字
        strToken, str_type, indicator = load_word(word, indicator)
    elif strToken == '(':
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = exp(strToken, str_type, indicator)
        # exp中已经把结果传到栈顶，所以不用再生成代码
        if strToken == ')':

            strToken, str_type, indicator = load_word(word, indicator)
        else:
            # print("缺少: )")
            row, col = find_mistake(indicator)
            print("缺少： )  (", row, ",", col, ")")
    else:
        # 由于已经进行过词法分析，因此错误主要可能为以下两种
        # print("factor 出错")
        if str_type == '保留字':
            # print(strToken + " 不应该为保留字，应该为常数或标识符")
            row, col = find_mistake(indicator)
            print(strToken + " 不应该为保留字，应该为常数或标识符", row, ",", col, ")")
        else:
            # print("缺少: (")
            row, col = find_mistake(indicator)
            print("缺少： (  (", row, ",", col, ")")
            strToken, str_type, indicator = exp(strToken, str_type, indicator)
            if strToken == ')':
                strToken, str_type, indicator = load_word(word, indicator)
            else:
                # print("缺少: )")
                row, col = find_mistake(indicator)
                print("缺少： )  (", row, ",", col, ")")

    return strToken, str_type, indicator


def term(strToken, str_type, indicator):
    strToken, str_type, indicator = factor(strToken, str_type, indicator)
    if strToken == '*' or strToken == '/':
        op=strToken
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = factor(strToken, str_type, indicator)
        if op=='*':
            gen('opr','0','4')
        else:
            gen('opr','0','5')
        while (strToken == '*' or strToken == '/'):
            op=strToken
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = factor(strToken, str_type, indicator)
            if op == '*':
                gen('opr', '0', '4')
            else:
                gen('opr', '0', '5')

    return strToken, str_type, indicator


indicator = 0
strToken = word[indicator]
str_type = Type[indicator]
if strToken == "program":
    strToken, str_type, indicator = load_word(word, indicator)
    display.append(0)
    gen('jmp','0','0')  # 后续需要回填，让他跳转到主程序
else:
    # print("缺少：program")
    row, col = find_mistake(indicator)
    print("缺少： program  (", row, ",", col, ")")
if str_type == "标识符":
    strToken, str_type, indicator = load_word(word, indicator)
else:
    # print("缺少:id")
    row, col = find_mistake(indicator)
    print("缺少： 标识符  (", row, ",", col, ")")
if strToken == ';':
    strToken, str_type, indicator = load_word(word, indicator)
else:
    # print("缺少：;")
    row, col = find_mistake(indicator)
    print("缺少： ;  (", row, ",", col, ")")
block(strToken, str_type, indicator)
gen('opr','0','0')
show_code()
write_code()