from cs50 import SQL
from flask import Flask, flash, render_template, request

app = Flask(__name__)

db = SQL("sqlite///nutritionfacts.db")


@app.route("/", methods=['GET', 'POST'])
def index():
    # First access or return after result
    if request.method == 'GET' or request.form.get('return') == True:
        return render_template("index.html")
    # Use a multiple options input to determine which page to render next
    elif request.form.get('exact/min') == 'exact' and request.form.get('db/custom') == 'db':
        return render_template('dbexact.html')
    elif request.form.get('exact/min') == 'min' and request.form.get('db/custom') == 'db':
        return render_template('dbmin')
    elif request.form.get('exact/min') == 'exact' and request.form.get('db/custom') == 'custom':
        return render_template('customexact')
    elif request.form.get('exact/min') == 'min' and request.form.get('db/custom') == 'custom':
        return render_template('custommin')
    else:
        return flash('Invalid input. Make sure to select an option: 1) database or custom foods; and 2) exact macros or minimum targets')