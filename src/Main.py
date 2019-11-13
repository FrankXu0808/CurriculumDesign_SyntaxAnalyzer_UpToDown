#!/usr/bin/python
# -*- coding: UTF-8 -*-
import EliLefRecu
import LeftFactoring
import re
import CR_PredictiveAnalysisTable
import SyntaxTree

Gs=[['E::=E+T|T', 'T::=T*F|F',  'F::=(E)|-F|id'],
 ['S::=aABe',  'A::=b|Abc' , 'B::=d']]
# markFlow = "(id+id)*id+id/"
markFlow = "abbcde"
#读取文法G，得到文法的描述
for fo in Gs:
    # fo = open("G.txt", "r+")
    # str = fo.readlines()
    str=fo
    for i in range(0,len(str)):
        str[i]=str[i].replace('\n','')
        str[i] = str[i].replace('!', 'ε')
    print ("读取的文法是 : ", str)

    fnote=open("Note.txt","r+")
    note=fnote.readlines()
    for i in range(0,len(note)):
        note[i]=note[i].replace('\n','')
    print ("多个字符作为一个终结符的是 : ", note)
    # 关闭打开的文件

    # fo.close()
    fnote.close()

    #消除左递归

    EliLefRecu.EliLefRec(str);
    for s in str:
        print(s)

    #消除左因子
    LeftFactoring.left_factoring(str)
    print("消除左因子后:")
    for s in str:
        print(s)
    #将list改为字典
    G={}
    for s in str:
        aLe = re.split(r'::=', s)[0]  # Aj
        aEx = re.split(r'::=', s)[1]
        G[aLe]=aEx
    #print(G)
    #输入记号流

    print("输入的记号流:",markFlow)
    first=CR_PredictiveAnalysisTable.CR_FIRST(str,G,note)
    print("FIRST集合:")
    for s in first:
        print("FIRST(", s, "):", first[s])
    #resu=CR_PredictiveAnalysisTable.FIRST("",G,note,first)

    #print(resu)
    follow=CR_PredictiveAnalysisTable.CR_Follow(str,G,note,first)
    print("FOLLOW集合:")
    for s in follow:
        print("FOLLOW(",s,"):",follow[s])
    print("预测分析表:")
    table=CR_PredictiveAnalysisTable.CR_PATable(first,follow,str,G,note)
    print("驱动器算法:")
    result=CR_PredictiveAnalysisTable.Drive(markFlow,table,str,note)
    if(result==1):
        print("符合语法！")
        break
    else:
        print("该文法不匹配本记号流!")
    print()
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print()
