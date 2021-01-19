# Hold 2 Views - HOME VIEW and INFO VIEW
from flask import render_template, request, Blueprint
from puppycompanyblog.models import BlogPost

core = Blueprint('core', __name__)


@core.route('/')
def index():
    # QUERY ALL THE BLOG POSTS!
    page = request.args.get('page', 1, type=int)

    # 'BlogPost.query' fetches ALL Blogs, we want to view them in desc order of dates
    blog_posts = BlogPost.query.order_by(
        BlogPost.date.desc()).paginate(page=page, per_page=10)

    return render_template('index.html', blog_posts=blog_posts)


@core.route('/info')
def info():
    return render_template('info.html')
