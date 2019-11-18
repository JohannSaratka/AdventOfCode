'''
--- Day 6: Signals and Noise ---
Something is jamming your communications with Santa. Fortunately, your signal is 
only partially jammed, and protocol in situations like this is to switch to a simple 
repetition code to get the message through.
In this model, the same message is sent repeatedly. You've recorded the repeating 
message signal (your puzzle input), but the data seems quite corrupted - almost too 
badly to recover. Almost.
All you need to do is figure out which character is most frequent for each position.
'''
import unittest
from collections import Counter

class TestGetSolution(unittest.TestCase):
    testInput= ['eedadn',
                'drvtee',
                'eandsr',
                'raavrd',
                'atevrs',
                'tsrnev',
                'sdttsa',
                'rasrtv',
                'nssdts',
                'ntnada',
                'svetve',
                'tesnvt',
                'vntsnd',
                'vrdear',
                'dvrsen',
                'enarar']
    def test_getErrorCorrectedMessage_solution1(self):
        self.assertEqual(getErrorCorrectedMessage(self.testInput), 'easter', "")
    def test_getErrorCorrectedMessage_solution2(self):
        self.assertEqual(getErrorCorrectedMessagePartTwo(self.testInput), 'advent', "")

def getErrorCorrectedMessage(inpMsg):
    inpMsgTranspose=zip(*inpMsg)
    message=''
    for line in inpMsgTranspose:
        message += Counter(line).most_common(1)[0][0]
    
    return message
def getErrorCorrectedMessagePartTwo(inpMsg):
    inpMsgTranspose=zip(*inpMsg)
    message=''
    for line in inpMsgTranspose:
        message += Counter(line).most_common()[-1][0]
    
    return message
'''
--- Part Two ---
Of course, that would be the message - if you hadn't agreed to use a modified 
repetition code instead.
In this modified code, the sender instead transmits what looks like random data, 
but for each character, the character they actually want to send is slightly less 
likely than the others. Even after signal-jamming noise, you can look at the letter 
distributions in each column and choose the least common letter to reconstruct the 
original message.
In the above example, the least common character in the first column is a; in the 
second, d, and so on. Repeating this process for the remaining characters produces 
the original message, advent.
Given the recording in your puzzle input and this new decoding methodology, what is 
the original message that Santa is trying to send?
'''
if __name__ == '__main__':
    with open('Day06Data.txt','r')as inputFile:
        lines=inputFile.read().splitlines()
        print getErrorCorrectedMessage(lines)
        print getErrorCorrectedMessagePartTwo(lines)