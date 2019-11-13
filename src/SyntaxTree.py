import random
import re
class nodes:

    def __init__(self, data):
        self._data = data
        self._children = []

    def getdata(self):
        return self._data

    def getchildren(self):
        return self._children

    def add(self, node):

            self._children.append(node)

    def go(self, data):
        for child in self._children:
            if child.getdata() == data:
                return child
        return None


class tree:

    def __init__(self,node):
        self._head = node
    def gethead(self):
        return self._head


    def insert(self, path, data):
        cur = self._head
        for step in path:
            if cur.go(step) == None:
                return False
            else:
                cur = cur.go(step)
        cur.add(node(data))
        return True

    def search(self, path):
        cur = self._head
        for step in path:
            if cur.go(step) == None:
                return None
            else:
                cur = cur.go(step)
        return cur
    def printSpace(self,count):
        for i in range(count):
            print("  ",end="")
    def PrintByLevel(self,counts):
        count=counts
        level={}
        level["start"]=self.gethead()
        isend=False

        while(isend==False):
            temp={}
            nochildindex=-1;
            index=-1

            self.printSpace(count)
            for n in level:

             if(isinstance(level[n],str)==True):print(level[n],end="")
             else:
                index = index + 1
                print(level[n].getdata(),"(",re.split(r' ',n)[0],")       ",end="")
                if(len(level[n].getchildren())>0):

                    if(nochildindex==-1):nochildindex=index
                    for s in level[n].getchildren():
                        temp[level[n].getdata()+" "+str(random.random())]=s
                        #print("$$$",s.getdata(), end="")
                        temp[random.random()]=" "
                    if(len(level[n].getchildren())<=2) :count=count-1
                    elif(len(level[n].getchildren())>2) :count=count-2
            if(nochildindex>0):count+=nochildindex*6
            level=temp
            print()
            print()
            if(len(level)==0): isend=True

    def LeftSearchPrint(self):
        stack=[]#结点栈
        indexStack=[]#坐标栈
        stack.append(self.gethead())
        indexStack.append(0)
        temp=self.gethead()
        while(len(stack)>0):


            if(len(temp.getchildren())>0 and len(temp.getchildren())>indexStack[-1]):#非叶子结点
                index=indexStack[-1]
                stack.append(temp.getchildren()[index])

                indexStack.append(0)
            else:
                print(temp.getdata()," ",end="")
                stack.pop()
                indexStack.pop()
                if(len(indexStack)>0):
                 indexStack[-1]= indexStack[-1]+1
            if(len(stack)>0):
             temp=stack[-1]
        print()

# a=nodes("L")
# b=nodes("E")
# a.add(b)
# c=nodes(";")
# a.add(c)
# d=nodes("L")
# a.add(d)
# null=nodes("!")
# d.add(null)
#
# t=nodes("T")
# b.add(t)
# f=nodes("F")
# t.add(f)
# id=nodes("id")
# f.add(id)
#
# ee=nodes("E'")
# b.add(ee)
# adds=nodes("+")
# ee.add(adds)
#
# T=tree(a)
#print(len(b.getchildren()))
#T.LeftSearchPrint()
#T.PrintByLevel(30)






