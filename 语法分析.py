from 词法分析器 import get_data
end_of_row,Word=get_data()
def find_mistake(indicator):  # 返回错误的位置
    indicator-=1
    indicator=Word[indicator]-len(word[indicator])+1 # 得到开始位置
    row = 0
    for i in range(len(end_of_row)):
        if (indicator >= end_of_row[i]):
            row += 1
        else:
            break
    col = indicator - end_of_row[row - 1]
    return row, col

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


# def alignment(word, indicator, target):  # 对齐到目标target
#     strToken, str_type, indicator = load_word(word, indicator)
#     while strToken != target:
#         strToken, str_type, indicator = load_word(word, indicator)
#     return strToken, str_type, indicator


# print(word[0])

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
    if strToken == 'const' or strToken == 'var' or strToken == 'procedure':
        if strToken == 'const':
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = condecl(strToken, str_type, indicator)

        if strToken == 'var':
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = vardecl(strToken, str_type, indicator)

        if strToken == 'procedure':
            strToken, str_type, indicator = proc(strToken, str_type, indicator)

    if strToken == 'begin':
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
    if str_type == '标识符':
        strToken, str_type, indicator = load_word(word, indicator)
        if strToken == ':=':
            strToken, str_type, indicator = load_word(word, indicator)
            if str_type == "常数":
                strToken, str_type, indicator = load_word(word, indicator)
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
    if str_type == '标识符':
        strToken, str_type, indicator = load_word(word, indicator)
    else:
        # print("缺少：标识符")
        row, col = find_mistake(indicator)
        print("缺少： 标识符  (", row, ",", col,")")
    while strToken == ',':
        strToken, str_type, indicator = load_word(word, indicator)
        if str_type == '标识符':
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
        strToken, str_type, indicator = load_word(word, indicator)
    else:
        # print("缺少： procedure")
        row, col = find_mistake(indicator)
        print("缺少： procedure  (", row, ",", col,")")
    if str_type == '标识符':
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
        strToken, str_type, indicator = load_word(word, indicator)
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
    return strToken, str_type, indicator


def body(strToken, str_type, indicator):
    if strToken == 'begin':
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

    else:
        # print("缺少： begin")
        row, col = find_mistake(indicator)
        print("缺少： begin  (", row, ",", col, ")")
    return strToken, str_type, indicator


def statment(strToken, str_type, indicator):
    if str_type == "标识符":
        strToken, str_type, indicator = load_word(word, indicator)
        if strToken == ':=':
            strToken, str_type, indicator = load_word(word, indicator)
            if strToken==';':
                row, col = find_mistake(indicator)
                print("缺少： 标识符  (", row, ",", col, ")")
                strToken, str_type, indicator = load_word(word, indicator)
            else:
                strToken, str_type, indicator = exp(strToken, str_type, indicator)
        else:
            # print("缺少: :=")
            row, col = find_mistake(indicator)
            print("缺少： :=  (", row, ",", col, ")")
            strToken, str_type, indicator = exp(strToken, str_type, indicator)

    elif strToken == 'if':
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = lexp(strToken, str_type, indicator)
        if strToken == 'then':
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = statment(strToken, str_type, indicator)
            if strToken == 'else':
                strToken, str_type, indicator = load_word(word, indicator)
                strToken, str_type, indicator = statment(strToken, str_type, indicator)

            else:
                if str_type == '标识符' or strToken == 'if' or strToken == 'while' or strToken == 'call' or strToken == 'begin' or strToken == 'read' or strToken == 'write':
                    # print("缺少： else")
                    row, col = find_mistake(indicator)
                    print("缺少： else  (", row, ",", col, ")")
                # 否则暂时不需要else

            # elif strToken == 'end':
            #     strToken, str_type, indicator = load_word(word, indicator)
            # else:
            #     print("缺少：end")
        else:
            # print("缺少： then")
            row, col = find_mistake(indicator)
            print("缺少： then  (", row, ",", col, ")")
    elif strToken == 'while':
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = lexp(strToken, str_type, indicator)
        if strToken == 'do':
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = statment(strToken, str_type, indicator)
        else:
            # print("缺少： do")
            row, col = find_mistake(indicator)
            print("缺少： do  (", row, ",", col, ")")
            strToken, str_type, indicator = statment(strToken, str_type, indicator)

    elif strToken == 'call':
        strToken, str_type, indicator = load_word(word, indicator)
        if str_type == '标识符':
            strToken, str_type, indicator = load_word(word, indicator)
            if strToken == '(':
                strToken, str_type, indicator = load_word(word, indicator)
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
                strToken, str_type, indicator = load_word(word, indicator)
                if strToken!=',' or str_type!='标识符':
                    row, col = find_mistake(indicator)
                    print("read中不应该出现除了标识符和逗号的内容  (", row, ",", col, ")")
                    while strToken!=')':
                        strToken, str_type, indicator = load_word(word, indicator)
                    strToken, str_type, indicator = load_word(word, indicator)
                else:
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


    elif strToken == 'begin':
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = statment(strToken, str_type, indicator)
        while strToken == ';':
            strToken, str_type, indicator = statment(strToken, str_type, indicator)
        if strToken == 'end':
            strToken, str_type, indicator = load_word(word, indicator)
        else:
            # print("缺少： end")
            row, col = find_mistake(indicator)
            print("缺少： end  (", row, ",", col, ")")
    else:
        print("statement非法")
    return strToken, str_type, indicator


def lexp(strToken, str_type, indicator):
    if strToken == 'odd':
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = exp(strToken, str_type, indicator)
    else:
        strToken, str_type, indicator = exp(strToken, str_type, indicator)
        if strToken == '=' or strToken == '<>' or strToken == '<' or strToken == '<=' or strToken == '>' or strToken == '>=':
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = exp(strToken, str_type, indicator)
        else:
            # 有两种情况，确实odd或者缺少lop，分别对应产生式的两种可能
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
        while strToken == '+' or strToken == '-':
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = term(strToken, str_type, indicator)

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
            strToken, str_type, indicator = load_word(word, indicator)
            if strToken==';' or strToken=='else' or strToken=='end' or strToken==')': #exp的follow集合
                row, col = find_mistake(indicator)
                print("缺少： 标识符  (", row, ",", col, ")")
            else:
                strToken, str_type, indicator = term(strToken, str_type, indicator)

                # 可能漏打了一个aop
                while strToken != '+' and strToken != '-' and strToken != ')' and strToken != ';' and strToken != 'do' and strToken != 'then' and strToken!='else':
                    # 只是忘记打aop了，后面一个还是term
                    strToken, str_type, indicator = term(strToken, str_type, indicator)

    return strToken, str_type, indicator


def factor(strToken, str_type, indicator):
    if str_type == '标识符':
        strToken, str_type, indicator = load_word(word, indicator)
    elif str_type == '常数':
        strToken, str_type, indicator = load_word(word, indicator)
    elif strToken == '(':
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = exp(strToken, str_type, indicator)
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
        strToken, str_type, indicator = load_word(word, indicator)
        strToken, str_type, indicator = factor(strToken, str_type, indicator)
        while (strToken == '*' or strToken == '/'):
            strToken, str_type, indicator = load_word(word, indicator)
            strToken, str_type, indicator = factor(strToken, str_type, indicator)

    return strToken, str_type, indicator


indicator = 0
strToken = word[indicator]
str_type = Type[indicator]
if strToken == "program":
    strToken, str_type, indicator = load_word(word, indicator)
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
