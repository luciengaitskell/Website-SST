from flask import Flask, render_template, request, redirect
from file_len import file_length
import glob

@app.route('/articles/<articleNumber>/')
def main(articleNumber=None):
    if articleNumber!=None:
        fileSubfolder="articles/"
        fileBeginning="article-"
        fileExtention=".txt"
        filePath=str(fileSubfolder) + str(fileBeginning) + str(articleNumber) + str(fileExtention)

        fileIsThere=False
        for name in glob.glob(filePath):
        	fileIsThere=True
			
        if fileIsThere==False:
            redirect(/article, code=302)


        #fileSize = file_lenght(filePath) #shouldn't need this because the output of readlines is an array
        return render_template('article-render.html', filePath=filePath, fileSize=fileSize)
    else:
        return "THIS IS NOT THE FILE YOUR LOOKING FOR"



if __name__ == "__main__":
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=80
        )
