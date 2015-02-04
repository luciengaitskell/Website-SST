from flask import Flask, render_template, request
import MySQLdb
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

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

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz_answers', methods=['POST'])
def quiz_answers():
    q1 = request.form['q1']
    q2 = request.form['q2']
    q4 = request.form['q4']
    q5 = request.form['q5']

if __name__ == '__main__':
    app.run(host='0.0.0.0')
