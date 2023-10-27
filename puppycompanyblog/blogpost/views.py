# blog post/views.py

from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_required
from puppycompanyblog import db
from puppycompanyblog.models import BlogPost
from puppycompanyblog.blogpost.forms import BlogPostForm
from flask import abort

blogpost = Blueprint('blogpost', __name__)

#Create
@blogpost.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blogpost = BlogPost(title=form.title.data, text=form.text.data, user_id=current_user.id)
        db.session.add(blogpost)
        db.session.commit()

        flash('Blog Post Created')

        return redirect(url_for('core.index'))
    
    return render_template('create_post.html', form=form)


#View
@blogpost.route('/<int:blog_post_id>')
def view_post(blog_post_id):
    blogpost = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blogpost.title, date=blogpost.date, post=blogpost)




#Update
@blogpost.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blogpost = BlogPost.query.get_or_404(blog_post_id)

    if blogpost.author != current_user:
        abort(403)


    form = BlogPostForm()


    if form.validate_on_submit():
        blogpost.title = form.title.data
        blogpost.text = form.text.data

        db.session.commit()
        flash('Blog Post updated')

        return redirect(url_for('blogpost.view_post', blog_post_id=blogpost.id))
    elif request.method == 'GET':
        form.title.data = blogpost.title
        form.text.data = blogpost.text

    return render_template('create_post.html', title='Updating', form=form)

#Delete
@blogpost.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
def delete(blog_post_id):

    blogpost = BlogPost.query.get_or_404(blog_post_id)

    if blogpost.author != current_user:
        abort(403)

    db.session.delete(blogpost)
    db.session.commit()
    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))