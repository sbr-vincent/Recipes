# burgers.py
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


bcrypt = Bcrypt(app)

#Login and Registration
@app.route("/")
def index():
    users = User.get_all()
    print(users)
    return render_template("index.html")

@app.route("/recipes/new")
def new_recipe():
    logged_in = bool(session)

    if not logged_in:
        return redirect('/')
    
    return render_template("create_recipe.html")

@app.route('/create_recipe', methods=["POST"])
def create_recipe():
    radio_check = None

    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    if request.form["flexRadioDefault"] == 'On':
        radio_check = "Yes"
    else:
        radio_check = "No"

    data = {
        "name": request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "flexRadioDefault" : radio_check,
        "date" : request.form["date"],
        "user_id": session['user_id']
    }

    Recipe.save(data)
    return redirect("/dashboard")

@app.route('/recipes/<recipe_id>')
def get_recipe(recipe_id):
    logged_in = bool(session)

    if not logged_in:
        return redirect('/')

    data = {
        'id': recipe_id
    }

    recipe_info = Recipe.get_one(data)

    user_data = {
        'id': session['user_id']
    }

    user_name = User.get_one(user_data)

    return render_template("instructions.html", recipe_info= recipe_info, user_name=user_name)

@app.route('/delete/<recipe_id>')
def delete_recipe(recipe_id):
    data = {
        'id': recipe_id
    }

    print(data)
    print('^^^^^^^^')

    Recipe.delete(data)

    return redirect('/dashboard')

@app.route('/edit/<recipe_id>')
def edit_recipe(recipe_id):
    logged_in = bool(session)

    if not logged_in:
        return redirect('/')

    data = {
        'id': recipe_id
    }

    edit_recipe = Recipe.get_one(data)

    return render_template('edit.html', edit_recipe= edit_recipe)

@app.route("/edit/<recipe_id>/update", methods=["POST"])
def update_recipe(recipe_id):

    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/{recipe_id}')

    if request.form["flexRadioDefault"] == 'On':
        radio_check = "Yes"
    else:
        radio_check = "No"

    data = {
        "id": recipe_id,
        "name": request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "flexRadioDefault" : radio_check,
        "date" : request.form["date"],
        "user_id": session['user_id']
    }
    Recipe.update(data)
    
    return redirect('/dashboard')

#------------------------------------------------------------------
#Login/Register classes
@app.route('/register_email', methods=["POST"])
def register_email():

    if not User.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    
    email_check = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(email_check)

    if user_in_db:
        flash("Email is already registered")
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }

    user_id = User.save(data)

    session['user_id'] = user_id

    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')


@app.route('/validate_email', methods=["POST"])
def validate_email():

    data = { "email_login" : request.form["email_login"] }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password_login']):
        flash("Invalid Email/Password")
        return redirect("/")
    
    session['user_id'] = user_in_db.id

    return redirect('/dashboard')

#Next two classes are used to see if the user has logged out and it clears the session info
@app.route("/dashboard")
def success_login():
    logged_in = bool(session)

    if not logged_in:
        return redirect('/')

    data = {
        'id': session['user_id']
    }
    print(data)
    fav_recipes = User.get_user_info(data)
    print(fav_recipes)
    print('$$$$$$$$$')

    user_name = User.get_one(data)

    return render_template("dashboard.html", fav_recipes=fav_recipes, user_name=user_name)

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
