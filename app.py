"""Blogly application."""
from flask import Flask, request, redirect, render_template, flash, get_flashed_messages, session
from models import db, Users, connect_db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def root_reroute():
    """Takes you to the user list, which is the homepage."""
    return redirect('/users')

@app.route('/users')
def home_page():
    """Home page"""
    user_list = Users.query.all()
    return render_template('home.html', users=user_list)

@app.route("/users/<int:id>")
def user_page(id):
    """Displays the user's info."""
    return render_template('user.html', user=Users.query.get_or_404(id))


@app.route("/users/new", methods=["GET"])
def create_user_form():
    """Displays the form for creating a user."""
    return render_template('user_new_form.html')

@app.route("/users/new", methods=["POST"])
def create_user_submit():
    """Creates the user's row in the database."""
    first_name = request.form.get('first_name') if request.form.get('first_name') else ''
    last_name = request.form.get('last_name') if request.form.get('last_name') else ''
    image_url = request.form.get('image_url') if request.form.get('image_url') else ''

    user = Users(first_name="", last_name="")

    if len(first_name) <= 30 and len(first_name) > 0:
        user.first_name = first_name
    else:
        if len(first_name) > 30:
            flash("First name must be less than 30 characters long!")
        if len(first_name) == 0:
            flash("First name must not be empty!")
        return redirect(f'/usercreate')

    if len(last_name) <= 30 and len(last_name) > 0:
        user.last_name = last_name
    else:
        if len(last_name) > 30:
            flash("Last name must be less than 30 characters long!")
        if len(last_name) == 0:
            flash("Last name must not be empty!")
        return redirect(f'/usercreate')

    if len(image_url) > 0:
        user.image_url = image_url
    else:
        flash("Image URL must not be empty!")
        return redirect(f'/usercreate')

    db.session.add(user)
    try:
        db.session.commit()
    except:
        flash("Inputs must have correct format.")
        return redirect(f'/usercreate')

    return redirect(f'/users/{user.id}')



@app.route("/users/edit/<int:id>", methods=["GET"])
def edit_user_form(id):
    """Displays the form for editing a user."""
    return render_template('user_edit_form.html', user=Users.query.get_or_404(id))


@app.route("/users/edit/<int:id>", methods=["POST"])
def edit_user_submit(id):
    """Edits the user's row in the database."""
    first_name = request.form.get('first_name') if request.form.get('first_name') else ''
    last_name = request.form.get('last_name') if request.form.get('last_name') else ''
    image_url = request.form.get('image_url') if request.form.get('image_url') else ''

    user=Users.query.get(id)

    if len(first_name) <= 30 and len(first_name) > 0:
        user.first_name = first_name
    else:
        if len(first_name) > 30:
            flash("First name must be less than 30 characters long!")
        if len(first_name) == 0:
            flash("First name must not be empty!")
        return redirect(f'/users/edit/{id}')

    if len(last_name) <= 30 and len(last_name) > 0:
        user.last_name = last_name
    else:
        if len(last_name) > 30:
            flash("Last name must be less than 30 characters long!")
        if len(last_name) == 0:
            flash("Last name must not be empty!")
        return redirect(f'/users/edit/{id}')

    
    if len(image_url) > 0:
        user.image_url = image_url
    else:
        flash("Image URL must not be empty!")
        return redirect(f'/users/edit/{id}')


    db.session.add(user)
    try:
        db.session.commit()
    except:
        flash("Inputs must have correct format.")
        return redirect(f'/users/edit/{id}')

    return redirect(f'/users/{id}')



@app.route("/users/delete/<int:id>", methods=["POST"])
def delete_user(id):
    """Deletes a user."""
    Users.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/')