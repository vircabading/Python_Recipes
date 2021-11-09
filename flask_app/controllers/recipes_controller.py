# ////////////////////////////////////////////////////////
# RECIPESCONTROLLER
# ////////////////////////////////////////////////////////

from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models import login_model, recipes_model

# //// SHOW /////////////////////////////////////



# //// FORM POST /////////////////////////////////



# //// CREATE ////////////////////////////////////



# @app.route('/post', methods=['POST'])                         # Retrieve the input values from create form
# def post():
#     print("**** In / Post Retrieval **************")
#     data = {                                                            # Create Data Dictionary from values in form
#         'name': request.form['name'],
#         'email': request.form['email'],
#         'location': request.form['location'],
#         'fav_language': request.form['fav_language'],
#         'comment' : request.form['comment']
#     }
#     print(data)

#     if not users_model.Users.validate_user_create_data(data):
#         return redirect("/")

#     id = users_model.Users.create(data)                                 # Insert User in to database
#     data['id'] = id                                                     # Memorize ID of created User

#     user = users_model.Users.get_one(data)                              # get an instance of the created user
#     ("Newly created user instance: ", user)

#     print("**** Retrieving All Users *******************")
#     all_users = users_model.Users.get_all()                             # Get all instances of users from the database
#     return render_template("user_show.html", user = user, all_users = all_users)

# //// RETRIEVE ////////////////////////////////////

@app.route('/dashboard')                                                    # DASHBOARD
def Dashboard():
    print("******** in dashboard *******************")
    if not 'lu_id' in session:                                              # Check if user is logged in
        print("User is not logged in, redirect to root login")
        return redirect("/")                                                # If not logged in, redirect to root login
    data = {
        'id': session['lu_id']
    }
    print("data:")
    print(data)
    user = login_model.LoginUsers.get_one(data)                             # Retrive user's info from db and make a user instance
    print("User:")
    print(user)
    all_recipes = recipes_model.Recipes.get_all()
    return render_template("dashboard.html", user=user, all_recipes = all_recipes )                     # Pass user's info to the Dashboard

# @app.route('/users/')
# @app.route('/users')                                                    # Read All Users Page
# def users():
#     print("**** Retrieving Users *******************")
#     all_users = users_class.Users.get_all()                             # Get all instances of users from the database
#     return render_template("read_all.html", all_users = all_users)

# @app.route('/users/<int:id>')                                           # Retrive the data from one specified user
# def users_id (id):
#     print ("*********** In users id ******************")
#     data = {
#         'id': id
#     }
#     user = users_class.Users.get_one(data)
#     return render_template("users_read_one.html", user=user)

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

