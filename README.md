# MACROS INTO MEAL
#### Video Demo: <URL HERE>
#### Description:
## What the Project *Is*
"Macros into Meal" is a web-based application that ultimately tells the user how many grams of 3 different foods are needed to meet nutrition targets set by the user.

### How to interact with it
There are four varying functionalities, which can by combined two at a time, yielding four different cases to interact with the application. The functionalities are: 1.1) choosing foods from a database; or 1.2) inputing custom nutrition information; and 2.1) choosing exact carbohydrate, protein and fat targets; or 2.2) choosing an exact calorie target, minimum protein and fat targets, and a preferred food to eat as much as possible, given the targets.

The user can choose:
**(1.1 + 2.1):** selecting foods from a database and setting exact carbohydrate, protein and fat targets. Example: they set the targets to 100g of carbs, 40g of protein, and 20g of fat, and choose 'White rice, cooked', 'Chicken Breast, Skinless, cooked', and 'Butter, salted'. The application tells them they need 356g of rice, 98g of chicken breast, and 20g of butter.

**(1.2 + 2.1):** inputing custom nutrition information and setting exact carbohydrate, protein and fat targets. Example: they set the targets to 100g of carbs, 40g of protein, and 20g of fat, and input portion size, carbohydrate grams per portion, protein grams per portion, and fat grams per portion. Example: if their input corresponded to the same nutrition facts as rice, chicken, and butter, the application would return the same weights as the previous example. If the nutrition facts were different, it would return different weights.

**(1.1 + 2.2):** selecting foods from a database and setting an exact calorie target, minimum protein and fat targets, and a preferred food to eat as much as possible. Example: they set the targets to 1.000kcal, 40g of protein, and 20g of fat, and choose 'Egg noodles, raw' as their preferred ingredient, and 'Beef, chuck, cooked', and 'Olive oil' as their secondary ingredients. The application tells them they can eat 211g of pasta (weighed before cooking, since it's raw), 69g of chuck, and 8g of olive oil. If their preferred ingredient was chuck, it would instead tell them to eat 472g of chuck, since it meets both the protein and fat targets, and has 1.000kcal.

**(1.2 + 2.2):** inputing custom nutrition information and setting an exact calorie target, minimum protein and fat targets, and a preferred food to eat as much as possible. Its use is similar to the previous example, except it takes in custom foods which might not be in the database, such as a recipe combining multiple ingredients.

### Nutrition science
There's an acronym in the fitness industry that's supposed to empower people, letting them choose their own preferred foods instead of relying on generic 'diet foods' such as chicken, rice, broccoli, tilapia, etc. It's 'If It Fits Your Macros' (IIFYM). In a nutshell, it's the concept that eating the same ammount of macronutrients (namely: carbohydrates, protein, and fats) largely results in the same body composition changes, regardless of the actual food eaten. There's a lot more to nutrition than body composition and macronutrients, but it's an important concept for flexible dieting.

Unfortunately, giving someone a list of daily macronutrients and telling them to hit those numbers is often overwhelming to a person with no previous familiarity with nutrition. I hope this app helps bridge the gap, so more people can have a more flexible diet and still reach their goals.

The next time someone needs to figure out what a meal of 100g of carbs, 40g of protein, and 15g of fat looks like, they can just input their preferred ingredients, and know exactly how much to each of each food.

Another approach is to count calories and protein, or calories, protein and fats, as carbohydrates are non-essential. If someone wants to count calories and protein only, but has trouble figuring out what is an acceptable portion of a protein source, the application can help with that too.

DISCLAIMER: this app is not nutrition advice. Consult with a registered dietitian before starting a diet. There is more to nutrition than merely macros.

## The Actual Code
As CS50x's final project, I wanted to include everything I had learned. As such, I've included HTML, CSS, JS (including jquery), python, and SQL, using the flask framework.

There's a landing page rendered when the application is accessed via GET. This page has some HTML radio inputs, which then create other inputs via Javascript depending on the options selected. If the user selects the option to use the database, there's Javascript for the input textbox, which autocompletes with one of the hundreds of options in the database. The list with the options was hardcoded in a script.

After the user has filled all of the inputs and sent them via POST, there's some python action in the backend. First, the application checks which options were selected, and there's a different algorithm for each combination, plus an error page if none of them are selected. The HTML value of certain elements are used to check this. Then, if the database method was selected, there's a SQL query to find out the nutrition facts of the selected foods. Otherwise, the nutrition facts are got from the HTML value of the inputs. Then, the actual math problem is a lot different between the two remaining options, choosing exact macronutrient targets, or an exact calorie target plus macronutrient minimums. In the first scenario, it's a linear system with three variables (the ammounts of each food), and three equations (the macronutrient targets). This was solved using numpy, with a matrix inversion. The second scenario involves optimization, since there's only one equation (the calorie target), three variables (the ammounts of each food), and six restrictions (all three ammounts are non-negative, protein is greater than protein target, fat is greater than fat target, there's as much of the preferred ingredient as possible). This was solved using scipy, specifically optimization and linear programming.

With the quantities calculated, each option renders a slightly different HTML page telling the user how much of each food is necessary to reach their targets. If the quantities are negative, or the optimization returns failure, a different page is rendered explaining to the user how to fix that (choosing ingredients with a more specialized macronutrient profile, or choosing bigger macronutrient targets).

### Javascript: deeper dive
Javascript was one of the limitations that made me change the application from english to portuguese. Initially I grabbed a database with over 8.000 foods, but the autocomplete function was too slow. In the end I decided to make the application using local nutrition facts from *TACO (Tabela Brasileira de Composição de Alimentos)*, which has less than 600 foods, and with shorter names, leading to a much faster user experience. This script is really long due to the hardcoded list of foods, and was separated in *foods.js*.

The other major instance of Javascript is related to making the input fields dynamic. Some HTML elements called JS functions onclick. These functions used DOM (specifically document.querySelector) to change some elements' type into number, text, or hidden, making inputs that were invisible appear, or showing hiding previously visible inputs. They also changed the innerHTML of other paragraph elements, showing instructions based on the options selected. Finally, based on the options selected, they changed the value of an invisible HTML element that was only used by the backend, which informed it of the options selected via flask's "request.form.get()".

Finally, Javascript was used to import data from the python return statements. It was used to get how much of each ingredient, what were the targets, and what were the selected foods.

### Python: deeper dive
Python was used to get the user's input using "request.form.get()". This enabled the application to figure out which two of the four options were selected.

The next step was either getting the nutrition facts the user input, or getting the names of the foods to get the nutrition facts directly from the database. SQLite3 was used to connect with the database, and then a cursor was used to SELECT carbs, prot, fat FROM taco WHERE name LIKE ?. The results were fetched and stored.

At this point, the application knows the macronutrient and calorie targets, and the nutrition facts. All that's left is to solve.

In the case of exact macro targets, we have the following equations:
```
carb_target = weight1 * food1.carbs + weight2 * food2.carbs + weight3 * food3.carbs;
prot_target = weight1 * food1.prot + weight2 * food2.prot + weight3 * food3.prot;
fat_target = weight1 * food1.fat + weight2 * food2.fat + weight3 * food3.fat;
```
In which the only unknowns are the weights. The macros can be written in a 3x3 matrix, which can then be inverted using "numpy.linalg.inv()", and then multiplied by the vector of macronutrient targets, yielding the resulting weights of each food. If they are negative, it means it isn't possible to meet those macronutrient targets with the selected foods.

In the case of an exact calorie target, with minimum protein and fat targets, and a preferred ingredient, we have the following equation and inequalities:
```
kcal_target = weight1 * food1.kcal + weight2 * food2.kcal + weight3 * food3.kcal;
prot_target <= weight1 * food1.prot + weight2 * food2.prot + weight3 * food3.prot;
fat_target <= weight1 * food1.fat + weight2 * food2.fat + weight3 * food3.fat;
```
There're also the boundaries, which require that the weights are non-negative, and the optimization requiring weight1 to be maximized. This can be solved using "scipy.optimize.linprog()". It requires a matrix with the coefficients of the inequalities, namely protein and fat content of the foods. These values need to be multiplied by -1, since the linprog method takes inequalities in the "smaller than" format, and the application uses it in the "greater than" format. The next matrix is that of the constants of the inequalities, which are the protein and fat targets, whicha are also multiplied by -1 for the same reasons. There are coefficient and constant matrices for the equation aswell, which are merely the calorie contents of the food and the calorie target. With these matrices, linprog can be used to solve. If res.success == False, the user is directed to the same page as if the results were of negative weights.

That's all there is to it. Rendering pages, getting the user's input, fetching data from the database, solving linear systems or linear optimization, and returning the solution to the page via JS.

### HTML and CSS: shallow dive
HTML and CSS were used in a simple fashion, using a table to format the whole website. The elegant "table-dark" class was used from Bootstrap, along with "table-hover" to make the sections of the site better separated. The horizontal rule tag also aided in this organization.

Other than that, CSS was used to make the couple lists used more pretty, the whole background dark, and some text white.

As for HTML, the main thing was the form of the landing page, which had some classes in order to write a shorter code, instead of selecting each individual element by id, and some onclick functions.

### Closing thoughts
I'm extremely grateful for all the team behind CS50x. I know David, Brian and Doug take the spotlight, but I wanted to thank everyone involved. This was an educational experience on a whole other level. I am really inspired to keep learning and give back. Thank you.