'''
Created on 03.12.2017

--- Day 3: No Matter How You Slice It ---
'''

import unittest
from datetime import datetime
import numpy as np
import operator

class Test(unittest.TestCase):
    testinput = ("[1518-11-01 00:00] Guard #10 begins shift\n"
                     "[1518-11-01 00:05] falls asleep\n"
                     "[1518-11-01 00:25] wakes up\n"
                     "[1518-11-01 00:30] falls asleep\n"
                     "[1518-11-01 00:55] wakes up\n"
                     "[1518-11-01 23:58] Guard #99 begins shift\n"
                     "[1518-11-02 00:40] falls asleep\n"
                     "[1518-11-02 00:50] wakes up\n"
                     "[1518-11-03 00:05] Guard #10 begins shift\n"
                     "[1518-11-03 00:24] falls asleep\n"
                     "[1518-11-03 00:29] wakes up\n"
                     "[1518-11-04 00:02] Guard #99 begins shift\n"
                     "[1518-11-04 00:36] falls asleep\n"
                     "[1518-11-04 00:46] wakes up\n"
                     "[1518-11-05 00:03] Guard #99 begins shift\n"
                     "[1518-11-05 00:45] falls asleep\n"
                     "[1518-11-05 00:55] wakes up\n")
    def testFirstStrategy(self):   
        self.assertEqual(solve(self.testinput), 240)
        
    def testSecondStrategy(self):   
        self.assertEqual(solvePartTwo(self.testinput), 4455)
    

def generateGuardDict(timetable):
    activity_list = list()
    for note in timetable.split('\n'):
        if len(note) > 0:
            timestamp = note[1:17]
            text = note[19:]
            activity_list.append([datetime.strptime(timestamp, '%Y-%m-%d %H:%M'), text])
    
    activity_list.sort()
    guard_dict = dict()
    for timestamp, text in activity_list:
        if '#' in text:
            guard_id = text.split()[1][1:]
            if guard_id not in guard_dict.keys():
                guard_dict[guard_id] = np.zeros(60, dtype=np.uint16)
        elif text[0] == 'f':
            start = timestamp.minute
        else:
            end = timestamp.minute
            guard_dict[guard_id][start:end] += 1
    
    return guard_dict

def solve(timetable):
    guard_dict = generateGuardDict(timetable)
    most_minutes_asleep = max(guard_dict, key=lambda key:sum(guard_dict[key]))
    minute_spend_asleep_most = np.argmax(guard_dict[most_minutes_asleep])
    return int(most_minutes_asleep)*minute_spend_asleep_most
                
        
def solvePartTwo(timetable):
    guard_dict = generateGuardDict(timetable)
    most_minutes_asleep = max(guard_dict, key=lambda key:max(guard_dict[key]))
    minute_spend_asleep_most = np.argmax(guard_dict[most_minutes_asleep])
    return int(most_minutes_asleep)*minute_spend_asleep_most

if __name__ == "__main__":
    with open("input.txt",'r') as inFile:
        puzzleInput = inFile.read()
        print(solve(puzzleInput))
        print(solvePartTwo(puzzleInput))

    