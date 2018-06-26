from flask import Flask, flash, redirect, render_template, request, session, abort

from flask import Flask

app = Flask(__name__, template_folder = 'templates')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")