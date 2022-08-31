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

After the user has filled all of the inputs and sent them via POST, there's some python action in the backend. First, the application checks which options were selected, and there's a different algorithm for each combination, plus an error message if none of them are selected. The HTML value of certain elements are used to check this. Then, if the database method was selected, there's a SQL query to find out the nutrition facts of the selected foods. Otherwise, the nutrition facts are got from the HTML value of the inputs. Then, the actual math problem is a lot different between the two remaining options, choosing exact macronutrient targets, or an exact calorie target plus macronutrient minimums. In the first scenario, it's a linear system with three variables (the ammounts of each food), and three equations (the macronutrient targets). This was solved using numpy, with a matrix inversion. The second scenario involves optimization, since there's only one equation (the calorie target), three variables (the ammounts of each food), and six restrictions (all three ammounts are non-negative, protein is greater than protein target, fat is greater than fat target, there's as much of the preferred ingredient as possible). This was solved using scipy, specifically optimization and linear programming.

With the quantities calculated, each option renders a slightly different HTML page telling the user how much of each food is necessary to reach their targets.

### Javascript: deeper dive
Javascript was one of the limitations that made me change the application from english to portuguese. Initially I grabbed a database with over 8.000 foods, but the autocomplete function was too slow. In the end I decided to make the application using local nutrition facts from *TACO (Tabela Brasileira de Composição de Alimentos)*, which has less than 600 foods, and with shorter names, leading to a much faster user experience. This script is really long due to the hardcoded list of foods, and was separated in *foods.js*.

The other major instance of Javascript is related to making the input fields dynamic.

Finally, Javascript was used to import data from the python return statements. It was used to get how much of each ingredient, what were the targets, and what were the selected foods.

### Python: deeper dive

