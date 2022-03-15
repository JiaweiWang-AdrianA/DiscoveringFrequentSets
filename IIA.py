'''
IIA算法，求最大频繁项集算法
'''

from numpy import *
import operator
from dataset import * 

global maxFreqItemsDict

class TNode: # 存储事务T的信息
    def __init__(self, Tid, items, count):
        self.Tid = Tid
        self.items = items
        self.count = count
    def __str__(self):
        string = "<Tid:" + str(self.Tid) + ", "
        string += "items:" + str(self.items) + ", "
        string += "count:" + str(self.count) + ">"
        return string

def reduceDataset(dataset, minSup):
    """ 
        从数据集中排除非频繁的项目
        args: 原始数据集dataset, 最小支持数minSup
        return:仅包含频繁项目的数据集redDataset
    """
    freqItem, nofreqItem = [], []
    t_num = len(dataset)
    redDataset = []
    # 从每个事务中排除非频繁项目
    for i in range(0, t_num):
        T_i, items_num  = dataset[i], len(dataset[i])
        T_red = []
        # 确认事务T对应的项集的每个项目是否属于频繁项目
        for u in T_i:
            if u in freqItem:
                T_red.append(u)
            elif u in nofreqItem:
                continue
            else:
                count = 1
                for T_j in dataset[i+1:]:
                    if u in T_j: 
                        count += 1
                        if count >= minSup:
                            freqItem.append(u)
                            T_red.append(u)
                            break
                nofreqItem.append(u)
        # 将排除非频繁项目后的事务加入结果数据集redDataset中
        if T_red:
            redDataset.append(T_red)
    return redDataset

def getOrdDatasetFromDataset(dataset):
    """
        按事务对应的项集大小整理dataset
        得到字典ordDict: {长度: [T_i,...] } 和字典countDict:{T_1:T_1出现的次数, ...}
        按项集大小由大到小排列的有序数据集ordDataset:[ Tnode_1, Tnode_2 ...]
    """
    # 获取字典ordDict,countDict
    ordDict, countDict = {}, {}
    for T in dataset:
        item_num = len(T)
        if item_num not in ordDict:
            ordDict[item_num] = [T]
        else:
            ordDict[item_num].append(T)
        if tuple(T) not in countDict:
            countDict[tuple(T)] = 1
        else:
            countDict[tuple(T)] += 1

    # 根据字典ordDict和countDict获得有序数据集ordDataset
    ordDataset, Tid_count = [], 0
    for item_num in sorted(ordDict, reverse=True):
        for T in ordDict[item_num]:
            if tuple(T) in countDict:
                tnode = TNode(Tid_count, T, countDict[tuple(T)])
                ordDataset.append(tnode)
                Tid_count += 1
                countDict.pop(tuple(T))
    # print("ordDataset:")
    # for tnode in ordDataset: print(tnode)
    return ordDataset

def getOrdDatasetFromD1(D1):
    """
        按事务对应的项集大小整理D1
        得到字典ordDict: {长度: [T_i,...] } 和字典countDict:{T_1:T_1出现的次数, ...}
        按项集大小由大到小排列的有序数据集ordDataset:[ Tnode_1, Tnode_2 ...]
    """
    # 获取字典ordDict,countDict
    ordDict, countDict = {}, {}
    for tnode in D1:
        item_num = len(tnode.items)
        if item_num not in ordDict:
            ordDict[item_num] = [tnode]
        else:
            ordDict[item_num].append(tnode)
        if tuple(tnode.items) not in countDict:
            countDict[tuple(tnode.items)] = tnode.count
        else:
            countDict[tuple(tnode.items)] += tnode.count

    # 根据字典ordDict和countDict获得有序数据集ordDataset
    ordDataset, Tid_count = [], 0
    for item_num in sorted(ordDict, reverse=True):
        for tnode in ordDict[item_num]:
            if tuple(tnode.items) in countDict:
                tnode = TNode(Tid_count, tnode.items, countDict[tuple(tnode.items)])
                ordDataset.append(tnode)
                Tid_count += 1
                countDict.pop(tuple(tnode.items))
    # print("ordD1:")
    # for tnode in ordDataset: print(tnode)
    return ordDataset


def getMaxFreqItemLen(maxFreqItemsDict):
    """ maxFreqItemsDict中的最大频繁项集的长度"""
    if len(maxFreqItemsDict) > 0:
        maxlen = sorted(maxFreqItemsDict.keys(),reverse=True)[0]
    else:
        maxlen = 0
    return maxlen

def FindMFS(D1, minSup, ord_flag):
    global maxFreqItemsDict
    
    if not D1:
        return

    # 按序整理字典D1:[ Tnode_1, Tnode_2 ...]
    if ord_flag:
        ordD1 = getOrdDatasetFromD1(D1)
    else:
        ordD1 = D1

    # 对D1中的每个事务Tnode_i进行迭代取交集处理,直至遍历至前len(D1)-minSup+1条记录
    for i in range(0, len(ordD1)-minSup+1):
        # print("i:", i)
        # print("ordD1:")
        # for tnode in ordD1:  print(tnode)

        # 若i已经遍历至D1了前len(D1)-minSup条记录，则返回
        if i >= len(ordD1):
            return

        # 若Tnode_i的项集长度已经小于现最大频率项集的长度,则返回
        if len(ordD1[i].items) < getMaxFreqItemLen(maxFreqItemsDict):
            return

        # 若ordD1[i].count不小于最小支持数且长度大于等于现最大频繁项集长度,则直接将超过最小支持数且长度相同的前i项存入maxFreqItemsDict并返回
        maxFreqItemLen = getMaxFreqItemLen(maxFreqItemsDict)
        tnode = ordD1[i]
        maxOrdD1ItemLen = len(tnode.items)
        if tnode.count >= minSup and maxOrdD1ItemLen >= maxFreqItemLen:
            if maxOrdD1ItemLen not in maxFreqItemsDict:
                maxFreqItemsDict[maxOrdD1ItemLen] = [ tnode.items ]
            elif tnode.items not in maxFreqItemsDict[maxOrdD1ItemLen]:
                maxFreqItemsDict[maxOrdD1ItemLen].append( tnode.items )
            # 若tnode.count已经超过最小支持数且长度与maxFreqItemLen相同,则存入maxFreqItemsDict
            for tnode in ordD1[i+1:]:
                if tnode.count >= minSup and len(tnode.items) == maxOrdD1ItemLen and tnode.items not in maxFreqItemsDict[maxOrdD1ItemLen]:
                    maxFreqItemsDict[maxOrdD1ItemLen].append(tnode.items)
            # print("!!!!update:", maxFreqItemsDict)
            return


        # 事务Tnode_i进行取交集处理得到D2
        T_i, j = ordD1[i].items, i + 1
        D2, D2_Tid_count = [], 0
        while j<len(ordD1):
            T_j = ordD1[j].items
            T_inter = sorted(list(set(T_i).intersection(set(T_j))))
            if T_inter: 
                tnode = TNode(D2_Tid_count, T_inter, ordD1[j].count+1)
                D2.append(tnode)
                D2_Tid_count += 1
            if not list(set(T_j).difference(set(T_i))):
                ordD1.remove(ordD1[j])
                j -= 1
            j += 1
        # print("D2:")
        # for tnode in D2: print(tnode)

        # 复制D2至D2_temp,对D2_temp中的事务进行移入maxFreqItemsDict和剔除处理
        D2_temp = D2.copy()
        # D2_temp = getOrdDatasetFromD1(D2_temp) # 整理D2_temp
        # print("D2_temp:")
        # for tnode in D2_temp: print(tnode)
        for k in range(0, len(D2)):
            T_k = D2[k].items

            # 若T_k的长度>=最小支持数, 则从D2_temp中删除T_k及其后续子集
            if D2[k].count >= minSup:
                # 若T_k的长度>=现最大频率项集的长度, 则将其存入maxFreqItemsDict
                if len(T_k) >= getMaxFreqItemLen(maxFreqItemsDict):
                    if len(T_k) in maxFreqItemsDict:
                        maxFreqItemsDict[len(T_k)].append(T_k)
                    else:
                        maxFreqItemsDict[len(T_k)] = [T_k]
                    # print("update:", maxFreqItemsDict)

                if D2[k] in D2_temp:
                    D2_temp.remove(D2[k])
                for l in range(k+1, len(D2)):
                    T_l = D2[l].items
                    if not list(set(T_l).difference(set(T_k))) and D2[l] in D2_temp:
                        D2_temp.remove(D2[l])
        # print("D2_temp:")
        # for tnode in D2_temp: print(tnode)
        
        # 处理后的D2_temp长度>=minSup时,将D2_temp作为D1进行迭代取交集处理 ; 否则继续遍历D1
        if len(D2_temp) >= minSup:
            FindMFS(D2_temp, minSup, 1)


def IIA(dataset, minSup):
    global maxFreqItemsDict
    maxFreqItemsDict = {}

    # 缩减原始数据集dataset得到缩减数据集redDataset
    redDataset = reduceDataset(dataset, minSup)

    # 将缩减数据集redDataset整理成有序数据集D1
    D1 = getOrdDatasetFromDataset(redDataset)
    # print("ordDataset:")
    # for tnode in D1: print(tnode)

    # 迭代交集获得最大频繁项集字典maxFreqItemsDict
    # 无需重新排序D1, ord_flag=0
    FindMFS(D1, minSup, 0) 
    
    # 由最大频繁项集字典maxFreqItemsDict得到最大频繁项集列表maxFreqItemsList
    maxFreqItemsLen = getMaxFreqItemLen(maxFreqItemsDict)
    maxFreqItemsList = []
    if maxFreqItemsLen>0:
        for maxFreqItem in maxFreqItemsDict[maxFreqItemsLen]:
            maxFreqItemsList.append(tuple(maxFreqItem))
        maxFreqItemsList = sorted(list(set(maxFreqItemsList)))
    # print("maxFreqItemsDict:", maxFreqItemsDict)
    # print("maxFreqItemsList:", maxFreqItemsList)
    return maxFreqItemsList, maxFreqItemsDict
    
 
if __name__ == '__main__':
    minSup = 4
    global maxFreqItemsDict
    maxFreqItemsDict = {}

    for t_num in [20]:
        for item_num in [10]:
            for items_num_max in [5]:
                #print("[ t_num: %5d," % t_num, end=" ")
                #print("item_num: %5d," % item_num, end=" ")
                #print("items_num_max: %5d ]" % items_num_max)
                #dataset = Dataset(t_num, item_num, items_num_max)
                dataset = Dataset()
                datas = [[1, 5, 6, 7, 8], [0, 1, 3, 9], [1, 3, 4, 8], [9], [1, 3, 8], [1], [3, 4], [6, 7, 8], [0, 1, 2, 3], [1, 3, 4, 5], [3, 5, 8], [0, 1, 5, 6], [0, 2, 6], [1, 2, 4, 6, 8], [2, 3], [2, 6, 7], [2], [0, 4, 5], [0, 4, 6, 7, 9], [0, 2, 3, 6, 9]]
                #datas = [ [2,7], [2,7], [2,7], [2,4], [2,4], [2,4], [4], [4] ]
                dataset.datasetGen(datas)
                #dataset.printDataset()
                print(dataset.dataset)

                #test
                maxFreqItemsList, maxFreqItemsDict = IIA(dataset.dataset, minSup)
                print("maxFreqItemsDict:", maxFreqItemsDict)
                print("maxFreqItemsList:", maxFreqItemsList)
                

    