'''
生成随机测试数据集dataset:
    参数: 
        事务数: t_num;
        项目数: item_num;
        每个事务对应的项集个数最大值: items_num_max;
    规则:
        一共有item_num个项目:[0,1, 2, ..., item_num-1]
        数据集dataset包含t_num个事务T: dataset = [T_0, T_1, ..., T_t_num-1]
        每个事务T的项集items包含items_num个项: T_i = [u_1, u_2, ..., u_items_num] (0<=i<t_num and 1<=items_num<=items_num_max)
        即, 随机生成事务T_i的项集T_i's items (items按序排列):
            T_i's items_num = random.randint(1, self.items_max_num) 
            T_i's items = sorted( random.sample(range(0, self.item_num), items_num) )

    示例:
        item_num = 5, t_num = 4, items_num_max = 5
        dataset = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
            T_1 = [1, 3, 4] (items_num:3)
            T_2 = [2, 3, 5] (items_num:3)
            T_3 = [1, 2, 3, 5] (items_num:4)
            T_4 = [2, 5] (items_num:2)
'''
import random

class Dataset():

    def __init__(self, t_num=3, item_num=5, items_num_max=4, dataset=None):
        self.t_num = t_num
        self.item_num = item_num
        self.items_num_max = items_num_max
        self.dataset = dataset

        
    def datasetGen(self, dataset=None):
        if dataset:
            self.dataset = dataset
        else:
            dataset = []
            for t in range(0, self.t_num):
                items_num = random.randint(1, self.items_num_max)
                items = random.sample(range(0, self.item_num), items_num)
                dataset.append( sorted(items) )
            self.dataset = dataset

    def printDataset(self):
        for T_id in range(0, len(self.dataset)):
            print(str(T_id) + "\t" + str(self.dataset[T_id]))


    

if __name__ == '__main__':
    # test1
    # datas = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]] 
    # dataset = Dataset(dataset=datas)
    # test2
    dataset = Dataset(t_num=10, item_num=5, items_num_max=4)
    dataset.datasetGen()

    dataset.printDataset()