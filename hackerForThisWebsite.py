import requests
import string

def charCheck(charNumb, password, charRange):
    for ii in charRange:
        if numToEnd>0:
            succeeded = charCheck(charNumb+1, password, charRange)
            if not succeeded:
                password[charNumb]=ii
    else:


'''
To do:

1. make main thread start charCheck as a seperate thread

2. make two queues for charCheck to send the guesses back to the main thread
and to send instructions to charCheck from the main thread

3. make main thread to deal with guesses (post, tell charCheck if correct, etc.)

4. check charCheck is working

5. make sure charCheck waits while main thread is posting. (make it wait for
command from one of the queues)

6. make it so charCheck terminates if it is right
'''

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
