from flask import Flask, render_template, request
import MySQLdb
import glob
app = Flask(__name__)

@app.route('/')
def hello_world():
    files=[]
    for ii in glob.glob("articles/*"):
        files.append(ii)
    return files[1]

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# FROM HERE: http://stackoverflow.com/questions/19213226/how-to-html-input-to-flask
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz_answers',methods=['POST'])
def quiz_answers():
    trud = request.form['q1']
    turd = request.form['q2']
    #q4 = request.form['q4']
    #q5 = request.form['q5']
    return trud

if __name__ == '__main__':
    app.debug = True
    app.run(
	host='0.0.0.0',
	port=80
	)
