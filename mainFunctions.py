from flask import Flask, render_template, request, redirect, url_for, session, Markup
from file_len import file_length
from datetime import timedelta
import time
import glob
import sys

def findBetween(inputString, findString, lowerBound, upperBound=False):
	if upperBound == False:
		upperBound=len(inputString)

	if lowerBound > upperBound: # if lower bound is larger
		stupidVar = upperBound
		upperBound = lowerBound
		lowerBound = stupidVar

	if upperBound > len(inputString):
		upperBound = len(inputString)

	if lowerBound > len(inputString):
		lowerBound = upperBound

	inputString=inputString[lowerBound:upperBound]
	returnAmount=inputString.find(findString)
	if not returnAmount == -1:
		returnAmount = returnAmount + lowerBound

	return returnAmount

def inFirstColumn(theString, theArray):
	for ii in theArray:
		if theString == ii[0]:
			return True
	return False

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def utf8len(s):
    return len(s.encode('utf-8'))

def arrayToUnicode(inputArray):
	outputArray=[]

	for gg in inputArray:
		outputArray.append(gg.decode('UTF-8'))
	return outputArray

def findNewFileName(leadingPath, extention):
	fileNumber=0
	fileFound=False
	filesThere=False
	while not fileFound:
		fileNumber=fileNumber+1
		filePath=str(leadingPath) + str(fileNumber) + str(extention)
		for ii in glob.glob(str(leadingPath) + "*" + str(extention)):
			filesThere=True
			if ii!=filePath:
				fileFound=True
				pathOutput=filePath
				break

		if filesThere==False:
			fileFound=True
			pathOutput=filePath
			break

	return str(pathOutput)

def fileDateNumbOrgainise(fileNames, theFileBeginning, theFileExtention):
	uniqueDates=[]
	fileNamesSorted=[]
	dates=[]

	for ii in fileNames:
		dates.append(ii[len(theFileBeginning):int(findBetween(ii,"-", len(theFileBeginning)+1))])

	for ii in range(len(fileNames)): # for each file
		newDate= dates[ii] # Date of the file
		dateNew=True
		for jj in uniqueDates: # Finding if the date of the file is new
			if jj == newDate:
				dateNew=False

		if dateNew == True:
			uniqueDates.append(newDate) # adding file date if its good

	uniqueDates.sort(reverse=True) # sorting the dates so the latest ones are first

	for ii in range(len(uniqueDates)):

		fileNamesNew=[]

		for jj in range(len(fileNames)):
			#return "jj: " + jj + " | returned: " + str(findBetween(jj, "-", len(theFileBeginning)))
			#return (jj)[len(theFileBeginning):findBetween(jj, "-", len(theFileBeginning))]
			#return "uniqueDates: " + str(uniqueDates) + " | " + (jj)[len(theFileBeginning):findBetween(jj, "-", len(theFileBeginning))]
			if uniqueDates[ii] == dates[jj]:
				fileNamesNew.append((fileNames[jj])[len(theFileBeginning):len(fileNames[jj])-len(theFileExtention)])

		fileNamesNew.sort(reverse=True)

		for jj in fileNamesNew:
			fileNamesSorted.append(str(theFileBeginning) + str(jj) + str(theFileExtention))

	return fileNamesSorted

def makeSessionPermanent():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(days=31)

def makeSessionDefault():
	session.permanent = False

def loginCheckMain(username, password, logins, cacheCheck, timeOut=True):
	#username is False check cache
	userPassOut=[False,False]
	mode=False
	#mode set
	if (username==False or password==False) and cacheCheck:# mode: loginCheckCache
		mode=1
	elif cacheCheck: # mode: loginCheckCacheMatch
		mode=2
	elif not cacheCheck: #mode: loginCheckSignin
		mode=3

	if not cacheCheck: # its a signin
		if not timeOut:
			makeSessionPermanent()
		else:
			makeSessionDefault()

	for indexNumb in range(len(logins)):
		if cacheCheck==True:
			if 'username' in session:
				userCheck=logins[indexNumb][0]
				passCheck=logins[indexNumb][1]

				if username!=False:
					userCheck=username
					passCheck=password

				if session['username']==userCheck:
					if 'password' in session:
						if session['password']==passCheck:
							userPassOut=[userCheck, passCheck]
						else:
							userPassOut=[userCheck, False] #if username matches but the pass doesn't
					else:
						userPassOut=[userCheck, False] #if username matches but the pass doesn't

					break #if the username is correct but the pass isn't it still exits
		elif str(username)==logins[indexNumb][0]:
			if str(password)==logins[indexNumb][1]:
				userPassOut=[str(username), str(password)]
				session['username']=str(username)
				session['password']=str(password)
			break #if the username is correct but the pass isn't it still exits

	#makeSessionDefault()
	#return redirect("/")
	return userPassOut

def loginCheckCache(logins): # checks if the cache contains a match for creds in logins
	return loginCheckMain(False, False, logins, True)

def loginCheckCacheMatch(username, password):
	# checks if cache matches the input username and pass
	return loginCheckMain(username, password, [ ], True)

def loginCheckSignin(username, password, logins, timeOut=True):
	# checks if the user and pass match a login, has a time out option
	return loginCheckMain(username, password, logins, False, timeOut)

def loginCheckRedirect(username,password,logins, linkTrue, linkFalse, timeOut=True):
	result=loginCheckSignin(username, password, logins, timeOut)
	#return str(result)
	if result[0]!=False:
		return redirect(linkTrue)
	else:
		return redirect(linkFalse)
