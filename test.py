from Apriori import *
from FPGrowth import * 
from IIA import *
from dataset import * 
import time

def test(dataset, minSup):

    # Apriori
    startTime = time.time()
    aprioriFreqItem = Apriori(dataset, minSup)
    endTime = time.time()
    aprioriTime = endTime - startTime

    # FPGrowth
    startTime = time.time()
    FPGrowthFreqItem = FPGrowth(dataset, minSup)
    endTime = time.time()
    FPGrowthTime = endTime - startTime

    #test
    startTime = time.time()
    IIAmaxFreqItemsList, IIAmaxFreqItemsDict = IIA(dataset, minSup)
    endTime = time.time()
    IIATime = endTime - startTime
    

    # # print Test result
    # # 1. print frequent items
    # # Apriori
    # print("Apriori result: ")
    # for fi in aprioriFreqItem:
    #     print(set(fi), end=",")
    # print("\n")
    # # FPGrowth
    # print("FPGrowth result: ")
    # for fi in FPGrowthFreqItem:
    #     print(fi, end=",")
    # print("\n")
    # # IIA
    # print("FPGrowth result: ")
    # for fi in IIAmaxFreqItemsList:
    #     print(fi, end=",")
    # print("\n")

    # # 2. print running time
    # print("Apriori : %.6f s" % aprioriTime, end="\t")
    # print("FPGrowth: %.6f s" % FPGrowthTime, end="\t")
    # print("IIA     : %.4f s" % IIATime)

    
    return aprioriTime, FPGrowthTime, IIATime

 

if __name__ == '__main__':
    test_num = 10

    t_num_testList = [100]
    item_num_testList = [50]
    items_num_max_testList = [25]
    minSup_testList = [10,20]

    for t_num in t_num_testList:
        for item_num in item_num_testList:
            #items_num_max_testList = [ int(item_num/2) ]
            for items_num_max in items_num_max_testList:
                print("[ t_num: %5d," % t_num, end=" ")
                print("item_num: %5d," % item_num, end=" ")
                print("items_num_max: %5d ]" % items_num_max)
                dataset = Dataset(t_num, item_num, items_num_max)
                dataset.datasetGen()
                #dataset.printDataset()

                for minSup in minSup_testList:
                    print("* minSup: %d" % minSup)
                    aTimeSum, fTimeSum, iiaTimeSum = 0, 0, 0
                    for i in range(0,test_num):
                        aTime, fTime, iiaTime = test(dataset.dataset, minSup)
                        aTimeSum += aTime
                        fTimeSum += fTime
                        iiaTimeSum += iiaTime

                    print("Apriori : %.4f s" % (aTimeSum/test_num), end="\t")
                    print("FPGrowth: %.4f s" % (fTimeSum/test_num), end="\t")
                    print("IIA     : %.4f s" % (iiaTimeSum/test_num))
                        






