from flask import Flask, render_template, request
from file_len import file_length
import glob

@app.route('/articles/<articleNumber>/')
def main(articleNumber=None):
	fileBeginning="article-"
	fileExtention=".txt"
	fileName= str(fileBeginning) + str(articleNumber) + str(fileExtention)
		


if __name__ == "__main__":
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=80
        )
