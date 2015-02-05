from flask import Flask, render_template, request
import MySQLdb
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz_answers', methods=['POST'])
def quiz_answers():
	turd1=request.form.get("q1")
	turd2=request.form.get("q2")
    #q1 = request.form['q1']
    #q2 = request.form['q2']
    #q4 = request.form['q4']
    #q5 = request.form['q5']
	return "Q1: " + str(turd1) + ", Q2: " + str(turd2)

if __name__ == "__main__":
    app.debug = True
    app.run(
	host='0.0.0.0',
	port=80
	)
