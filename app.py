from flask import Flask, flash, render_template, request
import numpy as np
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("nutritionfacts.db", check_same_thread=False)
cur = con.cursor()


@app.route("/", methods=['GET', 'POST'])
def index():
    # First access or return after result
    if request.method == 'GET' or request.form.get('return') == True:
        return render_template("index.html")
    # Use a multiple options input to determine which page to render next
    elif request.form.get('exactminchoice') == 'exact' and request.form.get('dbcustomchoice') == 'db':
        ingredient1 = request.form.get('db1')
        ingredient2 = request.form.get('db2')
        ingredient3 = request.form.get('db3')
        res = cur.execute('SELECT carbohydrate, protein, fat FROM nutritionfacts WHERE name = ?', (ingredient1,))
        macros1 = res.fetchall()
        res = cur.execute('SELECT carbohydrate, protein, fat FROM nutritionfacts WHERE name = ?', (ingredient2,))
        macros2 = res.fetchall()
        res = cur.execute('SELECT carbohydrate, protein, fat FROM nutritionfacts WHERE name = ?', (ingredient3,))
        macros3 = res.fetchall()
        carbstarget = int(request.form.get('carbs'))
        proteintarget = int(request.form.get('protein'))
        fatstarget = int(request.form.get('fats'))
        # carbs = a*m1.carbs + b*m2.carbs + c*m3 carbs
        # protein = a*m1.protein + b*m2.protein + c*m3 protein
        # fats = a*m1.fats + b*m2.fats + c*m3 fats
        A = np.matrix([[float(macros1[0][0]),float(macros2[0][0]),float(macros3[0][0])],
                       [float(macros1[0][1]),float(macros2[0][1]),float(macros3[0][1])],
                       [float(macros1[0][2]),float(macros2[0][2]),float(macros3[0][2])]])
        B = np.matrix([[carbstarget],[proteintarget],[fatstarget]])
        A_inverse = np.linalg.inv(A)
        X = A_inverse * B
        for i in range(3):
            if X[i][0] < 0:
                return('negative.html')
            X[i][0] = round(float(X[i][0] * 100))
        return render_template('dbexact.html', X=X, carbstarget=carbstarget, proteintarget=proteintarget, fatstarget=fatstarget, ingredient1=ingredient1, ingredient2=ingredient2, ingredient3=ingredient3)
    elif request.form.get('exactminchoice') == 'min' and request.form.get('dbcustomchoice') == 'db':
        ingredient1 = request.form.get('db1')
        ingredient2 = request.form.get('db2')
        ingredient3 = request.form.get('db3')
#        macros1 = db.execute('SELECT calories, protein, fat FROM nutritionfacts WHERE food == ?', ingredient1)
#        macros2 = db.execute('SELECT calories, protein, fat FROM nutritionfacts WHERE food == ?', ingredient2)
#        macros3 = db.execute('SELECT calories, protein, fat FROM nutritionfacts WHERE food == ?', ingredient3)
        calories = int(request.form.get('calories'))
        protein = int(request.form.get('protein'))
        fats = int(request.form.get('fats'))
        # https://stackoverflow.com/questions/48966934/solve-a-system-of-linear-equations-and-linear-inequalities
        # Tenho que encontrar uma região em que as inequações são atendidas, determinar o ponto em que peso1 é máximo, e encontrar peso2 e peso3 correspondentes
        # P >= PT, F >= FT, kcal = kcalT, pesos >= 0, peso1 max
        #
        # carbs = a*m1.carbs + b*m2.carbs + c*m3 carbs
        # protein = a*m1.protein + b*m2.protein + c*m3 protein
        # fats = a*m1.fats + b*m2.fats + c*m3 fats
        #A = np.matrix([[macros1['calories'],macros2['calories'],macros3['calories']],
        #               [macros1['protein'],macros2['protein'],macros3['protein']],
        #               [macros1['fats'],macros2['fats'],macros3['fats']]])
        #B = np.matrix([[calories],[protein],[fats]])
        #A_inverse = np.linalg.inv(A)
        #X = A_inverse * B
        #for i in X:
        #    if X[i] < 0:
        #        return('negative.html')
        #    X[i] = round(X[i] * 100)
        return render_template('dbmin.html', X)
    elif request.form.get('exactminchoice') == 'exact' and request.form.get('dbcustomchoice') == 'custom':
        weight = [int(request.form.get('weight1')), int(request.form.get('weight2')), int(request.form.get('weight3'))] 
        carbs = [int(request.form.get('carbs1')), int(request.form.get('carbs2')), int(request.form.get('carbs3'))]
        protein = [int(request.form.get('protein1')), int(request.form.get('protein2')), int(request.form.get('protein3'))]
        fats = [int(request.form.get('fats1')), int(request.form.get('fats2')), int(request.form.get('fats3'))]
        carbstarget = int(request.form.get('carbs'))
        proteintarget = int(request.form.get('protein'))
        fatstarget = int(request.form.get('fats'))
        # carbstarget = a*carbs[0] + b*carbs[1] + c*carbs[2]
        # proteintarget = a*protein[0] + b*protein[1] + c*protein[2]
        # fats = a*fats[0] + b*fats[1] + c*fats[2]
        A = np.matrix([carbs,protein,fats])
        B = np.matrix([[carbstarget],[proteintarget],[fatstarget]])
        A_inverse = np.linalg.inv(A)
        X = A_inverse * B
        for i in range(3):
            if X[i] < 0:
                return('negative.html')
            X[i] = round(float(X[i] * weight[i]))
        return render_template('customexact.html', X=X, carbstarget=carbstarget, proteintarget=proteintarget, fatstarget=fatstarget)
    elif request.form.get('exactminchoice') == 'min' and request.form.get('dbcustomchoice') == 'custom':
        return render_template('custommin.html')
    else:
        return flash('Invalid input. Make sure to select an option: 1) database or custom foods; and 2) exact macros or minimum targets')