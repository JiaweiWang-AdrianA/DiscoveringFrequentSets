'''
Frequent Pattern Growth算法，频繁项集算法
'''

from numpy import *
import operator
from dataset import *


class treeNode: # 存储节点信息
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue  # 自身频繁项名字，如‘z'或’x'
        self.count = numOccur  # 此时此刻这个节点被事务经过的次数
        self.nodeLink = None   # 用于保存相似项的实例地址
        self.parent = parentNode # 保存父节点的实例地址
        self.children = {}  # children是以一个嵌套字典，存贮分叉时的实例地址
 
    def inc(self, numOccur): # count计数加上numOccur
        self.count += numOccur
 
    def disp(self, ind=1): # 遍历children属性，打印出子树
        # print(' '*ind,self.name,self.count)
        for child in self.children.values():
            child.disp(ind+1)

def createIniSet(dataSet): # 整理成字典形式
    retDict = {}
    for trans in dataSet:
        if frozenset(trans) not in retDict:
            retDict[frozenset(trans)] = 1
        else:
            retDict[frozenset(trans)] += 1
    #print('retDict:',retDict)
    return retDict
 
def updateHeader(nodeToTest, targetNode): # 找到节点链接的最后一个实例，然后该实例的self.nodeLink保存刚才待被连接的节点实例，相当于节点链接末尾又增了一个节点
    while (nodeToTest.nodeLink != None):  # 如果nodeLink不是空时继续顺着节点链接走，知道找到末尾
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode    # 找到末尾之后，末尾节点的nodeLink保存新的节点实例
 
def updateTree(items,inTree,headerTable,count): # items是每条记录按支持度排好的特征，
    if items[0] in inTree.children:  # 如果这棵子树同一深度有这个键(特征)了，就把其对应的频数加一
        inTree.children[items[0]].inc(count)
    else:    # 如果这棵子树在同一深度没有这个键
        inTree.children[items[0]] = treeNode(items[0],count,inTree) # 就把这个键形成的节点存到这棵子树的children属性中
        if headerTable[items[0]][1] == None: # 如果项目头对应该键的节点指针指向为空
            headerTable[items[0]][1] = inTree.children[items[0]] # 那么把项目头对应该键的节点指针指向该节点，翻译到程序中就是headerTable中该键对应的值的第二位存储该节点的实例地址
        else:  # 如果已经有指向了，就在已有指向的节点的nodeLink属性添加刚才那个节点的信息
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::],inTree.children[items[0]],headerTable,count) # 把该记录整理的特征集合的第一个特征删掉，继续递归
 
def createTree(dataSet,minSup=1):  # 创建树
    headerTable = {}
    for trans in dataSet:      # 每个特征计数
        for item in trans:
            headerTable[item] = headerTable.get(item,0) + dataSet[trans]
    for k in list(headerTable.keys()):     # 把不满足支持度的特征删除
        if headerTable[k] < minSup:
            del headerTable[k]            # headerTable的键是满足支持度的特征，值是支持度
    freqItemSet = set(headerTable.keys()) # 满足支持度的特征的集合，也可以认为是频繁1项集
    if len(freqItemSet) == 0:
        return None,None
    for k in headerTable:  # 改造成真正的项头表格式
        headerTable[k] = [headerTable[k],None]  # headerTable键还是满足支持度的特征，值的第一个位置是具体支持度数，第二个是None
    retTree = treeNode('Null set',1,None)     # 创建树，根是Null set
    for tranSet,count in dataSet.items():     # 从原始事务中取一条事务
        localD = {}
        for item in tranSet:   # 开始对原始事务进行处理，即去除不满足支持度的元素
            if item in freqItemSet: # freqItemSet是满足支持度的特征的元组
                localD[item] = headerTable[item][0]   # 把一条记录的符合支持度的特征及对应的支持度存到自点的键与值中
        if len(localD) > 0:  # 如果此筛选后的事务中有符合条件的元素
            orderedItems = [v[0] for v in sorted(localD.items(),key = operator.itemgetter(1,0),reverse=True)] # orderedItems把每个记录的特征按支持度倒序排列
            # print('orderItems=',orderedItems)
            updateTree(orderedItems,retTree,headerTable,count)
    return retTree,headerTable
 
def ascendTree(leafNode, prefixPath):  # leafNode是节点信息，prefixPath是前缀路径，其实就是条件模式基的列表
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath)  # 如果这个节点还有父亲节点，那么递归
 
def findPrefixPaht(basePat, treeNode):  # basePat节点名称如‘z'或’x',treeNode是headerTable表中存的这个节点的实例
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode,prefixPath)  # prefixPath是一条前缀路径，treeNode是存入headerTable表的这个节点的实例
        if len(prefixPath) > 1: # 因为前缀路径我们不写结尾元素，也就不是不写该节点，所以假如有前缀路径，那么prefixPaht大小一定大于1,等于1说明这个频繁项这条前缀路径是空
            condPats[frozenset(prefixPath[1:])] = treeNode.count # 前缀路径的所有元素的计数值等于这个尾元素的计数值，且把这个频繁项去掉，前缀路径不写结尾元素
        treeNode = treeNode.nodeLink  # 顺着节点链接找到相似项，再查找相似项的前缀路径
    return condPats
 
def getFrequentSet(element,myHeadList,freqItemList):
    freqItemList.append(frozenset((myHeadList[0],element)))
    if len(myHeadList)>1:
        getFrequentSet(element,myHeadList[1:],freqItemList)
 
def mineTree(inTree, headerTable, minSup, preFix,freqItemList): # preFix是set(),freqItem是[]
    bigL = [v[0] for v in headerTable.items()]
    # print('bigL=',bigL)
    for basePat in bigL:
        newFreqSet = preFix.copy() # preFix是set集合，这里用了copy，即newFreqSet的变化不会影响原pareFix
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPaht(basePat,headerTable[basePat][1])  # condPattBases是该值对应的条件模式基
        myCondTree,myHead = createTree(condPattBases,minSup)
        # print('myHead=是条件树的项头表',basePat,myHead)
        if myHead != None:  # myHead是条件树的项头表
            # print('conditional tree for:',newFreqSet)
            myCondTree.disp(1)
            mineTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)
    return freqItemList


def FPGrowth(dataset, minSup):
    initSet = createIniSet(dataset)
    myFptree,myHeaderTab = createTree(initSet,minSup)
    freqItem = []
    if myFptree:
        myFptree.disp()
        freqItem = mineTree(myFptree,myHeaderTab,minSup,set([]),freqItem)
    return freqItem

 
if __name__ == '__main__':
    #simData = loadDataSet()
    dataset = Dataset()
    dataset.datasetGen()
    dataset.printDataset()

    simData = dataset.dataset

    initSet = createIniSet(simData)
    minSup = 3
    myFptree,myHeaderTab = createTree(initSet,minSup)

    if not myFptree:
        print("No freqItem!")
        exit()

    myFptree.disp()
    freqItem = []
    freqItem = mineTree(myFptree,myHeaderTab,minSup,set([]),freqItem)
    print(freqItem)