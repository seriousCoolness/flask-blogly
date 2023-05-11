"""Blogly application."""
from flask import Flask, request, redirect, render_template, flash, get_flashed_messages, session
from models import db, Users, Posts, Tags, PostTags, connect_db
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
    page_user = Users.query.get_or_404(id)
    authored_posts = page_user.posts
    return render_template('user.html', user=page_user, posts=authored_posts)


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

    user=Users.query.get_or_404(id)

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
    
    Posts.query.filter_by(user_id=id).delete()
    Users.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/')

@app.route('/posts/<int:id>')
def post_page(id):
    """Shows a specific post."""

    selected_post = Posts.query.get_or_404(id)
    return render_template('post.html', post=selected_post, author=selected_post.author)

@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def new_post_form(user_id):
    """Form for submitting new post."""
    tags = Tags.query.all()
    return render_template('post_new_form.html', id=user_id, all_tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post_submit(user_id):
    """Submits new post to database."""
    try:
        
        post=Posts(title=request.form.get('post_title'), content=request.form.get('post_content'), user_id=user_id)

        tag_ids=request.form.get('tags')
        tags = []
        for tag_id in tag_ids:
            tags.append(Tags.query.get(tag_id))

        post.tags=tags

        db.session.add(post)
        db.session.commit()

    except Exception as e:
        flash(e)
        return redirect(f'/users/{user_id}/posts/new')
    else:
        return redirect(f'/posts/{post.id}')
    
@app.route('/posts/<int:id>/edit', methods=["GET"])
def edit_post_form(id):
    """Form for editing post."""
    post=Posts.query.get_or_404(id)
    tags = Tags.query.all()

    return render_template('post_edit_form.html', post=post, all_tags=tags)

@app.route('/posts/<int:id>/edit', methods=["POST"])
def edit_post_submit(id):
    """Edits post info in database."""
    try:
        title=request.form.get('post_title')
        content=request.form.get('post_content')
        tag_ids=request.form.getlist('tags', type=int)
        
        tags = []
        for tag_id in tag_ids:
            tags.append(Tags.query.get(tag_id))

        post=Posts.query.get_or_404(id)

        post.title = title
        post.content = content
        post.tags = tags

        db.session.add(post)
        db.session.commit()

    except Exception as e:
        flash(e)
        return redirect(f'/posts/{id}/edit')
    else:
        return redirect(f'/posts/{id}')
    
@app.route('/posts/<int:id>/delete', methods=["POST"])
def delete_post(id):

    post=Posts.query.filter_by(id=id)
    post_tags=PostTags.query.filter_by(post_id=id).delete()
    post.delete()
    db.session.commit()

    return redirect('/users')

@app.route('/tags')
def all_tags():
    """Shows list of tags"""
    tags = Tags.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:id>')
def show_details(id):
    """Shows one tag."""
    tag = Tags.query.get_or_404(id)
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new', methods=["GET"])
def create_tag_form():
    """form for creating tag"""
    return render_template('tag_new_form.html')

@app.route('/tags/new', methods=["POST"])
def create_tag_submit():
    """Submits newly created tag to database."""
    
    tag=Tags(name=request.form.get('name'))

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:id>/edit', methods=["GET"])
def edit_tag_form(id):
    """form for editting tag"""
    tag=Tags.query.get_or_404(id)

    return render_template('tag_edit_form.html', tag=tag)

@app.route('/tags/<int:id>/edit', methods=["POST"])
def edit_tag_submit(id):
    """Updates editted tag in database."""
    
    tag = Tags.get_or_404(id)
    tag.name = request.form.get('name')

    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:id>/delete', methods=["POST"])
def delete_tag(id):
    Tags.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect('/tags')