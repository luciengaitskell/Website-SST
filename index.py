from flask import Flask, render_template, request, redirect, url_for, session, Markup
from file_len import file_length
from datetime import timedelta
import time
import glob
import sys


app = Flask(__name__)

userPass=[["~owner", "a_boss"]]

if len(sys.argv) >= 2:
	testServer=str(sys.argv[1])

#if true its the test server
if "True" in sys.argv:
	debugState = True
	if len(sys.argv) >= 3:
		if (str(sys.argv[2]).isdigit()):
			portSet=int(sys.argv[2])
		else:
			portSet=5000
	else:
		portSet=5000

	fileSubFolder="/var/www/Website-SST/testArticles/" #articles
	loginsSubFolder="/var/www/Website-SST/testLogins/" #logins
else:
	debugState = True #False
	portSet = 5000
	fileSubFolder="/var/www/Website-SST/mainArticles/" #articles
	loginsSubFolder="/var/www/Website-SST/mainLogins/" #logins

fileBeginning="article_"
fileExtention=".txt"

loginsExtention=".txt"

#delete this stupid comment

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

@app.before_request
def getLogins():
	global userPass
	for ii in glob.glob(str(loginsSubFolder)+ "*" + str(loginsExtention)):
		file=open(ii,"r")
		lines=file.readlines()
		file.close()
		usernameWrite=lines[0]
		usernameWrite=usernameWrite[:len(usernameWrite)-1]
		passwordWrite=lines[2]
		#passwordWrite=passwordWrite[:len(passwordWrite)-1] #WASN'T NEEDED WAS EOF

		if not inFirstColumn(usernameWrite,userPass):
			userPass.append([usernameWrite, passwordWrite])

	#return str(userPass)


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


# a "/" after the link is only for ones that users visit, ones without are form submit pages and other things

@app.route('/')
def displayMain():
	noFiles=False
	fileNameOpen=""
	newDate=""
	dateNew=True
	newText=[]
	fileNames=[]
	fileNamesNew=[]
	fileNamesSorted=[]
	fileLines=[]
	singleIncrement=0
	maxLineLength=30
	titles=[]
	names=[]
	dates=[]
	texts=[]
	editableFiles=[]
	articleLinks=[]
	loggedIn=loginCheckCache(userPass)
	username=loggedIn[0]

	for ii in glob.glob(str(fileSubFolder) + "*"):
		fileNames.append(ii)

	#return "fileNames: " +str(fileNames) +" | dates: " + str(dates)
	if len(fileNames)>0: # there are files
		fileNamesSorted=fileDateNumbOrgainise(fileNames, fileSubFolder + fileBeginning, fileExtention)
		#return str(fileNamesSorted)
		# getting infor in the sorted order
		#return str(fileNamesSorted)

		for ii in fileNamesSorted:
			articleLinks.append(ii[len(fileSubFolder)+len(fileBeginning):len(ii)-len(fileExtention)])

		for ii in fileNamesSorted:
			fileNameOpen = open(str(ii), "r")
			jj = fileNameOpen.readlines()
			fileNameOpen.close()

			if username==(jj[1])[:len(jj[1])-1]: # if the file is editable
				editableFiles.append("/articles/" + str(ii)[len(fileSubFolder)+len(fileBeginning):len(ii)-len(fileExtention)] + "/edit/")
			else:
				editableFiles.append(False)


			titles.append((jj[0])[:len(jj[0])-1])
			names.append((jj[1])[:len(jj[1])-1])
			dates.append((jj[2])[:len(jj[2])-1])

			#return str((newText[0])[:maxLineLength)])

			newText=[(jj[3].decode("utf-8")),""]

			#return unicode(len(newText[0]))
			if len(newText[0] + unicode(" ")) -1 > maxLineLength: # if the first display line is over max
				newText[0]=(newText[0])[:maxLineLength]
				newText[1]=(jj[3].decode("utf-8"))[maxLineLength:]

			if len(jj)>4: #there are more then one file text lines
				newText[1]=unicode(newText[1]) + unicode(jj[4].decode("utf-8"))
				# add the line on to the 2nd index - will get cut off below if needed

			if len(newText[1] + unicode(" ")) -1 > maxLineLength:
				newText[1]=unicode((newText[1])[:maxLineLength-len("...")]) + "..."
				# if the last display text line exceedes the max display lenght

			texts.append(newText[0])
			texts.append(newText[1])

		dates = arrayToUnicode(dates)
		names = arrayToUnicode(names)
		titles = arrayToUnicode(titles)
		#texts = arrayToUnicode(texts) # is decoded earlier
	else:
		editableFiles.append(False)
		noFiles=True

	#return str(dates)
	#return uniqueDates[1]
	return render_template('main.html'
	, noFiles=noFiles
	, fileNamesSorted=fileNamesSorted
	, dates=dates
	, names=names
	, titles=titles
	, texts=texts
	, singleIncrement=singleIncrement
	, username=username
	, editableFiles=editableFiles
	, articleLinks=articleLinks)

@app.route('/logOut/')
def signOut():
	session['username']=False
	session['password']=False
	return redirect('/')


@app.route('/login/')
def loginPage():
	inputIncorrect=request.args.get('inputIncorrect', '')
	inputIncorrect=str(inputIncorrect)

	return render_template('login.html',inputIncorrect=inputIncorrect)

@app.route('/loginCheck', methods=['POST'])
def loginCheckPage():
	'''username=request.form.get("username")
	password=request.form.get("password")
	remember=request.form.get("rememberPass")'''

	inputCreds=[
	request.form.get("username")
	, request.form.get("password")
	, request.form.get("rememberPass")]

	linkTrue='/'
	linkFalse='/login/?inputIncorrect=True'
	if inputCreds[2]=="on":
		notRemeberInput=False
	else:
		notRemeberInput=True

	for ii in inputCreds[:len(inputCreds)-1]:
		if not is_ascii(ii):
			return redirect('/login/')
	return loginCheckRedirect(inputCreds[0]
	, inputCreds[1]
	, userPass
	, linkTrue
	, linkFalse
	, notRemeberInput)

	#return str(credsCorrect)
	'''if credsCorrect==1:
		return redirect("/")
	else: #they arn't correct
		return redirect("/login/?inputIncorrect=True")'''

'''
@app.route('/deleteArticle')
def deleteArticle():

	searchword = request.args.get('articleName', '')

	if 'username' in session:
		return'Logged in as %s' % escape(session['username'])

	return 'You are not logged in'
'''
@app.route('/favicon.ico')
def favicon():
	return redirect(url_for('static', filename='favicon.ico'))

@app.route('/WheelerHub-logo.png')
def logo():
	return redirect(url_for('static', filename='logo/WheelerHub-logo.png'))

@app.route('/signUp/')
def signUp():
	error = request.args.get('error', '') # 1: Passwords don't match, 2: cred empty (str)
	username = request.args.get('username', False)
	email = request.args.get('email', False)

	return render_template('signUp.html'
	, error=error
	, username=username
	, email=email)

@app.route('/signUp/check', methods=['POST'])
def signUpCheck():
	credentials=[request.form.get("username")
	, request.form.get("email")
	, request.form.get("password1")
	, request.form.get("password2")]

	for ii in credentials:# stoping unallowed (unicode) characters (error 3)
		if not is_ascii(ii): #  or '"' in ii  #didn't need it, seemed to work w/out disrupting html
			return redirect("/signUp/?error=3")

	if " " in credentials[0] or " " in credentials[1]: # stopping spaces in email of username
		return redirect("/signUp/?error=5")

	for ii in range(len(credentials)):#checking for empty spaces(error 2)
		if credentials[ii]=="":
			return redirect("/signUp/?error=2&username=" + str(credentials[0]) + "&email=" + str(credentials[1]))

	if credentials[2]!=credentials[3]:# redirects if passwords arn't the same (error 1)
		return redirect("/signUp/?error=1&username=" + str(credentials[0]) + "&email=" + str(credentials[1]))

	session['username']=credentials[0]#only need to check the username
	session['password']=credentials[2]# so it signs in once account is made
	if ((loginCheckCache(userPass))[0])!=False:#the username is taken (error 4)
		return redirect("/signUp/?error=4&username=" + str(credentials[0]) + "&email=" + str(credentials[1]))

	filePath=findNewFileName(str(loginsSubFolder), str(fileExtention))
	file = open(filePath,"w")
	for ii in range(len(credentials[:len(credentials)-1])):#excludes last
		if ii==len(credentials)-2: # 2nd to last one (1st pass)
			file.write(credentials[ii])
		else:
			file.write(str(credentials[ii])+"\n")
	file.close()
	return redirect('/')
	#return str(filePath)
@app.route('/post/')
def postMain():
	loggedIn=loginCheckCache(userPass)
	username=loggedIn[0]

	return render_template('postArticle.html', username=username)

@app.route('/post/record', methods=['POST'])
@app.route('/post/edit', methods=['POST'])
def postRecord():
	fileNamefound = False

	articleNumber=0

	articleDate=time.strftime("%Y%m%d")
	filePath=""


	if (loginCheckCache(userPass))[1]!=False: # signed in thru session
		name=session['username']
	else:
		name=request.form.get("Name")

	if not name:#it's blank
		name="Anonymous"

	title=request.form.get("Title")

	if not title:#it's blank
		title="Unamed"

	articleText=request.form.get("articleText")

	if "<script>" in str(articleText) or "</script>" in str(articleText):
		# stops malicious js code being implanted
		return "I don't like hackers"

	if not articleText: # if the text is blank
		articleText="THIS IS SPAM"

	if request.path == "/post/edit":
		filePath=session['filePath']
		file = open(filePath, "r")
		lines=file.readlines()
		#return lines[0]
		articleDate=(lines[2]).rstrip() # removing newLine char which gets added lower down
		file.close()
	else:
		while fileNamefound == False:
			articleNumber=articleNumber+1
			filePath=str(fileSubFolder) + str(fileBeginning) + str(articleDate) + "-" + str(articleNumber) + str(fileExtention)

			fileNamefound=True # gets set back to False if the name is already used
			for ii in glob.glob(str(fileSubFolder) + "*"):
				if ii==filePath:
					fileNamefound=False
					break



	titleNew=(str(title.encode("UTF-8")) + "\n")
	nameWrite=(str(name.encode("UTF-8")) + "\n")
	articleDateWrite=(str(articleDate.encode("UTF-8")) + "\n")
	articleTextNew=(str(articleText.encode("UTF-8"))) # removed the + "\n\n"

	file = open(filePath, "w")
	file.write(titleNew)
	file.write(nameWrite)
	file.write(articleDateWrite)
	file.write(articleTextNew)
	file.close()

	return redirect("/")
	"""return str("Your Name is: "
	 + str(name)
	 + ", The Title is: "
	 + str(title)
	 + ", \n You said: \n\n"
	 + str(articleText)
	 + ", IT WAS POSTED TO "
	 + str(filePath))
	"""


@app.route('/articles/')
@app.route('/articles/<articleNumber>/')
@app.route('/articles/<articleNumber>/edit/')
def readMain(articleNumber=None):
	if articleNumber!=None:
		loggedIn=loginCheckCache(userPass)
		lineIterator=0
		filePath=str(fileSubFolder) + str(fileBeginning) + str(articleNumber) + str(fileExtention)
		#filePathSnipped=filePath[9:len(filePath)-4] # moved lower and now easier to read
		fileIsThere=False

		for name in glob.glob(filePath):
			fileIsThere=True

		#return 'file "' + filePath + '" is there: ' + str(fileIsThere)

		if fileIsThere==False:
			#return str(request.path)
			return redirect('/articles', code=302)
		else:
			filePathSnipped=str(fileBeginning)+str(articleNumber)
			articleFile=open(filePath)
			lines = articleFile.readlines()
			for ii in range(len(lines)):
				lines[ii]=(lines[ii])[:len(lines[ii])].decode('UTF-8')# Did this further down

			articleFile.close()

			if request.path == "/articles/" + str(articleNumber) + "/edit/":
				if loggedIn[0]!=False:
					if str(lines[1])[:len(lines[1])-1]==str(session['username']):
						text=lines[3]
						for ii in range(len(lines)):
							if ii==0:
								title=lines[ii]#.decode('UTF-8')
							elif ii==1:
								name=lines[ii]#.decode('UTF-8')
							elif ii>3:
								text= unicode(text) + unicode(lines[ii]) # the line already has carrage returns in them

						#return text
						#text.decode('UTF-8') # only can decode afterwards cuz
						# strings added a couple lines up

						#return str(text)
						#had to omit last char from the file from the line (it stopped it working)
						session['filePath']=filePath
						return render_template('articleEditor.html'
						, lines=lines
						, title=title
						, name=name
						, text=text)
						#, filePathSnipped=filePathSnipped
						#, filePath=filePath)
						return "u need: " + str(lines[1]) + ", but ur: " + str(session['username'])
				return "YOU ARN'T EVEN SIGNED IN"
			else:
				return render_template('articleRender.html'
				, filePathSnipped=filePathSnipped
				, filePath=filePath
				, lines=lines
				, lineIterator=lineIterator)
	else:
		return "NO FILE WAS FOUND WITH THAT NAME"

@app.route('/help/')
def helpPage():
	return render_template('helpPage.html')

@app.route('/test/')
def testFunc():
	#return str(len(userPass))
	return request.url

@app.route('/radio/')
def radio():
	return render_template('theMixRadio.html')

if __name__ == "__main__":
	app.secret_key = 'Ymsf,sfatwBU!Iwruh,bus'
	app.debug = debugState
	app.run(
		host='0.0.0.0',
		port=portSet
		)
