from flask import Flask, render_template, request, redirect, url_for, session, Markup
from file_len import file_length
from datetime import timedelta
from mainFunctions import *
import time
import glob
import sys

#for dev - change port and debug afterwards

app = Flask(__name__)

userPass=[["~owner", "a_boss"]]

#if true its the test server
if "True" in sys.argv:
	debugState = True
	portSet = 5000
	fileSubFolder="../testArticles/" #articles
	loginsSubFolder="../testLogins/" #logins
else:
	debugState = False
	portSet = 80
	fileSubFolder="../mainArticles/" #articles
	loginsSubFolder="../mainLogins/" #logins

fileBeginning="article_"
fileExtention=".txt"

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

		if not inFirstColumn(usernameWrite,userPass):
			userPass.append([usernameWrite, passwordWrite])

	#return str(userPass)
	#return None

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
			articleLinks.append(ii[len(fileSubFolder)+len(fileBeginning)+1:len(ii)-len(fileExtention)])

		for ii in fileNamesSorted:
			fileNameOpen = open((str(fileSubFolder) + str(ii)), "r")
			jj = fileNameOpen.readlines()
			fileNameOpen.close()

			if username==(jj[1])[:len(jj[1])-1]: # if the file is editable
				editableFiles.append("/articles/" + str(ii)[len(fileBeginning):len(ii)-len(fileExtention)] + "/edit/")
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

	if "<script>" in articleText or "</script>" in articleText:
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

		return "file """ + filePath + '" is there: ' + str(fileIsThere) 

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
				return "rendering"
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
	return str(len(userPass))

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
