from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'
@app.route("/sinup/")
def sign_up():
    return render_template('sinup.html')

if __name__ == '__main__':
    app.run()
