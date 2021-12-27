from app import app, db
from flask import render_template, request, redirect, url_for, jsonify
from models import Post, Project
from upload_form import newProject
from flask_uploads import configure_uploads, IMAGES,  UploadSet
from flask_security import login_required
from werkzeug.utils import secure_filename
import os

images = UploadSet('images', IMAGES)
configure_uploads(app, images)


@app.route("/")
def index():
    q = request.args.get('q')

    if q:
        posts = Post.query.filter(
            Post.title.contains(q) | Post.body.contains(q))

    else:
        posts = Post.query.order_by(Post.created.desc())

    # page = request.args.get('page')
    # if page and page.isdigit():
    #     page = int(page)
    # else:
    #     page = 1

    # pages = posts.paginate(page=page, per_page=2)

    featured = posts[0]

    rest = posts[1:5]

    return render_template('index.html', featured=featured, rest=rest)


@app.route("/about")
def about():
    projects = Project.query.order_by(Project.created.desc())

    # if request.methods == "POST":

    return render_template('aboutme.html', projects=projects)


@app.route("/about-blog")
def about_blog():
    return render_template("about.html")


@app.route("/terms")
def terms():
    return render_template('terms.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/newproject', methods=["GET", "POST"])
@login_required
def newproject():
    form = newProject()

    if request.method == 'POST':
        filename = images.save(form.image.data)
        name = request.form.get('project_name')
        code_url = request.form.get('project_url')
        info_url = request.form.get('info_url')

        try:
            project = Project(project_name=name, img_path="images/uploads/" +
                              str(filename), code_url=code_url, info_url=info_url)
            db.session.add(project)
            db.session.commit()
        except:
            render_template('500.html')
        return redirect(url_for('newproject'))

    return render_template('newproject.html', form=form)

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
   

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route("/upload",methods=["POST","GET"])
# def upload():  
#     if request.method == 'POST':
#         file = request.files['file']
#         filename = secure_filename(file.filename)
          
#         if file and allowed_file(file.filename):
#            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            print('File successfully uploaded ' + file.filename + ' to static/upload')
#         else:
#            print('Invalid Uplaod only png, jpg, jpeg, gif')   
#     return jsonify(filename)