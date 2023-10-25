#views. py -> user folder
from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_user, current_user, logout_user, login_required
from puppycompanyblog import db
from puppycompanyblog.models import User, BlogPost
from puppycompanyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from puppycompanyblog.users.pictures_handler import add_profile_pic

users = Blueprint('users', __name__)

# REGISTER
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username = form.username.data, password = form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


# LOGIN
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #if nothing
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Log in Success!')

            #if user visits a page that requires login, and they are not logged in, then they will be redirected to the login page
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html', form=form)

#LOGOUT
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index')) # we cannot say index since it is using a blueprint.


# ACCOUNT page(update blogpost)
#Important...
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)

            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET': #if they are not submmiting anything we are grabbing the current username and email
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html',profile_image=profile_image, form=form)

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int) # to cycle through the pages
    user = User.query.filter_by(username=username).first_or_404()
    # .paginate allows us to have pages and per page 5 blogs.
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)



# user's list of Blog Post