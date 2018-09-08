import json
import requests
from difflib import get_close_matches
from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Dictionary.html')

data = json.load(open("076 data.json"))
@app.route('/check/<w>')
def check(w):
    w = w.lower()
    if w in data:
        wo = data[w]
        return render_template('word.html', result = wo, word = w)

    elif w.title() in data:
        wo = data[w.title()]
        return render_template('word.html', result = wo, word = w.title())

    elif w.upper() in data:
        wo = data[w.upper()]
        return render_template('word.html', result = wo, word = w.upper())

    elif len(get_close_matches(w,data.keys()))>0:
        q = len(get_close_matches(w,data.keys()))
        wo = get_close_matches(w,data.keys())[0]
        k = data[wo]
        return render_template('word.html', result = k, like_word = wo, flag = q)
    else:
        p = "The word doesn't exist, please double check it."
        return render_template('word.html', error = p, word = w)

@app.route('/dict', methods = ['GET','POST'])
def dict():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('check', w = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('check', w = user))

if __name__ == "__main__":
    app.run(debug = True)
