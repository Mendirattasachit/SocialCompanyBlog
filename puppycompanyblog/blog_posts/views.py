# blog_posts/views.py
from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from puppycompanyblog import db
from puppycompanyblog.models import BlogPost
from puppycompanyblog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts', __name__)


# CREATE  ############ - MAKE BLOG AND ADD TO DB

@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data,  # Create a sample Blog of BlogPost model
                             text=form.text.data,
                             user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Created')
        return redirect(url_for('core.index'))  # Redirect to Home page
    return render_template('create_post.html', form=form)


############      BLOG POST(READ)     ############
# blog_post_id is int variable!Each blog post has to have int & Unique ID
# QUERY THE DB AND RENDER ON TEMPLATE, PASSING INFO ABOUT THE BLOG TO THE TEMPLATE
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):

    # Query that ID from model ie y we kept it int
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title, date=blog_post.date, post=blog_post)


#####################      UPDATE     ###################
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    # WE DON'T WANT USER TO EDIT SOMEONE ELSE'S POST! MAKE SURE CURRENT AUTHOR IS CURRENT USER!
    blog_post = BlogPost.query.get_or_404(blog_post_id)
# GRAB A POST,CHECK FOR CORRECT USER, MAKE UPDATIONS, WRITE EXISTING BLOG AND RENDER ON TEMPLATE
    if blog_post.author != current_user:
        abort(403)  # Built-in flask method, takes error codes, ie Restricted Access

    form = BlogPostForm()
    if form.validate_on_submit():
        # Updations
        blog_post.title = form.title.data
        blog_post.text = form.text.data

        db.session.commit()
        flash('Blog Post Updated!')
        # View.View, blog_post view takes id, so we pass it here
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))

    elif request.method == 'GET':
        # USER MUST ALREADY SEE EXISTING BLOG TEXT, SO NOW HE CAN UPDATE IT, RATHER RE-WRITING ENTIRE BLOG!
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html', title='Updating', form=form)


################      DELETE     #################
@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    # GRAB A BLOG, CHECK FOR CORRECT USER, DELETE BLOG AND RENDER ON INDEX PAGE!
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    # USER CANNOT DELETE SOMEONE ELSE'S BLOG!
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()

    flash('Blog Post is Deleted!')
    return redirect(url_for('core.index'))
