
import codecs
def strToBase64(hex):
    return codecs.encode(codecs.decode(hex, 'hex'), 'base64').decode()

def changeToBeHex(s):
    return (int(s,base=16))
def xorTwoStr(s1,s2):
    str1Hex = changeToBeHex(s1)
    str2Hex = changeToBeHex(s2)
    return hex (str1Hex ^ str2Hex)


print(strToBase64('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'))
print("round 2")
print(xorTwoStr("1c0111001f010100061a024b53535009181c","686974207468652062756c6c277320657965"))

print("we did it")

