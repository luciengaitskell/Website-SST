from flask import Flask, render_template, request, redirect
from file_len import file_length
import glob

app = Flask(__name__)

@app.route('/')
def welcome():
	return "IT WORKS"

@app.route('/post/')
def postMain():
	return render_template('postArticle.html')

@app.route('/post_record/', methods=['POST'])
def postRecord():
	Name=request.form.get("Name")
	Title=request.form.get("Title")
	articleText=request.form.get("articleText")
	return "THE POST WORKED (RECORDING HAS NOT YET BEEN INPLEMENTED)"

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
