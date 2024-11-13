# Text to Morse Code and Morse Code to Text Converter

import zlib

def texttomorse(text):
    text = zlib.compress(text.encode()).decode('latin-1')
    text = ''.join(format(ord(char), '08b') for char in text)
    morse_code_dict = {'1':'🤣','0':'😂'}
    return ' '.join(morse_code_dict.get(char.upper(), '') for char in text)

def morsetotext(morse):
    morse_code_dict = {'🤣':'1','😂':'0'}
    a =  ''.join(morse_code_dict.get(code, '') for code in morse.split())
    return zlib.decompress(''.join(chr(int(a[i:i+8], 2)) for i in range(0, len(a), 8)).encode('latin-1')).decode()
