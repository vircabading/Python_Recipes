# ////////////////////////////////////////////////////////
# RECIPES CONTROLLER
# ////////////////////////////////////////////////////////

from flask_app import app
from flask import render_template, session, redirect, request
from flask import flash
from flask_app.models import login_model, recipes_model

# //// SHOW /////////////////////////////////////

# //// FORM POST /////////////////////////////////

# //// UTILITIES /////////////////////////////////

def make_sure_user_is_logged_in():
    if not 'lu_id' in session:                                              # Check if user is logged in
        print("User is not logged in, redirect to root login")
        return redirect("/")                                                # If not logged in, redirect to root login

# //// CREATE ////////////////////////////////////

@app.route('/recipes/new/post', methods=['POST'])
def recipes_new_post():
    print("**** In recipes new POST ********")
    data = {
        **request.form,
        'user_id': session['lu_id']
    }
    data['under_30_minutes'] = int(data['under_30_minutes'])
    print("data:")
    print(data)
    if not recipes_model.Recipes.is_valid_recipe_data(data):
        return redirect("/recipes/new")
    recipes_model.Recipes.create(data)
    return redirect("/dashboard")


# //// RETRIEVE ////////////////////////////////////

@app.route('/dashboard')                                                    # DASHBOARD
def Dashboard():
    print("**** In Dashboard ********")
    if not 'lu_id' in session:                                              # Check if user is logged in
        print("User is not logged in, redirect to root login")
        return redirect("/")                                                # If not logged in, redirect to root login
    data = {
        'id': session['lu_id']
    }
    user = login_model.LoginUsers.get_one(data)                             # Retrive user's info from db and make a user instance
    all_recipes = recipes_model.Recipes.get_all()                           # Retrieve all recipos in the database
    return render_template("dashboard.html", user=user, all_recipes = all_recipes )                     # Pass user's info to the Dashboard

@app.route('/recipes/<int:id>/viewinstructions')                                           # Retrive the data from one specified user
def recipes_id_viewinstructions (id):
    print ("*********** In recipes id view instructions ******************")
    if not 'lu_id' in session:                                              # Check if user is logged in
        print("User is not logged in, redirect to root login")
        return redirect("/")                                                # If not logged in, redirect to root login
    data = {
        'id': session['lu_id']
    }
    user = login_model.LoginUsers.get_one(data)                             # Retrive user's info from db and make a user instance
    
    data = {
        'id': id
    }
    recipe = recipes_model.Recipes.get_one(data)                            # Retrieve the recipe
    print("**** Testing strftime******")
    print(recipe.date_made_on.strftime("%B %d, %Y"))
    return render_template("recipes_view_instructions.html", user=user, recipe = recipe)

# **** Function that displays a form for creating a new recipe
@app.route("/recipes/new")
def recipes_new():
    if not 'lu_id' in session:                                              # Check if user is logged in
        print("User is not logged in, redirect to root login")
        return redirect("/")                                                # If not logged in, redirect to root login
    data = {
        'id': session['lu_id']
    }
    user = login_model.LoginUsers.get_one(data)                             # Retrive user's info from db and make a user instance
    return render_template("recipes_new.html", user=user)

# **** Function the creates a pre-populated FORM for Editing a Recipe
@app.route("/recipes/<int:id>/edit")
def recipes_id_edit(id):
    print("**** In recipes ID Edit Form, creation ")
    if not 'lu_id' in session:                                              # Check if user is logged in
        print("User is not logged in, redirect to root login")
        return redirect("/")                                                # If not logged in, redirect to root login
    data = {
        'id': session['lu_id']                                              # assign user id
    }
    user = login_model.LoginUsers.get_one(data)                             # Retrive user's info from db and make a user instance
    data = {
        'id': id                                                            # assign recipe id
    }
    recipe = recipes_model.Recipes.get_one(data)                            # Retrieve recipe info from the db and make a recipe instance
    if user.id != recipe.user_id:                                           # Only the creator of the recipe should be allowed to edit the recipe
        return redirect("/dashboard")
    return render_template("recipes_id_edit.html", user=user, recipe= recipe)

# **** Action JOIN *******************************
# Function: Get all of the recipes of the logged in user
@app.route('/user/recipes')
def user_recipes():
    print("**** In get all User's Recipes ********")
    if not 'lu_id' in session:                                              # Check if user is logged in
        print("User is not logged in, redirect to root login")
        return redirect("/")                                                # If not logged in, redirect to root login
    data = {                                                                # User id of the user is the Logged in User ID in session
        'id': session['lu_id']
    }
    user = login_model.LoginUsers.get_user_with_recipes(data)               # Get instance of user with all their recipes
    return render_template("user_recipes.html", user=user)

# //// UPDATE ////////////////////////////////////

@app.route("/recipes/<int:id>/edit/post", methods=['POST'])
def recipes_id_edit_post(id):
    print("*** In Recipes ID Edit POST ******")
    data = {
        **request.form,
        'id': id,
        'user_id': session['lu_id']
    }
    print("data retrieved:")
    print(data)
    if not recipes_model.Recipes.is_valid_recipe_data(data):
        return redirect (f"/recipes/{id}/edit")
    
    recipes_model.Recipes.update_one(data)

    return redirect("/dashboard")

# //// DELETE ////////////////////////////////////

@app.route("/recipes/<int:id>/delete")
def recipes_id_delete(id):                                                    # Given the recipe ID, delete the specified ID
    print("**** In Delete recipe ID ************")
    if not 'lu_id' in session:                                              # Check if user is logged in
        print("User is not logged in, redirect to root login")
        return redirect("/")                                                # If not logged in, redirect to root login
    data = {
        'id': id
    }
    recipes_model.Recipes.delete(data)                                      # Delete the specified recipe from the database
    return redirect("/dashboard")