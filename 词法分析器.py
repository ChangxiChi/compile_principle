reserseWord = {"const": 1, "var": 2, "procedure": 3, "begin": 4, "end": 5, "if": 6, "then": 7, "while": 8, "do": 9,
               "call": 10, "odd": 11, "write": 12,
               "read": 13, "program": 14}  # 保留字
Operator = ["+", "-", "*", "/", '=', '<>', ":=", "<=", ">=", ">", "<"]  # 算符
Delimiter = ["(", ")", ",", ";"]  # 界符
Identifier_list = []  # 符号表
Const_list = []  # 常数表

end_of_row = [0]  # 记录每一行最后一个字符的下标，用于确认错误所在的行号和列号
word=[] #记录每个单词的最后一个位置
table={'name':[],'type':[],'value':[],'address':[]}
def GetChar(article, indicator):  # indicator表示指示器
    ch = article[indicator]
    indicator += 1
    return ch, indicator


def GetBC(ch, article, indicator):
    while (ch == ' ' and indicator < len(article)):
        ch, indicator = GetChar(article, indicator)
    if ch == ' ' and indicator >= len(article) - 1:
        return ch, -1
    else:
        return ch, indicator


def Concat(ch, strToken):
    strToken = strToken + ch
    return strToken


def IsLetter(ch):
    if ((ch >= 'a' and ch <= 'z') or (ch >= 'A' and ch <= 'Z')):
        return True
    else:
        return False


def IsDigit(ch):
    if (ch >= '0' and ch <= '9'):
        return True
    else:
        return False


def Reverse(strToken):
    if (strToken not in reserseWord):
        return 0;
    else:
        return reserseWord[strToken]


def Retract(indicator):
    ch = ''
    return ch, indicator - 1


def InsertId(strToken):
    Identifier_list.append(strToken)
    return


def InsertConst(strToken):
    Const_list.append(strToken)
    return


def find_mistake(indicator):  # 返回错误的位置
    row = 0
    for i in range(len(end_of_row)):
        if (indicator >= end_of_row[i]):
            row += 1
            indicator += 1
        else:
            break
    col = indicator - end_of_row[row - 1]
    return row, col


f = open("article.txt", encoding="utf-8")
# 输出读取到的数据
a = f.read()
article = str()
# 关闭文件
f.close()

f = open("result.txt", 'w', encoding="utf-8")
# 输出读取到的数据

# 关闭文件


for i in range(len(a)):
    if i==len(a)-1:
        if a[i]=='.':
            break
        else:
            print("error:结束符不是'.'")
            break
    if a[i] != '\n' and a[i]!='\t':
        article = article + a[i]
    else:
        article = article + ' '
        end_of_row.append(i)
article = article + ' '

# 以下是具体实现过程
char_num = 0

indicator = 0
while indicator < len(article) and len(article) != 0:
    ch, indicator = GetChar(article, indicator)
    ch, indicator = GetBC(ch, article, indicator)
    strToken = str()
    if indicator == -1:  # 判断文章的末尾是不是全为空格
        break

    if IsLetter(ch):
        while (IsDigit(ch) or IsLetter(ch)) and indicator < len(article):
            strToken = Concat(ch, strToken)
            ch, indicator = GetChar(article, indicator)
        ch, indicator = Retract(indicator)
        code = Reverse(strToken)
        if code == 0:
            InsertId(strToken)
            print(strToken + ' 标识符')
            table['name'].append(strToken)
            table['type'].append('var') # 这里将const、var、proc都当作var，因为词法分析暂时无法确定
            table['value'].append('')
            table['address'].append('')
            f.write(strToken + ' 标识符\n')
            word.append(indicator-1)
            strToken = str()
        else:
            print(strToken + ' 保留字')
            f.write(strToken + ' 保留字\n')
            word.append(indicator-1)
            strToken = str()
    elif IsDigit(ch):
        while IsDigit(ch) and indicator < len(article):
            strToken = Concat(ch, strToken)
            ch, indicator = GetChar(article, indicator)
        if IsDigit(ch):
            print(strToken + ch + ' 常数')
            f.write(strToken + ch + ' 常数\n')
            word.append(indicator-1)
            break
        elif ch == ' ' or ch in Operator or ch in Delimiter:
            ch, indicator = Retract(indicator)
            InsertConst(strToken)
            print(strToken + ' 常数')
            f.write(strToken + ' 常数\n')
            word.append(indicator-1)
        else:
            row, col = find_mistake(indicator)
            while ch != ' ' and ch not in Operator and ch not in Delimiter and indicator < len(article):  # 未遇到空格,界符和算符
                strToken = Concat(ch, strToken)
                ch, indicator = GetChar(article, indicator)
            ch, indicator = Retract(indicator)
            print("error" + "(", row, ",", col, "):" + strToken + ' is not const')
            a = "error" + "(" + str(row) + "," + str(col) + "): " + strToken + " is not const\n"
            f.write(a)
            word.append(indicator-1)
            strToken = str()
    elif ch in Operator:
        if ch=='>':
            if article[indicator]=='=':
                strToken=ch+'='
                indicator+=1
            else:
                strToken='>'
        elif ch=='<':
            if article[indicator]=='=':
                strToken = ch + '='
                indicator+=1
            elif article[indicator]=='>':
                strToken = ch + '>'
                indicator+=1
            else:
                strToken='<'
        else:
            strToken = Concat(ch, strToken)
        print(strToken + " 算符")
        f.write(strToken + " 算符\n")
        word.append(indicator-1)
        strToken = str()
    elif ch in Delimiter:
        strToken = Concat(ch, strToken)
        print(strToken + " 界符")
        f.write(strToken + " 界符\n")
        word.append(indicator-1)
        strToken = str()
    elif ch == ':':
        strToken = Concat(ch, strToken)
        ch, indicator = GetChar(article, indicator)
        if ch == '=':
            strToken = Concat(ch, strToken)
        else:
            row, col = find_mistake(indicator)
            ch, indicator = Retract(indicator)
            print("error" + "(", row, ",", col - 1, "): " + strToken + " not valid")
            a = "error" + "(" + str(row) + "," + str(col) + "): " + strToken + " not valid\n"
            f.write(a)
            word.append(indicator-1)
            strToken = str()
            continue
        print(strToken + " 赋值符")
        f.write(strToken + " 赋值符\n")
        word.append(indicator-1)
        strToken = str()
    elif ch == '>':
        strToken = Concat(ch, strToken)
        ch, indicator = GetChar(article, indicator)
        if ch == '=':
            strToken = Concat(ch, strToken)
        else:
            ch, indicator = Retract(indicator)
        print(strToken + " 算符")
        f.write(strToken + " 算符\n")
        word.append(indicator-1)
        strToken = str()
    elif ch == '<':
        strToken = Concat(ch, strToken)
        ch, indicator = GetChar(article, indicator)
        if ch == '=':
            strToken = Concat(ch, strToken)
        else:
            ch, indicator = Retract(indicator)
        print(strToken + " 算符")
        f.write(strToken + " 算符\n")
        word.append(indicator-1)
        strToken = str()
    else:
        row, col = find_mistake(indicator)
        while ch != ' ' and ch not in Operator and ch not in Delimiter and indicator < len(article) and not IsDigit(
                ch) and not IsLetter(ch):
            strToken = Concat(ch, strToken)
            ch, indicator = GetChar(article, indicator)
        ch, indicator = Retract(indicator)
        print("error" + "(", row, ",", col, "): " + strToken + " not valid")
        a = "error" + "(" + str(row) + "," + str(col) + "): " + strToken + " not valid\n"
        f.write(a)
        word.append(indicator-1)
        strToken = str()
f.close()

def get_data():
    return end_of_row,word
print(word)

