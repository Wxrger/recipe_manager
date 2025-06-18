from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'recipes.json'

# Load or initialize recipes
def load_recipes():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_recipes(recipes):
    with open(DATA_FILE, 'w') as f:
        json.dump(recipes, f, indent=4)

@app.route('/')
def index():
    recipes = load_recipes()
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<int:index>')
def view_recipe(index):
    recipes = load_recipes()
    if index < 0 or index >= len(recipes):
        return "Recipe not found", 404
    return render_template('recipe.html', recipe=recipes[index], index=index)

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        new_recipe = {
            'name': request.form['name'],
            'ingredients': request.form['ingredients'].splitlines(),
            'instructions': request.form['instructions'],
            'time': request.form['time'],
            'tags': request.form['tags'].split(',')
        }
        recipes = load_recipes()
        recipes.append(new_recipe)
        save_recipes(recipes)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:index>')
def delete_recipe(index):
    recipes = load_recipes()
    if 0 <= index < len(recipes):
        del recipes[index]
        save_recipes(recipes)
    return redirect(url_for('index'))

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # use Render's port or default to 5000
    app.run(debug=False, host='0.0.0.0', port=port)
