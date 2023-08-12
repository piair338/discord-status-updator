global file
import base64
import sys
from datetime import date
import requests

TEXT = "Message you want as a profile"
status = 'DND' # differents status are Online, Idle, DND, invisible
TOKEN = 'YOUR TOKEN GOES HERE'


def add_byte(byte):
    global settings
    settings = settings + " " +str(byte)

def taille(txt, offset=0): # output the len of the binary string in binary
    t = text_to_binary(txt).count(" ") + offset + 1 
    t = bin(t)
    t = str(t)
    t = t[2:]
    t = t.zfill(8)
    if t > "01111111":
        t = t + " 00000001"
    return(t)

status_code = { # look like size of fthe word + 2
    "Online":"00001000",
    "Idle":"00000110",
    "DND":"00000101",
    "Invisible": "00001011"
}

status_name = { # first byte is the len of the name, then letter of the status in utf-8
    "Online":"00000110 01101111 01101110 01101100 01101001 01101110 01100101",
    "Idle":"00000100 01101001 01100100 01101100 01100101",
    "DND":"00000011 01100100 01101110 01100100",
    "Invisible": '00001001 01101001 01101110 01110110 01101001 01110011 01101001 01100010 01101100 01100101'
}

offsets = {
    "Online":8,
    "Idle":6,
    "DND":5,
    "Invisible":11,
}

def text_to_binary(s):
    binary_utf8 = ' '.join(format(byte, '08b') for byte in s.encode('utf-8')) #thanks ChatGPT, convert a string to a binary string, using UTF-8
    return(binary_utf8)



FIRST_BYTE = "01011010"
SPACER = "00001010"
END_SEQUENCE = "00011010 00000010 00001000 00000001"



def custom_offset_1(text): #add if later byte are longer
    if taille(text, 2).count(" ") > 0 : 
        if taille(text).count(" ") > 0 :
            return(2)
        return(1)
    return(0)

def custom_offset_2(text): #add if later byte are longer
    if taille(text).count(" ") > 0 : 
        return(1)
    return(0)

settings = FIRST_BYTE # first byte, always constant
add_byte(taille(TEXT, 10 + offsets[status] + custom_offset_1(TEXT))) # 10 is a bit weird but alright, probably related to emoji or big size -> MAY BE RELATED TO THE NUMBER OR CONTROLS BYTES
add_byte(SPACER)

add_byte(status_code[status])   # maybe can be merged with things under
add_byte(SPACER)
add_byte(status_name[status]) 

add_byte("00010010") # depend on emoji but i don't know how yet

add_byte(taille(TEXT, 2 + custom_offset_2(TEXT))) # 2 is a bit weird but alright, probably related to emoji
add_byte(SPACER)

add_byte(taille(TEXT))
add_byte(text_to_binary(TEXT))

add_byte(END_SEQUENCE) # maybe related to current date -> apparently not, lets check if it's related to UTC time diff


# convert string to bytes
binary_data = bytes(int(b, 2) for b in settings.split())
# convert byte to base64 
base64_data = base64.b64encode(binary_data)

#debug stuff
message = (base64_data.decode('utf-8'))
print(TEXT)
print(message)


# User ID



# request
url = 'https://discord.com/api/v9/users/@me/settings-proto/1'
headers = {
    'authorization': TOKEN,
    'content-type': 'application/json',
}

data = '{"settings":"' + message + '"}'

# send to server

response = requests.patch(url, headers=headers, data=data)
print(response)
print(response.text)
print("\n\n")
print(message)
