from flask import Flask, render_template, request, redirect, url_for
from file_len import file_length
import time
import glob

app = Flask(__name__)

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

			dates.append(jj[0])
			names.append(jj[1])
			titles.append(jj[2])

			#return str((newText[0])[:maxLineLength)])

			newText.append(jj[3])

			if len(newText[0]) > maxLineLength:
				newText[0]=(newText[0])[:maxLineLength]
				newText.append((newText[0])[maxLineLength:])

			if jj>4 or len(newText) > 1:
				return "it equals: " + len(str((newText[0])[:maxLineLength]))
				newText[1]=(newText[0])[maxLineLength:]
				if len(newText[1]) > maxLineLength:
					newText[1]=str((newText[1])[:maxLineLength-len("...")]) + "..."

				if len(jj) > 4:
					newText[1]=str(newText[1]) + str(jj[4])

				texts.append(newText[0])
				texts.append(newText[1])
			else:
				texts.append(jj[3])

		dates = arrayToUnicode(dates)
		names = arrayToUnicode(names)
		titles = arrayToUnicode(titles)
		texts = arrayToUnicode(texts)
	else:
		noFiles=True

	#return uniqueDates[1]
	return render_template('main.html', noFiles=noFiles, fileNamesSorted=fileNamesSorted, dates=dates, names=names, titles=titles, texts=texts, singleIncrement=singleIncrement)

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

	if not name:
		name="Anonymous"

	title=request.form.get("Title")

	if not title:
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
	file.write(articleDateWrite)
	file.write(nameWrite)
	file.write(titleNew)
	file.write(articleTextNew)
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
			return render_template('articleRender.html', filePathSnipped=filePathSnipped, filePath=filePath, lines=lines, lineIterator=lineIterator)
	else:
		return "NO FILE WAS FOUND WITH THAT NAME"

if __name__ == "__main__":
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=80
        )
