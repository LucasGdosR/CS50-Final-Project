from flask import Flask, flash, render_template, request
import numpy as np
from scipy.optimize import linprog
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("taco.db", check_same_thread=False)
cur = con.cursor()


@app.route("/", methods=['GET', 'POST'])
def index():
    # First access or return after result
    if request.method == 'GET' or request.form.get('return') == "Voltar":
        return render_template("index.html")

    # Use a multiple options input to determine which page to render next
    # Exact macros using database
    elif request.form.get('exactminchoice') == 'exact' and request.form.get('dbcustomchoice') == 'db':
        ingredient1 = request.form.get('db1')
        ingredient2 = request.form.get('db2')
        ingredient3 = request.form.get('db3')
        res = cur.execute('SELECT carb, prot, fat FROM taco WHERE name LIKE ?', (ingredient1,))
        macros1 = res.fetchall()
        res = cur.execute('SELECT carb, prot, fat FROM taco WHERE name LIKE ?', (ingredient2,))
        macros2 = res.fetchall()
        res = cur.execute('SELECT carb, prot, fat FROM taco WHERE name LIKE ?', (ingredient3,))
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
            if X[i] < 0:
                return render_template('negative.html')
            X[i] = round(float(X[i] * 100))
        return render_template('dbexact.html', weight1=int(X[0]), weight2=int(X[1]), weight3=int(X[2]), carbstarget=carbstarget, proteintarget=proteintarget, fatstarget=fatstarget, ingredient1=ingredient1, ingredient2=ingredient2, ingredient3=ingredient3)
    
    # Calorie target using database
    elif request.form.get('exactminchoice') == 'min' and request.form.get('dbcustomchoice') == 'db':
        ingredient1 = request.form.get('db1')
        ingredient2 = request.form.get('db2')
        ingredient3 = request.form.get('db3')
        res = cur.execute('SELECT kcal, prot, fat FROM taco WHERE name LIKE ?', (ingredient1,))
        macros1 = res.fetchall()
        res = cur.execute('SELECT kcal, prot, fat FROM taco WHERE name LIKE ?', (ingredient2,))
        macros2 = res.fetchall()
        res = cur.execute('SELECT kcal, prot, fat FROM taco WHERE name LIKE ?', (ingredient3,))
        macros3 = res.fetchall()
        caloriestarget = int(request.form.get('calories'))
        proteintarget = int(request.form.get('protein'))
        fatstarget = int(request.form.get('fats'))
        # https://stackoverflow.com/questions/48966934/solve-a-system-of-linear-equations-and-linear-inequalities
        # P >= PT, F >= FT, kcal = kcalT, weights >= 0, weight1 max
        coefficients_inequalities = [[-float(macros1[0][1]), -float(macros2[0][1]), -float(macros3[0][1])], [-float(macros1[0][2]), -float(macros2[0][2]), -float(macros3[0][2])]]  # require -1*x + -1*y <= -180
        constants_inequalities = [-proteintarget, -fatstarget]
        coefficients_equalities = [[float(macros1[0][0]), float(macros2[0][0]), float(macros3[0][0])]]
        constants_equalities = [caloriestarget]
        coefficients_max_1 = [-1, 0, 0]
        res = linprog(coefficients_max_1,
              A_ub=coefficients_inequalities,
              b_ub=constants_inequalities,
              A_eq=coefficients_equalities,
              b_eq=constants_equalities)
        if res.success == False:
            return render_template('negative.html')
        return render_template('dbmin.html', weight1=round(res.x[0] * 100), weight2=round(res.x[1] * 100), weight3=round(res.x[2] * 100), caloriestarget=caloriestarget, proteintarget=proteintarget, fatstarget=fatstarget, ingredient1=ingredient1, ingredient2=ingredient2, ingredient3=ingredient3)
    
    # Exact macros with custom foods
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
                return render_template('negative.html')
            X[i] = round(float(X[i] * weight[i]))
        return render_template('customexact.html', weight1=int(X[0]), weight2=int(X[1]), weight3=int(X[2]), carbstarget=carbstarget, proteintarget=proteintarget, fatstarget=fatstarget)
    
    # Calorie target with custom foods
    elif request.form.get('exactminchoice') == 'min' and request.form.get('dbcustomchoice') == 'custom':
        weight = [int(request.form.get('weight1')), int(request.form.get('weight2')), int(request.form.get('weight3'))] 
        calories = [int(request.form.get('carbs1')), int(request.form.get('carbs2')), int(request.form.get('carbs3'))]
        protein = [int(request.form.get('protein1')), int(request.form.get('protein2')), int(request.form.get('protein3'))]
        fats = [int(request.form.get('fats1')), int(request.form.get('fats2')), int(request.form.get('fats3'))]
        caloriestarget = int(request.form.get('calories'))
        proteintarget = int(request.form.get('protein'))
        fatstarget = int(request.form.get('fats'))
        coefficients_inequalities = [[-protein[0], -protein[1], -protein[2]], [-fats[0], -fats[1], -fats[2]]]
        constants_inequalities = [-proteintarget, -fatstarget]
        coefficients_equalities = [calories]
        constants_equalities = [caloriestarget]
        coefficients_max_1 = [-1, 0, 0]
        res = linprog(coefficients_max_1,
              A_ub=coefficients_inequalities,
              b_ub=constants_inequalities,
              A_eq=coefficients_equalities,
              b_eq=constants_equalities)
        if res.success == False:
            return render_template('negative.html')
        return render_template('custommin.html', weight1=round(res.x[0] * weight[0]), weight2=round(res.x[1] * weight[1]), weight3=round(res.x[2] * weight[2]), caloriestarget=caloriestarget, proteintarget=proteintarget, fatstarget=fatstarget)

    # If the options aren't selected
    else:
        return render_template('options.html')