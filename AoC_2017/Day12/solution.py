'''
Created on 01.12.2017

--- Day 12: Digital Plumber ---

You walk through the village and record the ID of each program and the IDs with which it can communicate directly (your puzzle input). Each program has one or more programs with which it can communicate, and these pipes are bidirectional; if 8 says it can communicate with 11, then 11 will say it can communicate with 8.

You need to figure out how many programs are in the group that contains program ID 0.

For example, suppose you go door-to-door like a travelling salesman and record the following list:

0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5

In this example, the following programs are in the group that contains program ID 0:

    Program 0 by definition.
    Program 2, directly connected to program 0.
    Program 3 via program 2.
    Program 4 via program 2.
    Program 5 via programs 6, then 4, then 2.
    Program 6 via programs 4, then 2.

Therefore, a total of 6 programs are in this group; all but program 1, which has a pipe that connects it to itself.

How many programs are in the group that contains program ID 0?

--- Part Two ---

There are more programs than just the ones in the group containing program ID 0. The rest of them have no way of reaching that group, and still might have no way of reaching each other.

A group is a collection of programs that can all communicate via pipes either directly or indirectly. The programs you identified just a moment ago are all part of the same group. Now, they would like you to determine the total number of groups.

In the example above, there were 2 groups: one consisting of programs 0,2,3,4,5,6, and the other consisting solely of program 1.

How many groups are there in total?

'''
import unittest


class Test(unittest.TestCase):
    def testCommunication(self):
        test_data ='0 <-> 2\n1 <-> 1\n2 <-> 0, 3, 4\n3 <-> 2, 4\n4 <-> 2, 3, 6\n5 <-> 6\n6 <-> 4, 5'
        self.assertEqual(solve(test_data), 6)

def solve(input_list):
    communication_dict = dict()
    for item in input_list.split('\n'):
        prog_ID, connections = item.split(' <-> ')
        communication_dict[prog_ID] = connections.split(', ')
    connections_to_check = ['0']
    programs_contain_id = []
    while len(connections_to_check) > 0:
        check_program = connections_to_check.pop(0)
        if check_program not in programs_contain_id:
            programs_contain_id.append(check_program)
            connections_to_check.extend(communication_dict[check_program]) 
    return len(programs_contain_id)

def solvePartTwo(input_list):
    communication_dict = dict()
    groups_to_check = list()
    actual_groups = list()
    for item in input_list.split('\n'):
        prog_ID, connections = item.split(' <-> ')
        communication_dict[prog_ID] = connections.split(', ')
        groups_to_check.append(prog_ID)
        
    while len(groups_to_check) > 0:
        connections_to_check = [groups_to_check[0]]
        programs_contain_id = list()
        while len(connections_to_check) > 0:
            check_program = connections_to_check.pop(0)
            if check_program not in programs_contain_id:
                programs_contain_id.append(check_program)
                connections_to_check.extend(communication_dict[check_program])
        actual_groups.append(programs_contain_id)
        groups_to_check = list(set(groups_to_check) - set(programs_contain_id))
    return len(actual_groups)
                
            
enableUnitTest = False

if __name__ == "__main__":
    if enableUnitTest:
        unittest.main()
    else:
        with open("input.txt",'r') as inFile:
            puzzleInput = inFile.read().rstrip()        
            print solve(puzzleInput)
            print solvePartTwo(puzzleInput)
    