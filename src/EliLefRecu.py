#!/usr/bin/python
# -*- coding: UTF-8 -*-
import  re
#消除直接左递归
def EliStrLefRec(aile,aiEx,str,index):
    # 第一个字符是本非终结符的集合
    Aa=[]
    # 第一个字符不是本非终结符的集合
    b=[]
    for i in range(len(aiEx)):
        for s in re.split(r'\|',aiEx[i]):
            #以A开头的
          if(len(s)>0):
            if(s.find(aile)==0):
                s=s.replace(aile,"",1)
                Aa.append(s)
            else:
                if(s=='ε'):s=''
                b.append(s)
    if(len(Aa)==0):#没有找到直接左递归的式子
        return 0
    #("Aa==:",Aa)
    A=aile+'::='#A->
    A_=aile+'\''+'::='#A'->
    for s in b:
        A+=s+aile+'\''+'|'
    for s in Aa:
        A_+=s+aile+'\''+'|'
    A_+='ε'
    del str[index]
    str.insert(index,A_)
    str.insert(index,A)
# 替换
def replace(ai,aj,str,index):
        ajLe = re.split(r'::=',aj)[0]#Aj
        ajEx = re.split(r'\|', re.split(r'::=',aj)[1])#Aj->&1|&2....
        aiLe = re.split(r'::=',ai)[0]#Ai
        aiEx = re.split(r'\|', re.split(r'::=',ai)[1])#Ai->&1|&2....
        for i in range(len(aiEx)):
               temp=""
               if(aiEx[i].find(ajLe)==0): #形如 Ai->Ajr
                temp=aiEx[i][len(ajLe):]#取r
               if(len(temp)==0):
                   continue#如果没有找到形如Ai->Ajr的式子
               else:#可以替换
                aiEx[i]=""
                for j in range(len(ajEx)):
                    aiEx[i]+=ajEx[j]+temp+"|"
        EliStrLefRec(aiLe,aiEx,str,index);#消除直接左递归
def EliLefRec(str):
       print("消除左递归")
       # 先消除第一个表达式可能存在的直接左递归
       aiLe = re.split(r'::=', str[0])[0]  # Ai
       aiEx = re.split(r'\|', re.split(r'::=', str[0])[1])  # Ai->&1|&2....
       EliStrLefRec(aiLe, aiEx, str, 0)
       i=1;
       #print(str)
       while (i<len(str)):
        for j in range(0,i):
          #消除递归
          #print("i=",i)
          #print(str[i]+"   @@@@@@@"+str[j])
          replace(str[i],str[j],str,i)
        i = i + 1

       return str;
# str=['S::=SaP|Sf|P', 'P::=qbP|q']
# EliLefRec(str)
# print(str)