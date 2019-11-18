'''
--- Day 4: Security Through Obscurity ---
Finally, you come across an information kiosk with a list of rooms. Of 
course, the list is encrypted and full of decoy data, but the instructions 
to decode the list are barely hidden nearby. Better remove the decoy 
data first.
Each room consists of an encrypted name (lowercase letters separated by 
dashes) followed by a dash, a sector ID, and a checksum in square brackets.
A room is real (not a decoy) if the checksum is the five most common 
letters in the encrypted name, in order, with ties broken by 
alphabetization. For example:
    aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters are a (5), b (3), and then a tie between x, y, and z, which are listed alphabetically.
    a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all tied (1 of each), the first five are listed alphabetically.
    not-a-real-room-404[oarel] is a real room.
    totally-real-room-200[decoy] is not.
Of the real rooms from the list above, the sum of their sector IDs is 1514.
What is the sum of the sector IDs of the real rooms?
'''
import unittest
from collections import Counter
import re
import string

class TestGetSolution(unittest.TestCase):
    def test_getSectorID_solution1(self):
        self.assertEqual(getSectorID('aaaaa-bbb-z-y-x-123[abxyz]'), 123, "")
    def test_getSectorID_solution2(self):
        self.assertEqual(getSectorID('a-b-c-d-e-f-g-h-987[abcde]'), 987, "")
    def test_getSectorID_solution3(self):
        self.assertEqual(getSectorID('not-a-real-room-404[oarel]'), 404, "")
    def test_getSectorID_solution4(self):
        self.assertEqual(getSectorID('totally-real-room-200[decoy]'), 0, "")
    def test_decryptRoom_solution1(self):
        self.assertEqual(decryptRoom('qzmt-zixmtkozy-ivhz-',343), 'very encrypted name', "")

prog = re.compile(r"(\D+)(\d+)\[(\D+)\]")

def getSectorID(encryptedRoom):
    roomParts = getRoomParts(encryptedRoom)
    # If there are capturing groups in the separator and it matches at the start of the 
    # string, the result will start with an empty string. The same holds for the end of 
    # the string
    count = Counter(roomParts[1].replace('-','')).most_common()
    count.sort(key=lambda x: (-x[1],x[0]))
    checksum="".join([x[0] for x in count[:5]])
    return int(roomParts[2]) if checksum==roomParts[3] else 0

def getRoomParts(encryptedRoom):
    return prog.split(encryptedRoom)


'''
--- Part Two ---
With all the decoy data out of the way, it's time to decrypt this list 
and get moving.
The room names are encrypted by a state-of-the-art shift cipher, which is 
nearly unbreakable without the right software. However, the information 
kiosk designers at Easter Bunny HQ were not expecting to deal with a master 
cryptographer like yourself.
To decrypt a room name, rotate each letter forward through the alphabet 
a number of times equal to the room's sector ID. A becomes B, B becomes 
C, Z becomes A, and so on. Dashes become spaces.
'''
def decryptRoom(encryptedRoomName,sectorID):    
    cleanRoomName=encryptedRoomName[:-1].replace('-',' ')
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[sectorID%26:] + alphabet[:sectorID%26]
    table = string.maketrans(alphabet, shifted_alphabet)    
    return cleanRoomName.translate(table)

if __name__ == '__main__':
    with open('Day04Data.txt','r')as inputFile:    
        #print sum(map(getSectorID,inputFile.read().splitlines()))
        for line in inputFile:
            if getSectorID(line)!=0:
                roomParts = getRoomParts(line)
                # What is the sector ID of the room where North Pole objects are stored?
                if 'north' in decryptRoom(roomParts[1],int(roomParts[2])):
                    print roomParts[2]