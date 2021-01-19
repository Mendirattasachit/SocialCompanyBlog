# users/views.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from puppycompanyblog import db
from puppycompanyblog.models import User, BlogPost
from puppycompanyblog.users.forms import LoginForm, RegistrationForm, UserUpdateForm
from puppycompanyblog.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)


# Register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(email=form.email.data,
                    username=form.username.data, password=form.password.data)  # Make a user

        db.session.add(user)
        db.session.commit()

        flash('Thanks for Registration!')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


# Login
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data).first()  # Grab user by email

        # Check correct password and user exist
        if user.check_password(form.password.data) and user is not None:
            login_user(user)

            flash('Login Success!')

            # Is user try access webpage that reqd login, if so, grab that page
            next = request.args.get('next')
            # IF NO next, redirect him to home page
            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)  # Else, redirect him to 'next'

    return render_template('login.html', form=form)
# Logout


@users.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('core.index'))


# account (update UserForm)
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UserUpdateForm()

    if form.validate_on_submit():

        if form.picture.data:  # Check if user has added a pic!
            username = current_user.username  # Grab current username
            # Pass in pic and username to function we created in picture_handler.py
            pic = add_profile_pic(form.picture.data, username)

            current_user.profile_image = pic  # Set the profile_image column of User to the pic

        current_user.username = form.username.data  # Update username
        current_user.email = form.email.data   # Update Email

        db.session.commit()
        flash('Account Updated Succesfully!')

        return redirect(url_for('users.account'))

        # User is NOT submitting anything, we're just grabbing current username and email information
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

        # rendering actual Image
    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)

    return render_template('account.html', profile_image=profile_image, form=form)


# Users list of Blog Posts
# 3 steps - Page, User, blog_posts!!!
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # Grab current page
    # Grab user OR return 404 error
    user = User.query.filter_by(username=username).first_or_404()

    # author is the backref in BlogPost model
    # Query all our blogpost where author is user and order by date in descending order
    # paginate allows us to have pages
    blog_posts = BlogPost.query.filter_by(author=user).order_by(
        BlogPost.date.desc()).paginate(page=page, per_page=5)

    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
