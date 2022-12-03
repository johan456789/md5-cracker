from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crack')
def crack():
    md5 = request.args.get('md5')
    # hash = hashlib.md5('123'.encode()).hexdigest()
    
    return render_template('crack.html', md5=md5)

def work_generator():
    raise NotImplementedError

