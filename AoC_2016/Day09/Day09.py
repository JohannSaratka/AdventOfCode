'''
--- Day 9: Explosives in Cyberspace ---
Wandering around a secure area, you come across a datalink port to a new 
part of the network. After briefly scanning it for interesting files, you 
find one file in particular that catches your attention. It's compressed 
with an experimental format, but fortunately, the documentation for the 
format is nearby.
The format compresses a sequence of characters. Whitespace is ignored. To 
indicate that some sequence should be repeated, a marker is added to the 
file, like (10x2). To getDecompressedLength this marker, take the subsequent 10 
characters and repeat them 2 times. Then, continue reading the file after 
the repeated data. The marker itself is not included in the decompressed 
output.
If parentheses or other characters appear within the data referenced by a 
marker, that's okay - treat it like normal data, not a marker, and then 
resume looking for markers after the decompressed section.
'''
import unittest

class TestGetSolution(unittest.TestCase):
    def test_getDecompressedLength_NoMarkers(self):
        self.assertEqual(getDecompressedLength('ADVENT'), 6, "")
    def test_getDecompressedLengthtest_decompress_OneMarker(self):
        self.assertEqual(getDecompressedLength('A(1x5)BC'), 7, "")
    def test_getDecompressedLength_MarkerAndRepeatSequenceOnly(self):
        self.assertEqual(getDecompressedLength('(3x3)XYZ'), 9, "")
    def test_getDecompressedLength_TwoMarkers(self):
        self.assertEqual(getDecompressedLength('A(2x2)BCD(2x2)EFG'), 11, "")
    def test_getDecompressedLength_IgnoreMarkerInRepeatSequence1(self):
        self.assertEqual(getDecompressedLength('(6x1)(1x3)A'), 6, "")
    def test_getDecompLength_IgnoreMarker2(self):
        self.assertEqual(getDecompressedLength('X(8x2)(3x3)ABCY'), 18, "")

class Marker(object):
    def __init__(self):
        self.open=False
        self.activeSeq=False
        self.inReadLength=True
        self.length=''
        self.repeat=''
        self.repeatSeq=''
    def getLength(self):
        return int(self.length)
    def getRepeat(self):
        return int(self.repeat)
    def isRepeatSeqFull(self):
        return len(self.repeatSeq)==self.getLength()

def getDecompressedLength(compressedStr):
    uncomprStr=""
    mark=Marker()
    for char in compressedStr:
        if char=='(' and not mark.activeSeq:
            mark.open=True            
        elif mark.open:            
            if char=='x':            
                mark.inReadLength=False
            elif char==')':
                mark.activeSeq=True
                mark.inReadLength=True
                mark.open=False
            else:
                if mark.inReadLength:
                    mark.length+=char
                else:
                    mark.repeat+=char
        elif mark.activeSeq:
            mark.repeatSeq+=char
            if mark.isRepeatSeqFull():
                uncomprStr+=mark.repeatSeq*mark.getRepeat()
                mark.activeSeq=False
                mark.length=''
                mark.repeat=''
                mark.repeatSeq=''         
        else:
            uncomprStr+=char
    return len(uncomprStr)

if __name__ == '__main__':
    with open('Day09Data.txt','r')as inputFile:
        decompressedFile=map(getDecompressedLength,inputFile.read().splitlines())
        print sum(decompressedFile)