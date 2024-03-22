from 语义分析_测试版本 import get_pcode,show_code
p_code=get_pcode()
stack=[]
for i in range(1000):
    stack.append(0)
  # 表示当前正在执行的指令地址

  # 静态链
  # 返回地址
  # 动态链（老sp）

# 偏移量从1开始

T=0  # 指向数据栈栈顶
B=0  # 存储基地址，存储指向老SP的
P=0  # 指向下一条要执行的指令地址
I=P  # 一开始下一条指令的编号为0

bias=0 # 由于传参会影响栈顶指针，这里记录因为传参带来的偏移
def initial(num):
    a=T+num-bias
    return a

while P<len(p_code['F']):
    I=P
    # print('I:', I)
    if p_code['F'][I]=='lit':
        #print('I:',I)# test
        stack[T]=int(p_code['A'][I])
        T+=1
        P+=1
        bias+=1
    elif p_code['F'][I]=='lod':
        if p_code['L'][I]=='0':
            v=stack[B+int(p_code['A'][I])-1]
            stack[T]=v
            T+=1
            bias+=1
        else:
            add=stack[B+2]  # 第三个放着静态链,这算第一次
            for i in range(int(p_code['L'][I])-1): # 往回跳层差次-1,前面已经跳过一次了
                add=stack[add+2]
            v=stack[add+int(p_code['A'][I])-1]
            stack[T]=v
            T+=1
            bias+=1
        P=I+1
        # 取到栈顶以后，栈顶指针会随之增加，bias需要加一
    elif p_code['F'][I]=='sto':  # 不会退栈
        v=stack[T-1]
        L=int(p_code['L'][I])
        if L<0:
            # 传参数
            # 同时确定静态链接
            b=int(p_code['A'][I])
            add=stack[B+2]
            for i in range(-L-1):
                add=stack[add+2]
            stack[T+2-bias]=add
            stack[T-bias+b-1]=v
        elif L==0:
            a=int(p_code['A'][I])
            stack[B+a-1]=v
        else:
            add = stack[B + 2]  # 第三个放着静态链,这算第一次
            for i in range(int(p_code['L'][I]) - 1):  # 往回跳层差次-1,前面已经跳过一次了
                add = stack[add + 2]
            stack[add+int(p_code['A'][I])-1]=v
        P = I + 1
    elif p_code['F'][I] == 'cal':
        T=T-bias # 活动记录栈顶
        # 恢复
        bias=0
        stack[T+1]=I+1 # 返回指令地址
        stack[T]=B #动态链
        B=T
        # 必须在cal就放，因为cal后面才是返回的目的地
        # 传参在前面均已完成
        P = int(p_code['A'][I])
    elif p_code['F'][I] == 'int': # 填入静态链和动态链以及返回地址
        num=int(p_code['A'][I])
        T=initial(num)
        # 动态链、返回地址、静态链均已填写好
        B=T-num
        P=I+1

    elif p_code['F'][I] == 'jmp':
        P=int(p_code['A'][I])
    elif p_code['F'][I] == 'jpc':
        if stack[T-1]==0:
            P=int(p_code['A'][I])
        else:
            P=I+1
    elif p_code['F'][I] == 'wrt':
        print(stack[T-1])
        P = I + 1
    elif p_code['F'][I] == 'opr':
        # 也要做bias清零
        if p_code['A'][I]=='0':
            if B==0:
                break
            else:
                P=stack[B+1] #存着返回到的指令，就是下一条该执行的指令
                T=B # 恢复到原来的栈顶
                B=stack[B]
            # T-=bias
            bias=0
        elif p_code['A'][I]=='1':
            stack[T-1]=-stack[T-1]
            P = I + 1
        elif p_code['A'][I] == '2':
            sum=stack[T-1]+stack[T-2]
            T=T-1
            stack[T-1]=sum
            bias-=1
            P = I + 1
        elif p_code['A'][I] == '3':
            sub = stack[T - 2] - stack[T - 1]
            T = T - 1
            stack[T - 1] = sub
            bias -= 1
            P = I + 1
        elif p_code['A'][I] == '4':
            mul = stack[T - 1] * stack[T - 2]
            T = T - 1
            stack[T - 1] = mul
            bias -= 1
            P = I + 1
        elif p_code['A'][I] == '5':
            div = stack[T - 2] / stack[T - 1]
            T = T - 1
            stack[T - 1] = div
            bias -= 1
            P = I + 1
        elif p_code['A'][I] == '6':
            # 奇数为1，偶数为0
            t=stack[T-1]
            if t%2==0:
                stack[T-1]=0
            else:
                stack[T-1]=1
            P = I + 1
        elif p_code['A'][I] == '7':
            if stack[T-1]==stack[T-2]:
                res=1
            else:
                res=0
            T=T-1
            stack[T-1]=res
            bias -= 1
            P = I + 1
        elif p_code['A'][I] == '8':
            if stack[T-1]==stack[T-2]:
                res=0
            else:
                res=1
            T=T-1
            stack[T-1]=res
            bias -= 1
            P = I + 1
        elif p_code['A'][I] == '9':
            if stack[T-1]>stack[T-2]:
                res=1
            else:
                res=0
            T=T-1
            stack[T-1]=res
            bias -= 1
            P = I + 1
        elif p_code['A'][I] == '10':
            if stack[T-1]<=stack[T-2]:
                res=1
            else:
                res=0
            T=T-1
            stack[T-1]=res
            bias -= 1
            P = I + 1
        elif p_code['A'][I] == '11':
            if stack[T-1]>stack[T-2]:
                res=1
            else:
                res=0
            T=T-1
            stack[T-1]=res
            bias -= 1
            P = I + 1
        elif p_code['A'][I] == '12':
            if stack[T-1]>=stack[T-2]:
                res=1
            else:
                res=0
            T=T-1
            stack[T-1]=res
            bias -= 1
            P = I + 1
        elif p_code['A'][I] == '13':
            print('\n')
            P = I + 1
    else: #red
        print("请输入值:")
        a=int(input())
        stack[T]=a
        T+=1
        P=I+1
        bias+=1