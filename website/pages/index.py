from flask import Flask, render_template, request, redirect
from file_len import file_length
from datetime import datetime
import glob

app = Flask(__name__)

@app.route('/')
def welcome():
	return "IT WORKS"

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
	filePath=""
	name=request.form.get("name")
	title=request.form.get("title")
	articleText=request.form.get("articleText")

	while fileNamefound == False:
		articleNumber=articleNumber+1
		filePath=str(fileSubfolder) + str(fileBeginning) + str(articleNumber) + str(fileExtention)

		fileNamefound=True # gets set back to False if the name is already used
		for ii in glob.glob("articles/*"):
			if ii==filePath:
				fileNamefound=False
				break

	file = open("newfile.txt", "w")
	file.write(str(datetime.date()) + "\n")
	file.write(name + "\n")
	file.write(title + "\n")
	file.write(articleText)
	file.close()

	return "Your Name is: " + str(name) + ", The Title is: " + str(title) + ", \n You said: \n\n" + str(articleText) + ", IT WAS POSTED TO " + str(filePath)

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
			articleFile.close()
			return render_template('article-render.html', lineIterator=lineIterator)
	else:
		return "NO FILE WAS FOUND WITH THAT NAME"

if __name__ == "__main__":
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=80
        )
