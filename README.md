

<p align="center">
  <img src="https://github.com/allafort/Miamiam/blob/main/app/static/img/miamiam_logo.png"> 
</p>


I created [Miamiam](https://miamiam-project.herokuapp.com/index) a recipe recommendation engine based on what you already have at home.
The user inputs a set of ingredients they would like to use as well as preferences such as their favorite cuisine. 

Using a dataset of recipes from popular food websites (first using 20k recipes from Epicurious.com).
The engine provides a list of recipes using the maximum number of ingredients specified by the user.  
In just a single result page, each recipe is listed along with all the additional ingredients needed to prepare it. 

The  order in which the recipes  are displayed is based on the cuisine preferences selected by the user. To do that, I built a Support Vector Machine Classifier using only the ingredients of each recipe as features to identify a recipe's probability of matching those cuisine types.


This project was developped during my fellowship at [The Data Incubator](https://www.thedataincubator.com/fellowship.html).


