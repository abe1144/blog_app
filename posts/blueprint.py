from flask import Blueprint
from flask import render_template
from flask import request, url_for, redirect, jsonify, make_response
from models import Post, Tag
from .forms import PostForm
from config import Config
from app import db, app
from flask_security import login_required
from flask_uploads import configure_uploads, IMAGES,  UploadSet
from werkzeug.utils import secure_filename
import os

posts = Blueprint("posts", __name__, template_folder="templates")

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

@posts.route('/create', methods=['POST', 'GET'])
@login_required
def post_create():
    form = PostForm()

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        file = request.files.get('image')
        img_path=""
        if file:
            filename = file.filename.lower()
            _, ext = filename.split('.')
            if ext in ['jpg', 'gif', 'png', 'jpeg']:
                img_fullpath = os.path.join(Config.UPLOADED_PATH, filename)
                img_path = 'images/uploads/' + str(filename)
                file.save(img_fullpath)
        
        try:
            post = Post(title=title, body=body, img_path=img_path)
            db.session.add(post)
            db.session.commit()
        except:
            print('Error')
        return redirect(url_for('posts.post_detail', slug=post.slug))

    return render_template('posts/post_create.html', form=form)

@posts.route('/imageuploader', methods=['POST'])
@login_required
def imageuploader():
    file = request.files.get('file')
    if file:
        filename = file.filename.lower()
        _, ext = filename.split('.')
        if ext in ['jpg', 'gif', 'png', 'jpeg']:
            img_fullpath = os.path.join(Config.UPLOADED_PATH, filename)
            file.save(img_fullpath)
            return jsonify({'location' : filename})

    # fail, image did not upload
    output = make_response(404)
    output.headers['Error'] = 'Image failed to upload'
    return output


@posts.route('/')
def posts_list():
    q = request.args.get('q')

    if q:
        posts = Post.query.filter(
            Post.title.contains(q) | Post.body.contains(q))

    else:
        posts = Post.query.order_by(Post.created.desc())

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    pages = posts.paginate(page=page, per_page=2)

    return render_template('posts/posts.html', posts=posts, pages=pages)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    return render_template('posts/tag_detail.html', tag=tag)


@posts.route('/<slug>/edit', methods=["POST", "GET"])
@login_required
def post_update(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit.html', post=post, form=form)
