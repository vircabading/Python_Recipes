# ////////////////////////////////////////////////////////
# RECIPESCONTROLLER
# ////////////////////////////////////////////////////////

from flask_app import app
from flask import render_template, session, redirect, request
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
    make_sure_user_is_logged_in()
    data = {
        **request.form,
        'user_id': session['lu_id']
    }
    data['under_30_minutes'] = int(data['under_30_minutes'])
    print("data:")
    print(data)
    recipes_model.Recipes.create(data)
    return redirect("/dashboard")


# //// RETRIEVE ////////////////////////////////////

@app.route('/dashboard')                                                    # DASHBOARD
def Dashboard():
    print("**** In Dashboard ********")
    make_sure_user_is_logged_in()                                           # Make sure that the user is logged in
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
    return render_template("recipes_view_instructions.html", user=user, recipe = recipe)

# **** Function that displays a form for creating a new recipe
@app.route("/recipes/new")
def recipes_new():
    make_sure_user_is_logged_in()                                           # make sure the use is logged in
    data = {
        'id': session['lu_id']
    }
    user = login_model.LoginUsers.get_one(data)                             # Retrive user's info from db and make a user instance
    return render_template("recipes_new.html", user=user)

# //// UPDATE ////////////////////////////////////

# @app.route('/users/<int:id>/update/post', methods=['POST'])             # Update a specified user's information
# def users_id_update_post(id):
#     print ("*********** In Users ID Edit POST *****************")
#     data = {                                                            # retrieve the data from the form
#         'id': id,
#         'first_name': request.form['first_name'],
#         'last_name': request.form['last_name'],
#         'email': request.form['email']
#     }
#     users_class.Users.update_one(data)
#     return redirect('/users')

# //// DELETE ////////////////////////////////////

# @app.route('/<int:id>/delete')                                    # Delete a specified user
# def users_id_delete(id):
#     print("******** IN DELETE ********************")
#     data = {
#         'id': id
#     }
#     users_model.Users.delete(data)
#     return redirect('/users')

