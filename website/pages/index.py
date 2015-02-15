from flask import Flask, render_template, request, redirect, url_for, session, Markup
from file_len import file_length
from datetime import timedelta
import time
import glob

app = Flask(__name__)

userPass=[["ur_mom", "stuff"],["user", "pass"]]

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

# a "/" after the link is only for ones that users visit, ones without are form submit pages and other things

@app.route('/signOut/')
def signOut():
	session['username']=""
	session['password']=""
	return redirect('/')

#@app.route('/test/')
"""def autoLoginTest():
	credsCorrect=loginCheck(False,-1,userPass)
	#return session['username']
	return str(credsCorrect)"""

@app.route('/test/', methods=['POST'])
def tests():
	if "poo" in request.form:
		name=request.form.get("poo")
		return name
	else:
		return "wasn't there"

@app.route('/login/')
def loginPage():
	inputIncorrect=request.args.get('inputIncorrect', '')

	if str(inputIncorrect)=="True":
		return "u got it wrong"

	return render_template('login.html')

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

@app.route('/')
def displayMain():
	noFiles=False
	fileNameOpen=""
	newDate=""
	fileSubFolder="articles/"
	fileBeginng="article-"
	fileExtention=".txt"
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
				fileNamesSorted.append(str(fileBeginng) + str(jj) + str(fileExtention))

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

@app.route('/post/')
def postMain():
	return render_template('postArticle.html')

@app.route('/post/record', methods=['POST'])
def postRecord():
	fileNamefound= False
	fileSubfolder="articles/"
	fileBeginning="article-"
	fileExtention=".txt"
	articleNumber=0
	articleDate=time.strftime("%Y%m%d")
	filePath=""
	name=request.form.get("Name")

	if not name:#it's blank
		name="Anonymous"

	title=request.form.get("Title")

	if not title:#it's blank
		title="Unamed"

	articleText=request.form.get("articleText")

	if not articleText:
		articleText="THIS IS SPAM"

	while fileNamefound == False:
		articleNumber=articleNumber+1
		filePath=str(fileSubfolder) + str(fileBeginning) + str(articleDate) + "-" + str(articleNumber) + str(fileExtention)

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

	return redirect(url_for('displayMain'))
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
def readMain(articleNumber=None):
	if articleNumber!=None:
		fileSubfolder="articles/"
		fileBeginning="article-"
		fileExtention=".txt"
		filePath=str(fileSubfolder) + str(fileBeginning) + str(articleNumber) + str(fileExtention)
		filePathSnipped=filePath[9:len(filePath)-4]
		fileIsThere=False
		lineIterator=0
		for name in glob.glob(filePath):
			fileIsThere=True

		if fileIsThere==False:
			return redirect('/articles', code=302)
		else:
			articleFile=open(filePath)
			lines = articleFile.readlines()
			for ii in range(len(lines)):
				lines[ii]=lines[ii].decode('UTF-8')
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
