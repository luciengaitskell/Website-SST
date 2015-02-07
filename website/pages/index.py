from flask import Flask, render_template, request, redirect, url_for
from file_len import file_length
import time
import glob

app = Flask(__name__)

@app.route('/')
def displayMain():
	fileNameOpen=""
	newDate=""
	fileSubFolder="articles/"
	fileBeginng="article-"
	fileExtention=".txt"
	dateNew=True
	uniqueDates=[]
	fileNames=[]
	fileNamesNew=[]
	fileNamesSorted=[]
	fileLines=[]
	singleIncrement=0
	titles=[]
	names=[]
	dates=[]
	texts=[]

	for ii in glob.glob("articles/*"):
		fileNames.append(ii)

	for ii in range(len(fileNames)):
		newDate=(fileNames[ii])[17:len(fileNames[ii])-6]
		dateNew=True
		for jj in uniqueDates:
			if jj == newDate:
				dateNew=False

		if dateNew == True:
			uniqueDates.append(newDate)

	uniqueDates.sort()

	for ii in range(len(uniqueDates)):
		fileNamesNew=[]
		for jj in fileNames:
			if uniqueDates[ii] == (fileNames[ii])[17:len(fileNames[ii])-6]:
				fileNamesNew.append((fileNames[ii])[17:len(fileNames[ii])-4])

		fileNamesNew.sort(reverse=True)

		for jj in fileNamesNew:
			fileNamesSorted.append(str(fileBeginng) + str(jj) + str(fileExtention))


	for ii in fileNamesSorted:
		fileNameOpen = open((str(fileSubFolder) + str(ii)), "r")
		jj = fileNameOpen.readlines()
		dates.append(jj[0])
		names.append(jj[1])
		titles.append(jj[2])
		texts.append(jj[3])
		texts.append(jj[4])

	return (fileNames[0])[17:len(fileNames[0])-4]
	#return uniqueDates[0]
	#return render_template('main.html', fileNamesSorted=fileNamesSorted, dates=dates, names=names, titles=titles, texts=texts, singleIncrement=singleIncrement)

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
	title=request.form.get("Title")
	articleText=request.form.get("articleText")

	while fileNamefound == False:
		articleNumber=articleNumber+1
		filePath=str(fileSubfolder) + str(fileBeginning) + str(articleDate) + "-" + str(articleNumber) + str(fileExtention)

		fileNamefound=True # gets set back to False if the name is already used
		for ii in glob.glob("articles/*"):
			if ii==filePath:
				fileNamefound=False
				break

	file = open(filePath, "w")
	file.write(str(articleDate) + "\n")
	file.write(str(name) + "\n")
	file.write(str(title) + "\n")
	file.write(str(articleText) + "\n\n")
	file.close()

	return redirect(url_for('displayMain'))
	#return "Your Name is: " + str(name) + ", The Title is: " + str(title) + ", \n You said: \n\n" + str(articleText) + ", IT WAS POSTED TO " + str(filePath)

@app.route('/articles/')
@app.route('/articles/<articleNumber>/')
def readMain(articleNumber=None):
	if articleNumber!=None:
		fileSubfolder="articles/"
		fileBeginning="article-"
		fileExtention=".txt"
		filePath=str(fileSubfolder) + str(fileBeginning) + str(articleNumber) + str(fileExtention)
		fileIsThere=False
		lineIterator=0
		for name in glob.glob(filePath):
			fileIsThere=True

		if fileIsThere==False:
			return redirect('/articles', code=302)
		else:
			articleFile=open(filePath)
			lines = articleFile.readlines()
			return render_template('article-render.html', filePath=filePath, lines=lines, lineIterator=lineIterator)
	else:
		return "NO FILE WAS FOUND WITH THAT NAME"

if __name__ == "__main__":
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=80
        )
