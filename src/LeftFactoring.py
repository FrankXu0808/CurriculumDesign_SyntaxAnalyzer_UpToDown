#!/usr/bin/python
# -*- coding: UTF-8 -*-
import  re
def Common_prefix(str):  # 产生式的公共前缀
    cpLen = 0;
    cp=''
    for i in range(len(str) - 1):
        for j in range(i + 1, len(str)):
            for k in range(0, min(len(str[i]),len(str[j]))):
                if (str[i][k] == str[j][k]):
                    if (k + 1 > cpLen):
                        cpLen = cpLen + 1
                        cp = str[i][0:k + 1]

                else:break
    return cp


def left_factoring(str):#消除左因子
    i=0
    while(i<len(str)):
        aLe = re.split(r'::=', str[i])[0]  # A
        aEx = re.split(r'\|', re.split(r'::=', str[i])[1])  # A->&1|&2....
        # print("aEx:",aEx)
        CommonPrefix=Common_prefix(aEx)#求得产生式A的最长公共前缀
        # print(CommonPrefix)
        if(CommonPrefix==''):#本表达式没有公共前缀
            i=i+1
            continue
        r=[]
        b=[]
        for s in aEx:
            if(s.find(CommonPrefix)==0):
                s=s.replace(CommonPrefix,'',1)
                if(len(s)==0):s='ε'
                b.append(s)
            else:
                r.append(s)
        A=aLe+"::="+CommonPrefix+aLe+'\''+'|'
        A_=aLe+'\''+"::="
        for s in r:
            A+=s+'|'
        for s in b:
            A_+=s+'|'
        del str[i]
        # print("@@",A_,A)
        str.insert(i,A_)
        str.insert(i,A)
        # print("str",str)
    return  str

# str=['S::=SaP|Sf|P', 'P::=qbP|q']
#
# print(Common_prefix(["aPS'","fS'","ε"]))