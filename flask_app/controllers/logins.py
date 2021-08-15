from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.login import Login

bcrypt = Bcrypt(app)

@app.route("/")
def index():

    return render_template("index.html")


@app.route("/login/success")
def success_login():
    logged_in = bool(session)

    if not logged_in:
        return redirect('/')

    flash("You have successfully logged in")

    return render_template("success.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

@app.route('/register_email', methods=["POST"])
def register_email():

    if not Login.validate_user(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    
    email_check = { "email" : request.form["email"] }
    user_in_db = Login.get_by_email(email_check)

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
    # Call the save @classmethod on User
    user_id = Login.save(data)
    # store user id into session
    session['user_id'] = user_id
    return redirect('/login/success')


@app.route('/validate_email', methods=["POST"])
def validate_email():

    data = { "email_login" : request.form["email_login"] }
    user_in_db = Login.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password_login']):
        flash("Invalid Email/Password")
        return redirect("/")
    
    session['user_id'] = user_in_db.id

    return redirect('/login/success')
