import os
import time
import numpy as np
_startTime = time.time()
_filename :str
_matris_length:int

class KnapsackItem:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
    def __repr__(self):
        return "Item(weight={}, value={})".format(self.weight, self.value)

class Knapsack:
    def __init__(self, capacity=None):
        self.capacity = capacity
        self.items = []
        self.answers = None
        self.table=None
    def  file_to_knapsack(_filename:str):
        knapsack = Knapsack()
        with open(_filename, 'r') as f:
            knapsack.capacity = int(f.readline().split()[1])
            for line in f:
                value, weight = [int(x) for x in line.split()]
                knapsack.add_item(KnapsackItem(weight, value))
        return knapsack
    
    def answer(self):
        solution = self.solve()
        return [1 if item in solution else 0 for item in self.items]

    def add_item(self, item):
        self.items.append(item)
    def __repr__(self):
        return "Knapsack(capacity={}, items={})".format(self.capacity, self.items)
    def get_optimal_value(self):
        if self.table is None:
            table = [[0 for _ in range(self.capacity+1)] for _ in range(_matris_length+1)]
            
            # Fill the table
            for i in range(0, len(self.items)):
                temp_i=i%_matris_length+1
                for w in range(1, self.capacity + 1):
                    if self.items[i].weight > w:
                        table[temp_i][w] = table[temp_i - 1][w]
                    else:
                        table[temp_i][w] = max(table[temp_i - 1][w], table[temp_i - 1][w - self.items[i].weight] + self.items[i].value)
                
                if temp_i == _matris_length and i!=len(self.items)-1:
                    
                    table_to_file(table, i)
                    for j in range(0, len(table[0])):
                        table[0][j] = table[-1][j]
                    
                if i==len(self.items)-1:
                    table_to_file(table,i)
            self.table = table
        return np.max(self.table)
    def solve(self):
        if self.answers is None:
            self.get_optimal_value()
            table=self.table
            
            solution = []
            i = len(self.items)-1
            
            w = self.capacity
            while i >= 0 and w > 0:
                temp_i=(i%_matris_length)+1
                if temp_i == _matris_length and i!=len(self.items):
                    table=file_to_table(i,len(table[0]))
                    
                if table[temp_i][w] != table[temp_i - 1][w]:
                    solution.append(self.items[i])
                    w -= self.items[i].weight
                i -= 1
            self.answers = solution
        return self.answers
def matris_copy_from_matis(matris1, matris2):
    for i in range(len(matris1),len(matris1)-2):
        for j in range(len(matris1[0])):
            matris1[i+2][j]=matris2[i][j]
def table_to_file(table, i):
    file = "./storage_"+_filename+"/" + str(i)
    os.makedirs(os.path.dirname(file), exist_ok=True)
    
    with open(file, 'w') as f:
        for row in table:
            f.write("".join([str(x)+" " if x!=0 else "" for x in row]) + "\n")
def file_to_table(i,l)->list:
    file = "./storage_"+_filename+"/" + str(i)
    with open(file, 'r') as f:
        table = []
        for line in f:
            lines = line.split()
            append_list = [0]*(l-len(lines))
            append_list.extend([x for x in lines])
            table.append(append_list)
    os.remove(file)
    return table
def Solve(filename: str, matris_length: int=100):
    global _filename, _matris_length
    _filename=filename
    _matris_length=matris_length
    knapsack = Knapsack.file_to_knapsack(_filename)
    optimal_value=knapsack.get_optimal_value()
    print(optimal_value)
    answer = knapsack.answer()
    print(knapsack.solve())
    print("--- %s saniye ---" % (time.time() - _startTime))
    os.makedirs("output", exist_ok=True)
    os.rmdir("./storage_"+_filename)
    with open("output/"+_filename+"_output", 'w') as f:
        f.write("{}\n".format(optimal_value))
        f.write(str(answer))