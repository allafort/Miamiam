from flask import Flask, render_template, request, redirect
import os
import pandas as pd
import re

#root_dir = '/Users/aliceallafort/Google_Drive/Github/'
#save_dir = root_dir + 'Miamiam/data_save/'

app = Flask(__name__)

img_dir = os.path.join('static', 'img')
app.config['img_dir'] = img_dir

app.vars = {'ingredients_kw': ''}

cuisine_list_reduced = ['italian', 'moroccan', 'thai', 'french', 'southern_us', 'indian', 'greek', 'mexican',
                        'japanese']
cuisine_list_reduced_names = ['Italian', 'Moroccan', 'Thai', 'French', 'Southern', 'Indian', 'Greek', 'Mexican',
                              'Japanese']


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        form = {}
        form['cuisine_list'] = cuisine_list_reduced
        form['cuisine_list_names'] = cuisine_list_reduced_names
        return render_template('index.html', **form)
    else:
        app.vars['ingredients_kw'] = request.form['ingredients_kw']
        app.vars['cuisines_selected'] = []
        for cui in cuisine_list_reduced:
            print(cui)
            if request.form.get(cui) != None:
                print(cui, 'selected')
                app.vars['cuisines_selected'].append(cui)

        recipe_list = get_recipes(df, kw=app.vars['ingredients_kw'], cuis=app.vars['cuisines_selected'])

        results = {}
        results['ingredients_kw'] = app.vars['ingredients_kw']
        results['cuisines_selected'] = " ".join(app.vars['cuisines_selected'])
        results['recipe_list'] = recipe_list[:6]
        results['number_of_recipes'] = len(recipe_list)
        return render_template('results.html', **results)


@app.route('/recipe_<recipe_id>')
def recipe(recipe_id):
    results = {}
    results['recipe_img']=None
    results['recipe_data'] = get_recipes(df, rec_id=recipe_id)[0]
    results['recipe_id'] = recipe_id
    if recipe_id == '19016':
        results['recipe_img'] = 'https://assets.epicurious.com/photos/55d74922edfa3b005396a03a/6:4/w_620%2Ch_413/238699_salmon-chowder_6x4.jpg'
    return render_template('recipe.html', **results)


@app.route('/welcome')
def home():
    full_filename = os.path.join(app.config['img_dir'], 'welcome.png')
    template_context = dict(background=full_filename)
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
    #return pd.read_json(save_dir + 'epicurious_cuisine.json')
    return pd.read_json('../data_save/epicurious_cuisine.json')


df = load_recipes()
cuisine_list = df.cuisine.unique()


def get_recipes(df, rec_id=None, kw=None, cuis=[]):
    """
    Query on recipe dataframe from keyword ingredients, matching all of them
    :param df:
    :param rec_id: Recipe Id to retrieve a single recipe to be displayed on its page
    :param kw: List of ingredients
    :param cuis: List of cuisine selected
    :return: dictionary
    """
    mask = df.index
    if kw is not None:
        kw = [k.strip() for k in kw.split(' ')]
        mask = df.ing_cleaned_all.apply(lambda t: match_string(kw, t, 'all'))
    if rec_id is not None:
        mask = df.recipe_id == int(rec_id)
    df_sel = df[mask]
    if cuis:
        print('CUISINES',cuis,'KW',kw)
        df_sel = sort_cuis(df_sel, cuis)
    df_sel = df_sel.drop_duplicates(subset="title")
    return df_sel[['recipe_id', 'title', 'ing_cleaned', 'ingredients', 'directions', 'cuisine']].to_dict('records')


def sort_cuis(df, cuis_list):
    ind_list, ind_list_match = {}, {}
    ind_sorted = []

    for cui in cuis_list:
        ind_list_match[cui] = list(df[df.cuisine == cui].sort_values(cui, ascending=False).index)
        ind_list[cui] = list(df.sort_values(cui, ascending=False).index)

    for i in range(max([len(l) for l in ind_list_match.values()])):
        for cui in cuis_list:
            try:
                ind_sorted.append(ind_list_match[cui][i])
            except:
                pass

    for i in range(len(df.index)):
        for cui in cuis_list:
            if ind_list[cui][i] not in ind_sorted:
                ind_sorted.append(ind_list[cui][i])

    df = df.loc[ind_sorted]
    return df


if __name__ == "__main__":
    app.run(debug=True)  # DEBUGGING
