'''
Created on 03.12.2017

--- Day 3: No Matter How You Slice It ---
'''

import unittest


class Test(unittest.TestCase):
    testinput = ("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2")
    def testLicenseFile(self):   
        self.assertEqual(solve(self.testinput), 138)
        
    def testSecondStrategy(self):   
        self.assertEqual(solvePartTwo(self.testinput), 66)

def solve(license_file):
    tree = list(map(int, license_file.split()))
    sum_meta_data = 0
    while len(tree)>0:
        pos_meta_data = tree.index(0)+2
        num_meta_data = tree[pos_meta_data-1]
        sum_meta_data += sum(tree[pos_meta_data:pos_meta_data+num_meta_data])
        #remove current node from parent and then from the list
        tree[pos_meta_data-4] -= 1
        del tree[pos_meta_data-2:pos_meta_data+num_meta_data]
    return sum_meta_data

class LicenseNode():
    def __init__(self,meta_data):
        self.child_nodes = list()
        self.meta_data = meta_data
        
    def __repr__(self):
        return "<meta_data: %s>" % self.meta_data        
    
    def get_value(self):
        if len(self.child_nodes)==0:
            return sum(self.meta_data)
        else:
            sum_child_nodes=0
            for child_idx in self.meta_data:
                if child_idx==0 or child_idx>len(self.child_nodes):
                    continue
                sum_child_nodes += self.child_nodes[child_idx-1].get_value()
            return sum_child_nodes
        
def generate_child_nodes(entries):
    i=0
    nodes=dict()
    parents=list()
    while len(entries)>0:        
        num_children = entries[0]
        num_meta_data = entries[1]
        if num_meta_data==0:
            print("error")
        del entries[:2]
        if num_children!=0:
            nodes[i]=LicenseNode(entries[-num_meta_data:])
            del entries[-num_meta_data:]
        else:            
            nodes[i]=LicenseNode(entries[:num_meta_data])
            del entries[:num_meta_data]
        
        if len(parents)>0:
            nodes[parents[-1]].child_nodes.append(nodes[i])
            del parents[-1]
        
        if num_children != 0:
            parents.extend([i for j in range(num_children)])
            
        i += 1
    return nodes[0]

    

def solvePartTwo(license_file):
    tree = list(map(int, license_file.split()))
    license_tree = generate_child_nodes(tree)
    return license_tree.get_value()

if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read()
        print(solve(puzzleInput))
        print(solvePartTwo(puzzleInput))

    