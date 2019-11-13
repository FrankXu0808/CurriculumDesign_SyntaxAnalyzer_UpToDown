#!/usr/bin/python
# -*- coding: UTF-8 -*-
import  re
import SyntaxTree
#驱动器
def Drive(w,table,str,notes):

    w+="#"
    S = re.split(r'::=', str[0])[0]  # Aj
    head = SyntaxTree.nodes(S)#语法树头部

    nodeStack=[head]#结点栈
    stack=["#",S]
    i=0
    p=stack[len(stack)-1]
    error={}
    while(i<len(w)):


        treePoint = nodeStack[-1]  # 当前指向的语法结点
        print(stack,'\t',"    ", end="")
        print(w[i:],'\t',"    ", end="")

        word="intial"
        #确定当前输入字符
        note=isNote(notes,w[i:],0)
        #print("i=",i," ",end="")
        if(note==False):
            word=w[i]
        else:
            word=note
        top=""
        #判断栈顶元素是终结符还是非终结符
        if(p[0].isupper()):#非终结符
            if(p=='\''):
                for z in range(len(stack) - 1, -1, -1):
                    if(stack[z]!='\''):
                        top=stack[z:]
                        temp=""
                        for s in top:
                            temp+=s
                        break
                top=temp
            else:
                top=p

            if(word in table[top].keys()):#在预测分析表里查到对应内容

                #POP
                print("pop(", stack[-1], "),",'\t', end="")
                stack.pop()
                nodeStack.pop()

                #PUSH
                print("push(", table[top][word], ")",'\t')
                #构造ε语法树结点
                if(table[top][word]=='ε'):
                    tempNode=SyntaxTree.nodes('ε')
                    #print(treePoint.getdata(),"@@add ", tempNode.getdata())
                    treePoint.add(tempNode)

                else:#非终结符，展开式右部不为ε

                    q=len(table[top][word])-1
                    pushstr=[]
                    while(q>=0):

                        s=table[top][word][q]
                        index=-1
                        #处理产生式右部 的非终结符
                        if(s=='\'' or s.isupper()):
                           if(s=='\''):
                            for j in range(q-1,-1,-1):
                                if(table[top][word][j]=='\''):
                                    s+='\''
                                    index=j
                                else:
                                    q=j
                                    break;
                            s+=table[top][word][index-1]

                        #处理产生式右部的 终结符
                        elif(s.lower()):
                            #判断是否是特殊终结符，如id，num，mod
                            temp = ""
                            for c in range(0,len(table[top][word])):
                                temp += table[top][word][c]

                            note = isNote(notes, temp, 0)
                            if (note != False):
                                s=""
                                for d in note[::-1]:
                                   s+=d
                                q=q-len(s)+1


                        pushstr.append(s[::-1])
                        q=q-1

                    nodelist=[]

                    for s in pushstr:
                        stack.append(s)
                        addnode=SyntaxTree.nodes(s)
                        nodeStack.append(addnode)
                        nodelist.append(addnode)
                    for s in nodelist[::-1]:

                        treePoint.add(s)








            else:
                print()
                print("字符<",w[i],">error,产生式不匹配，抛弃本字符")
                error[i]=w[i]
                i=i+1
                #break;


        else:#终结符
            top=stack[-1]
            if(top==word):
                print("pop(",top,")",'\t')
                stack.pop()
                i = i + len(word)
                # addnode = Tree.nodes(top)
                # treePoint.add(addnode)
                #

                nodeStack.pop()


            else:
                print()
                print("字符<", w[i], ">error,栈顶元素不匹配，抛弃本字符")
                error[i] = w[i]
                i = i + 1
                #break;
        p=stack[len(stack)-1]
        if(p=="#"):
            print(stack,w[i:],"succed")
            break;
    print("错误信息:")
    if(len(error)==0):
        print("无")
        tree = SyntaxTree.tree(head)
        #tree.LeftSearchPrint()
        print("语法树:")
        tree.PrintByLevel(50)
        return 1
    else:
        for s in error.keys():
            if(error[s]!='#' and w[int(s)]!='#'):
             print("坐标",s,"，语法匹配错误:",error[s])
             return  0
#构造预测分析表
def CR_PATable(first,follow,str,G,note):#构造预测分析表
    table={}
    final={"  ":0}

    for s in str:
        aLe = re.split(r'::=', s)[0]  # Aj
        aEx = re.split(r'\|', re.split(r'::=', s)[1])  # Aj->&1|&2....
        A={}
        for k in aEx:
          if(len(k)>0):
            temp=FIRST(k,G,note,first)
            # print(k,"%%%",temp)
            for a in temp:
                if(a=='ε'):
                    f=follow[aLe]
                    for b in f:
                        A[b]=k
                        final[b]=0
                else:A[a]=k
                final[a]=0
        table[aLe]=A
    #输出预测分析表
    final.pop('ε')
    for s in final:
        print(s,"   ",end='')
    print()
    for s in table:
        print(s,end=' \t')
        for ss in final:

            if(ss in table[s].keys()):
                print(table[s][ss],end='    ')
            elif(ss!="  "):
                print("er", end='    ')
        print()
    print(table)
    return table
#是否是特殊终结符
def isNote(note,temp,index):
    for s in note:
        if(temp.find(s)==index):
            return s
    return  False
#构造非终结符的FIRST集合
def CR_FIRST(str,G,note):
    first={}
    # 倒序进行求first集合
    for i in range(len(str))[::-1]:
        #  取左部和右部
        aLe = re.split(r'::=', str[i])[0]  # A fi=[]
        aEx = re.split(r'\|', re.split(r'::=', str[i])[1])  # A->&1|&2....
        # fi是保存计算过程中被认为是first集合中元素的集合
        fi=[]
        # 若非终结符退出伊普西龙，直接加入fi
        if(G[aLe].find('ε')>0):fi.append('ε')
        for s in aEx:
          #   构造 X-》Y0 Y1 Y2 ....Yk YK+1
          if(len(s)>0 and s!='ε'):
            temp=s;
            temp=temp.replace(temp[0],'ε'+temp[0])
            temp+='ε'
            # 条件三判断过程
            for j in range(len(temp)):
                # 表达式是ε
                if(temp[j]=='ε'):
                    if(temp[j+1].isupper()==False):
                        judge=isNote(note,temp,j+1)
                        if(judge==False):fi.append(temp[j+1])
                        else:fi.append(temp[j+1:j+1+len(judge)])
                    else:
                        Le=temp[j+1]
                        for k in range(j+1,len(temp)):
                            if(temp[k]=='\''):Le+='\''
                            else:break;
                        # print(first)
                        for s in first[Le]:
                            fi.append(s)
                # 表达式中扫描到非终结符
                elif(temp[j].isupper()):
                    # 判断非终结符带不带引号
                    Le = temp[j ]
                    for k in range(j , len(temp)):
                        if (temp[k+1] == '\''):
                            Le += '\''
                            j=j+1
                        else:break;
                    # 进行判断
                    if(temp[j+1].isalpha() and G[Le].find('ε')>0):
                        # 当前下一个字符是终结符
                        if (temp[j + 1].islower()):
                            judge = isNote(note, temp, j + 1)
                            if (judge == False):fi.append(temp[j + 1])
                            else: fi.append(temp[j + 1:j + 1 + len(judge)])
                        #当前下一个目标是非终结符
                        else:
                            Le = temp[j + 1]
                            for k in range(j + 1, len(temp)):
                                if (temp[k+1] == '\''):Le += '\''
                                else: break;
                            for s in first[Le]:
                                fi.append(s)
                    else:
                        first[aLe]=fi
                        break;
                # 右部是终结符，直接加入fi
                else:
                    first[aLe] = fi
                    break;
    return first
#求指定文法序列的FIRST集合
def FIRST(str,G,note,first):
    result=[]
    i=-1
    aLe=[]
    while(i<len(str)+1):
        i=i+1
        if(i==len(str)):#k>n
            result.append('ε')
            for s in aLe:
                for ss in first[s]:
                    isexist=False
                    for sss in result:
                      if(sss==ss):
                         isexist=True
                         break;
                    if(isexist==False):result.append(ss)
            return result
        if(str[i].isalpha() and str[i].isupper()):#非终结符
            Le=str[i]
            for k in range(i + 1, len(str)):
                if (str[k] == '\''):
                    Le += '\''
                    i=i+1
                else:break;
            aLe.append(Le)
            if(G[Le].find('ε')==-1):#第一个具有性质ε不属于FIRST（XK）的文法符号
                # result=first[Le]
                for kl in first[Le]:
                    result.append(kl)
                return result
        else:#终结符
            isnote=isNote(note,str,i)
            if(isnote==False):
                result.append(str[i])
                return result
                # if(str[i]=='a'):print("@@@@@@@@@@@@@@")
            else:
             i=i+len(isnote)-1
             result.append(isnote)
    return result
#求非终结符的Follow集合
def CR_Follow(str,G,note,First):
    follow={}
    for ss in range(len(str)):
        Le = re.split(r'::=', str[ss])[0]  # A
        follow[Le]=[]
    S = re.split(r'::=', str[0])[0]  # A

    # follow[S]=['#']


    for i in range(len(str)):

        Le= re.split(r'::=', str[i])[0]  # A

        fl=[]
        if(i==0):fl.append('#')#初态
        for s in str:
          sLe=re.split(r'::=', s)[0]  # A
          Ex = re.split(r'\|', re.split(r'::=', s)[1])  # A->&1|&2....
          for ss in Ex:
           if(len(ss)>0 and ss.find(Le)>=0):
            if( ss.find(Le)==len(ss)-len(Le)):#产生式中B后面没有β

                for k in follow[sLe]:
                    isexist=False
                    for kk in fl:
                        if(kk==k):
                            isexist=True
                            break;
                    if(isexist==False) :

                        if(Le in follow.keys()):

                            fl.append(k)

                        else:
                            fl.append(k)

                            follow[Le]=fl


            else:#αBβ
               #处理E匹配E'的问题
               isexist=False
               index=0
               if(len(Le)==1):
                   for i in range(len(ss)):
                     if(ss[i]==Le  ):
                         if(i==len(ss)-1):
                             isexist=True
                             index=i
                         else:
                             if(ss[i+1]!='\''):
                                 isexist=True
                                 index=i+1
                                 break;




               if(isexist==True):
                resu=FIRST(ss[index:],G,note,First)
                # print("$$",ss[index:],resu,ss,index)
                #查看是否有ε，若有先执行条件三的操作再删去
                # 条件二
                for index in range(len(resu)):
                    if(resu[index]=='ε'):
                        for k in follow[sLe]:
                            isexist = False
                            for kk in fl:
                                if (kk == k):
                                    isexist = True
                                    break;
                            if (isexist == False):
                                if (Le in follow.keys()):#将follow（A）加入follow（B）
                                    fl.append(k)

                                else:
                                    fl.append(k)

                                    follow[Le] = fl

                        # del resu[index]
                        break;
                #将除ε以外的FIRST（β）加入FOLLOW（B)中

                for k in resu:
                  if(k!= 'ε'):
                    isexist = False

                    for kk in fl:
                        if (kk == k):
                            isexist = True
                            break;
                    if (isexist == False):
                        if (Le in follow.keys()):

                            fl.append(k)

                            #follow[Le].append(k)

                        else:
                            fl.append(k)
                            follow[Le] = fl

        follow[Le]=fl
        # print("@@@",follow)

    return  follow

# str=['L::=E;L|ε', "E::=TE'|", "E'::=+TE'|-TE'|ε", "T::=FT'|", "T'::=*FT'|/FT'|modFT'|ε", 'F::=(E)|idc|num']
# G={'L': 'E;L|ε', 'E': "TE'", "E'": "+TE'|-TE'|ε", 'T': "FT'", "T'": "*FT'|/FT'|modFT'|ε", 'F': '(E)|id|num'}
# Note= ['mod', 'id', 'num']
#
# first=CR_FIRST(str,G,Note)
# print(first)
# resu=FIRST("idc",G,Note,first)
# print(resu)
# follow=CR_Follow(str,G,Note,first)
# print(follow)
# table=CR_PATable(first,follow,str,G,Note)
# Drive("(id+id)*id///num;",table,str,Note)
#print(isNote(Note,"id*id",0))

