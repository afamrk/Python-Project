from project import app,db,socketio
from flask import render_template

@app.route('/')
def home():  # put application's code here
    return render_template('home.html')


if __name__ == '__main__':
    socketio.run(app,debug=True)
