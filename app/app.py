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
        results = get_recipes(app.vars['ingredients_kw'])
        results['ingredients_kw'] = app.vars['ingredients_kw']
        return render_template('results.html', **results)


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


def get_recipes(ingredients_kw, n=3):
    """
    Query on recipe dataframe from keyword ingredients, matching all of them
    :param ingredients_kw: List of ingredients
    :param n: Number of recipes returned
    :return: dictionary of the first N results
    """
    df = load_recipes()
    ingredients_kw = [kw.strip() for kw in ingredients_kw.split(' ')]
    mask = df.ing_cleaned_all.apply(lambda t: match_string(ingredients_kw, t, 'all'))
    # return df[mask][['title', 'ing_cleaned']].to_dict('records')[:n]
    results = {'title0': '', 'title1': '', 'title2': ''}
    for i in range(min(n,len(df[mask].index))):
        results[list(results.keys())[i]] = df[mask]['title'].iloc[i]
    return results


if __name__ == "__main__":
    app.run(debug=True)  # DEBUGGING
