# ////////////////////////////////////////////////////////
# LOGIN CONTROLLER
# ////////////////////////////////////////////////////////

from flask_app import app
from flask import render_template, session, redirect, request
from flask_app.models import login_model, recipes_model

# //// SHOW /////////////////////////////////////

@app.route('/')                                                         # Main Page
def root():
    print("******** in index *******************")
    if 'lu_id' in session:                                              # check if user is logged in
        print("User is logged in, rerouting to dashboard")
        return redirect("/dashboard")
    return render_template("index.html")

@app.route('/registration')                                             # This routh shows a sucessful registration
def registration():
    print("**** In registration Creat Login User ****")
    return render_template("registration_success.html")

# //// UTILITIES /////////////////////////////////

@app.route('/logout')                                                   # Logout User
def logout():
    del session['lu_id']
    return redirect("/")

# //// CREATE ////////////////////////////////////

@app.route('/registration/post', methods=['POST'])                      # Function that handles regisstration form data
def registration_post():
    print("**** In Registration POST ****")
    data = {
        **request.form
    }
    if not login_model.LoginUsers.validate_login_user_create_data(data):    # If a login field is invalid, redirect to root
        return redirect('/')
    
    # **** Start hashing the password ********
    pw_hash = login_model.LoginUsers.generate_password_hash(data['password'])
    data['password']=pw_hash                                            # Save the hashed password to data

    login_model.LoginUsers.create(data)                                 # Create User in the Login Database

    return redirect("/registration")

# //// RETRIEVE ////////////////////////////////////

@app.route('/login/post', methods=['POST'])                             # Function that handles log in form data
def login_post():
    print("**** In Login POST ****")
    data = {
        **request.form
    }
    print(data)
    if not login_model.LoginUsers.validate_login_user_login_data(data): # Check if login data is valid
        return redirect("/")                                            # If login is invalid, redirect to root with flash errors
    else:                                                               # Else login the user
        user = login_model.LoginUsers.get_one_by_email(data)            # Retrieve user using email
        print(user.first_name,user.last_name,user.email)
        session['lu_id'] = user.id                                      # Set Login User ID to user id

    return redirect("/dashboard")

# //// UPDATE ////////////////////////////////////



# //// DELETE ////////////////////////////////////



# //// 404 CATCH //////////////////////////////////

# **** Ensure that if the user types in any route other than the ones specified, 
#           they receive an error message saying "Sorry! No response. Try again ****
@app.errorhandler(404) 
def invalid_route(e): 
    return "Sorry! No response. Try again."