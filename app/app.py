from flask import Flask, render_template, request, redirect
import os
import pandas as pd
import re

root_dir = '/Users/aliceallafort/Google_Drive/Github/'
save_dir = root_dir + 'Miamiam/data_save/'

app = Flask(__name__)

img_dir = os.path.join('static', 'img')
app.config['img_dir'] = img_dir

app.vars = {'ingredients_kw': ''}


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['ingredients_kw'] = request.form['ingredients_kw']
        results={}
        results['ingredients_kw'] = app.vars['ingredients_kw']

        results['recipe_list'] = get_recipes(df, kw=app.vars['ingredients_kw'])
        return render_template('results.html', **results)


@app.route('/recipe_<recipe_id>')
def recipe(recipe_id):
    results = {}
    results['recipe_data'] = get_recipes(df, rec_id=recipe_id)[0]

    return render_template('recipe.html', **results)


@app.route('/home')
def home():
    full_filename = os.path.join(app.config['img_dir'], 'pexels-lukas-349609.jpg')
    template_context = dict(background = full_filename)
    return render_template('home.html', **template_context)


@app.route('/about')
def about():
    return render_template('about.html')


# FROM MATCHING STRINGS
def match_string(keywords, title, how='any'):
    found = 0
    for pattern in keywords:
        if re.search(pattern, title, re.IGNORECASE):
            if how == 'any':
                return True
            if how == 'all':
                found += 1
    if found == len(keywords):
        return True
    else:
        return False


def load_recipes():
    """Loads recipe dataframe"""
    return pd.read_json(save_dir + 'epicurious_ing_cleaned.json')
df = load_recipes()

def get_recipes(df,rec_id=None, kw=None, n=3):
    """
    Query on recipe dataframe from keyword ingredients, matching all of them
    :param ingredients_kw: List of ingredients
    :param n: Number of recipes returned
    :return: dictionary of the first N results
    """
    if kw is not None:
        kw = [k.strip() for k in kw.split(' ')]
        mask = df.ing_cleaned_all.apply(lambda t: match_string(kw, t, 'all'))
    if rec_id is not None:
        mask = df.recipe_id == int(rec_id)
    return df[mask][['recipe_id', 'title', 'ing_cleaned', 'ingredients', 'directions']].to_dict('records')[:n]


if __name__ == "__main__":
    app.run(debug=True)  # DEBUGGING
