from flask import Flask, render_template, request, redirect, url_for, session, Markup
from file_len import file_length
from datetime import timedelta
import time
import glob

app = Flask(__name__)

userPass=[["ur_mom", "stuff"],["user", "pass"]]
fileSubFolder="articles/"
fileBeginning="article-"
fileExtention=".txt"

def makeSessionPermanent():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(days=31)

def makeSessionDefault():
	session.permanent = False

def loginCheck(username,password,logins, timeOut=True):
	#username is False check cache
	#timeOut is -1 or less for default, 0 for forever, or how many minutes
	passUserCorrect=0

	if username!=False:
		if not timeOut:
			makeSessionPermanent()
		else:
			makeSessionDefault()

	for indexNumb in range(len(logins)):
		if username==False:
			if 'username' in session:
				if session['username']==logins[indexNumb][0]:
					if session['password']==logins[indexNumb][1]:
						#return "remembered"
						passUserCorrect=1
						break
		elif str(username)==logins[indexNumb][0]:
			if str(password)==logins[indexNumb][1]:
				passUserCorrect=1
				session['username']=str(username)
				session['password']=str(password)
			break

	#makeSessionDefault()
	#return redirect("/")
	return str(passUserCorrect) #returns 1 if the creds are correct and 0 if they arn't

def loginCheckRedirect(username,password,logins, linkTrue, linkFalse, timeOut=True):
	result=loginCheck(username,password,logins, timeOut)
	#return str(result)
	if int(result)==1:
		return redirect(linkTrue)
	else:
		return redirect(linkFalse)

def getArticleStuff():
	pass

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
	loggedIn=loginCheck(False,False,userPass)
	loggedIn=int(loggedIn)
	username=False

	if loggedIn==1:
		username=session['username']

	for ii in glob.glob("articles/*"):
		fileNames.append(ii)

	if len(fileNames)>0:
		for ii in range(len(fileNames)):
			newDate=(fileNames[ii])[17:len(fileNames[ii])-6]
			dateNew=True
			for jj in uniqueDates:
				if jj == newDate:
					dateNew=False

			if dateNew == True:
				uniqueDates.append(newDate)

		uniqueDates.sort(reverse=True)

		for ii in range(len(uniqueDates)):
			fileNamesNew=[]

			for jj in fileNames:
				#testVar=testVar+1
				if uniqueDates[ii] == (jj)[17:len(jj)-6]:
					fileNamesNew.append((jj)[17:len(jj)-4])

			fileNamesNew.sort(reverse=True)

			for jj in fileNamesNew:
				fileNamesSorted.append(str(fileBeginning) + str(jj) + str(fileExtention))

		for ii in fileNamesSorted:
			fileNameOpen = open((str(fileSubFolder) + str(ii)), "r")
			jj = fileNameOpen.readlines()

			titles.append(jj[0])
			names.append(jj[1])
			dates.append(jj[2])

			#return str((newText[0])[:maxLineLength)])

			newText=[jj[3],""]

			if len(newText[0]) > maxLineLength:
				newText[0]=(newText[0])[:maxLineLength]
				newText[1]=(jj[3])[maxLineLength:]

			#if len(jj)>4 or newText[1] != None: #more than one text lines or the first line text carries over
				#newText.append("")#need to create a elemet in the 1 place
				#return "it equals: " + str(newText[1])
				#newText[1]=(newText[0])[maxLineLength:]

			if newText[1] != "":
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
	, username=username)

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
	username=request.form.get("username")
	password=request.form.get("password")
	remember=request.form.get("remeberPass")
	linkTrue='/'
	linkFalse='/login/?inputIncorrect=True'

	if remember=="on":
		remeberInput=False
	else:
		remeberInput=True

	#credsCorrect=int(loginCheck(username,password,userPass,remeberInput))

	return loginCheckRedirect(username,password,userPass, linkTrue, linkFalse, remeberInput)

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



@app.route('/post/')
def postMain():
	loggedIn=loginCheck(False,False,userPass)
	loggedIn=int(loggedIn)
	username=False

	if loggedIn==1:
		username=session['username']

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


	articleDateWrite=(str(articleDate.encode("UTF-8")) + "\n")
	nameWrite=(str(name.encode("UTF-8")) + "\n")
	titleNew=(str(title.encode("UTF-8")) + "\n")
	articleTextNew=(str(articleText.encode("UTF-8")) + "\n\n")

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
		lineIterator=0
		filePath=str(fileSubFolder) + str(fileBeginning) + str(articleNumber) + str(fileExtention)
		#filePathSnipped=filePath[9:len(filePath)-4] # moved lower and now easier to read
		fileIsThere=False

		for name in glob.glob(filePath):
			fileIsThere=True

		if fileIsThere==False:
			return redirect('/articles', code=302)
		else:
			filePathSnipped=str(fileBeginning)+str(articleNumber)
			articleFile=open(filePath)
			lines = articleFile.readlines()
			for ii in range(len(lines)):
				lines[ii]=lines[ii].decode('UTF-8')

			articleFile.close()

			if request.path == "/articles/" + str(articleNumber) + "/edit/":
				if loginCheck(False, False, userPass):
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
				return "YOU DON'T HAVE PERMS"
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
	return str(request.path)
"""def autoLoginTest():
	credsCorrect=loginCheck(False,-1,userPass)
	#return session['username']
	return str(credsCorrect)"""

"""@app.route('/test/', methods=['POST'])
def tests():
	if "Name" in request.form:
		name=request.form.get("Name")
		return name
	else:
		return "wasn't there" """

"""@app.route('/signature/')
def signature():
	return render_template('signature.html')"""


if __name__ == "__main__":
	app.secret_key = 'Ymsf,sfatwBU!Iwruh,bus'
	app.debug = True
	app.run(
		host='0.0.0.0',
		port=80
		)
