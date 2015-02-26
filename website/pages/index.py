from flask import Flask, render_template, request, redirect, url_for, session, Markup
from file_len import file_length
from datetime import timedelta
import time
import glob

app = Flask(__name__)

userPass=[["ur_mom", "stuff"],["cheese", "pass"]]
fileSubFolder="articles/" #articles
fileBeginning="article-"
fileExtention=".txt"

loginsSubFolder="logins/" #logins
loginsExtention=".txt"

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
		userPass.append([usernameWrite, passwordWrite])
	pass

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

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
	uniqueDates=[]
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
	loggedIn=loginCheckCache(userPass)
	username=loggedIn[0]

	for ii in glob.glob("articles/*"):
		fileNames.append(ii)

	if len(fileNames)>0: # there are files
		for ii in range(len(fileNames)): # for each file
			newDate=(fileNames[ii])[(len(fileSubFolder)+len(fileBeginning)):len(fileNames[ii])-6] # Date of the file
			dateNew=True
			for jj in uniqueDates: # Finding if the date of the file is new
				if jj == newDate:
					dateNew=False

			if dateNew == True:
				uniqueDates.append(newDate) # adding file date if its good

		uniqueDates.sort(reverse=True) # sorting the dates so the latest ones are first

		for ii in range(len(uniqueDates)):
			fileNamesNew=[]

			for jj in fileNames:
				#testVar=testVar+1
				if uniqueDates[ii] == (jj)[(len(fileSubFolder)+len(fileBeginning)):len(jj)-6]:
					fileNamesNew.append((jj)[(len(fileSubFolder)+len(fileBeginning)):len(jj)-4])

			fileNamesNew.sort(reverse=True)

			for jj in fileNamesNew:
				fileNamesSorted.append(str(fileBeginning) + str(jj) + str(fileExtention))

		for ii in fileNamesSorted:
			fileNameOpen = open((str(fileSubFolder) + str(ii)), "r")
			jj = fileNameOpen.readlines()
			fileNameOpen.close()

			if username!=False:
				#return "ur: " + str(session['username']) + ", but u need: " + str((jj[1])[:len(jj[1])-1])
				if username==(jj[1])[:len(jj[1])-1]:
					editableFiles.append("/" + str(fileSubFolder) + str(ii)[len(fileBeginning):len(ii)-4] + "/edit/")
				else:
					editableFiles.append(False)
			else:
				editableFiles.append(False)

			titles.append((jj[0])[:len(jj[0])-1])
			names.append((jj[1])[:len(jj[1])-1])
			dates.append((jj[2])[:len(jj[2])-1])

			#return str((newText[0])[:maxLineLength)])

			newText=[jj[3],""]

			if len(newText[0]) > maxLineLength:
				newText[0]=(newText[0])[:maxLineLength]
				newText[1]=(jj[3])[maxLineLength:]
				if len(newText[1]) > maxLineLength:
					newText[1]=str((newText[1])[:maxLineLength-len("...")]) + "..."

			if len(jj) > 4:
				newText[1]=str(newText[1]) + str(jj[4])

			texts.append(newText[0])
			texts.append(newText[1])
			#return newText[1]

		dates = arrayToUnicode(dates)
		names = arrayToUnicode(names)
		titles = arrayToUnicode(titles)
		texts = arrayToUnicode(texts)
	else:
		editableFiles.append(False)
		noFiles=True

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
	, editableFiles=editableFiles)

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
	remember=request.form.get("remeberPass")'''

	inputCreds=[
	request.form.get("username")
	, request.form.get("password")
	, request.form.get("remeberPass")]

	linkTrue='/'
	linkFalse='/login/?inputIncorrect=True'
	if inputCreds[2]=="on":
		notRemeberInput=False
	else:
		notRemeberInput=True

	for ii in inputCreds[:len(inputCreds)]:
		return ii
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

def arrayToUnicode(inputArray):
	outputArray=[]

	for gg in inputArray:
		outputArray.append(gg.decode('UTF-8'))
	return outputArray

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
	filePathBeg="logins/"
	credentials=[request.form.get("username")
	, request.form.get("email")
	, request.form.get("password1")
	, request.form.get("password2")]


	for ii in credentials:#stoping unicode characters (error 3)
		if not is_ascii(ii):
			return redirect("/signUp/?error=3")

	for ii in range(len(credentials)):#checking for empty spaces(error 2)
		if credentials[ii]=="":
			return redirect("/signUp/?error=2&username=" + str(credentials[0]) + "&email=" + str(credentials[1]))

	if credentials[2]!=credentials[3]:# redirects if passwords arn't the same (error 1)
		return redirect("/signUp/?error=1&username=" + str(credentials[0]) + "&email=" + str(credentials[1]))

	session['username']=credentials[0]#only need to check the username
	session['username']=credentials[2]# so it signs in once account is made
	if ((loginCheckCache(userPass))[0])!=False:#the username is taken (error 4)
		return redirect("/signUp/?error=4&username=" + str(credentials[0]) + "&email=" + str(credentials[1]))

	filePath=findNewFileName(str(filePathBeg), str(fileExtention))
	file = open(filePath,"w")
	for ii in range(len(credentials[:len(credentials)-1])):#excludes last
		if ii==len(credentials)-2: # 2nd to last one (1st pass)
			file.write(credentials[ii])
		else:
			file.write(str(credentials[ii])+"\n")
	file.close()
	return str(filePath)
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
	name=request.form.get("Name")
	if name==None:#it's just the username
		name=session['username']

	if not name:#it's blank
		name="Anonymous"

	title=request.form.get("Title")

	if not title:#it's blank
		title="Unamed"

	articleText=request.form.get("articleText")

	if not articleText:
		articleText="THIS IS SPAM"

	if request.path == "/post/edit":
		filePath=session['filePath']
		file = open(filePath, "r")
		lines=file.readlines()
		#return lines[0]
		articleDate=lines[2]
		file.close()
	else:
		while fileNamefound == False:
			articleNumber=articleNumber+1
			filePath=str(fileSubFolder) + str(fileBeginning) + str(articleDate) + "-" + str(articleNumber) + str(fileExtention)

			fileNamefound=True # gets set back to False if the name is already used
			for ii in glob.glob("articles/*"):
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

		if fileIsThere==False:
			return str(request.path)
			return redirect('/articles', code=302)
		else:
			filePathSnipped=str(fileBeginning)+str(articleNumber)
			articleFile=open(filePath)
			lines = articleFile.readlines()
			for ii in range(len(lines)):
				lines[ii]=lines[ii].decode('UTF-8')

			articleFile.close()

			if request.path == "/articles/" + str(articleNumber) + "/edit/":
				if loggedIn[0]!=False:
					if str(lines[1])[:len(lines[1])-1]==str(session['username']):
						text=lines[3]
						for ii in range(len(lines)):
							if ii==0:
								title=lines[ii]
							elif ii==1:
								name=lines[ii]
							elif ii>3:
								text= str(text) + str(lines[ii]) # the line already has carrage returns in them
						#return str(text)
						#had to omit last char from the file from the line (it stopped it working)
						session['filePath']=filePath;
						return render_template('articleEditor.html'
						, filePathSnipped=filePathSnipped
						, filePath=filePath
						, lines=lines
						, title=title
						, name=name
						, text=text)
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
	return str(userPass[2][0])

if __name__ == "__main__":
	app.secret_key = 'Ymsf,sfatwBU!Iwruh,bus'
	app.debug = True
	app.run(
		host='0.0.0.0',
		port=80
		)
