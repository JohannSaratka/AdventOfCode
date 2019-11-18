'''
--- Day 5: How About a Nice Game of Chess? ---
You are faced with a security door designed by Easter Bunny engineers that seem to 
have acquired most of their security knowledge by watching hacking movies.
The eight-character password for the door is generated one character at a time by 
finding the MD5 hash of some Door ID (your puzzle input) and an increasing integer 
index (starting with 0).
A hash indicates the next character in the password if its hexadecimal representation 
starts with five zeroes. If it does, the sixth character in the hash is the next 
character of the password.
For example, if the Door ID is abc:
    The first index which produces a hash that starts with five zeroes is 3231929, 
    which we find by hashing abc3231929; the sixth character of the hash, and thus 
    the first character of the password, is 1.
'''
import unittest
import hashlib

class TestGetSolution(unittest.TestCase):
    def test_getCharFromHash_solution1(self):
        self.assertEqual(getCharFromHash('abc3231929'), '1', "")
    def test_getCharFromHash_solution2(self):
        self.assertEqual(getCharFromHash('abc5017308'), '8', "")
    def test_getCharFromHash_solution3(self):
        self.assertEqual(getCharFromHash('abc5278568'), 'f', "")
    @unittest.skip("brute force method takes to long")
    def test_findPassword_solution1(self):
        self.assertEqual(findPassword('abc'), '18f47a30', "")
    def test_getCharFromHashPartTwo_solution1(self):
        self.assertEqual(getCharFromHashPartTwo('abc3231929'), ('1','5'), "")
    def test_getCharFromHashPartTwo_solution2(self):
        self.assertEqual(getCharFromHashPartTwo('abc5357525'), ('4','e'), "")
    def test_findPasswordPartTwo_solution1(self):
        self.assertEqual(findPasswordPartTwo('abc'), '05ace8e3', "")
        
def findPassword(doorID):
    i=0
    password=''
    while(len(password)<8):
        passChar = getCharFromHash(doorID+str(i))
        if passChar:
            #print passChar
            password+=passChar
        i+=1     
    return password

def getCharFromHash(inputStr):
    md5hash=hashlib.md5(inputStr).hexdigest()
    if md5hash.startswith('00000'):
        return md5hash[5]
    return None
'''
--- Part Two ---
As the door slides open, you are presented with a second door that uses a slightly 
more inspired security mechanism. Clearly unimpressed by the last version (in what 
movie is the password decrypted in order?!), the Easter Bunny engineers have worked 
out a better solution.
Instead of simply filling in the password from left to right, the hash now also 
indicates the position within the password to fill. You still look for hashes that 
begin with five zeroes; however, now, the sixth character represents the position (0-7), 
and the seventh character is the character to put in that position.
A hash result of 000001f means that f is the second character in the password. Use 
only the first result for each position, and ignore invalid positions.
For example, if the Door ID is abc:
    The first interesting hash is from abc3231929, which produces 0000015...; 
    so, 5 goes in position 1: _5______.
'''
def findPasswordPartTwo(doorID):
    i=0
    password=[None]*8
    while(None in password):
        passPos,passChar = getCharFromHashPartTwo(doorID+str(i))
        if passChar:            
            passPos=int(passPos,16)
            if (passPos<8) and (password[passPos] is None):
                password[passPos]=passChar
                #print password
        i+=1     
    return "".join(password)

def getCharFromHashPartTwo(inputStr):
    md5hash=hashlib.md5(inputStr).hexdigest()
    if md5hash.startswith('00000'):
        return md5hash[5],md5hash[6]
    return None,None

if __name__ == '__main__':  
    #print findPassword('ugkcyxxp')
    print findPasswordPartTwo('ugkcyxxp')