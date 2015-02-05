from flask import Flask, render_template, request
import MySQLdb
app = Flask(__name__)

@app.route('/')
def index_main():
	return "LUC'S WEBSERVER!"

@app.route('/hello/')# try /hello/ if it doesn't work
@app.route('/hello/<username>')
def hello_world(username=None):
	return render_template('hello2.html', username=username)

@app.route('/quiz')
def quiz():
	return render_template('quiz.html')

@app.route('/quiz_answers', methods=['POST'])
def quiz_answers():
	turd1=request.form.get("q1")
	turd2=request.form.get("q2")
	return "Q1: " + str(turd1) + ", Q2: " + str(turd2)

if __name__ == "__main__":
    app.debug = True
    app.run(
	host='0.0.0.0',
	port=80
	)
