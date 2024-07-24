import json, os
from os.path import basename
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from flask import * 
from flask_socketio import SocketIO, emit, join_room, leave_room
from markupsafe import escape
import re 
from flask_wtf.csrf import CSRFProtect
from myport import app,csrf,socketio
from myport.forms import *
from flask_login import login_required
from myport.models import db, BlogPost, Comment
from myport import mail
from flask_mail import Message

from sqlalchemy import func
from datetime import datetime


socketio = SocketIO(app)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    posts = BlogPost.query.all()
    return render_template('light/index.html', posts=posts)




@app.route("/HeartfulConnect/", methods=['GET', 'POST'])
def heartfulconnect():
    return render_template("light/portfolio-single-1.html", pagename='HeartfulConnect | Cybersage')

@app.route("/AmanigoTravels/", methods=['GET', 'POST'])
def amanigotravels():
    return render_template("light/portfolio-single-5.html", pagename='AmanigoTravels| Cybersage')

@app.route("/ExpenseTracker/", methods=['GET', 'POST'])
def expensetracker():
    return render_template("light/portfolio-single-7.html", pagename='Navigation | Cybersage')


@app.route("/GPS/", methods=['GET', 'POST'])
def locationtracker():
    return render_template("light/portfolio-single-8.html", pagename='GPS| Cybersage')

@app.route("/Resuglow/", methods=['GET', 'POST'])
def resuglow():
    return render_template("light/portfolio-single-6.html", pagename='ResuGlow| Cybersage')

@app.route("/Lagos/Afrobeat/", methods=["GET", "POST"])
def afrobeat():
    return render_template("light/portfolio-single-2.html", pagename='Afrobeat | Cybersage')

@app.route("/EStore/", methods=["GET", "POST"])
def estore():
    return render_template("light/portfolio-single-3.html", pagename='EStore | Cybersage')

@app.route("/Techhub/", methods=["GET","POST"])
def techhub():
    return render_template("light/portfolio-single-4.html", pagename="TechHub | Cybersage")

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def blog_single(post_id):
    # Query the specific blog post by ID
    post = BlogPost.query.get_or_404(post_id)

    if request.method == 'POST':
        name = request.form['name']
        comment_text = request.form['comment']
        # Create a new Comment object
        comment = Comment(post_id=post_id, name=name, comment=comment_text)
        # Add and commit the new comment to the database
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post', post_id=post_id))

    # Query comments for this post, ordered by comment_date descending
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.comment_date.desc()).all()
    return render_template('light/blog-single.html', post=post, comments=comments)


UPLOAD_FOLDER = 'path/to/upload/directory'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    form = BlogPostForm()
    if form.validate_on_submit():
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']
        image_url_input = request.form['image_url']  # Get the image URL input
        author = request.form['author']
        read_time = calculate_read_time(content)  # Dynamically calculate read time

        image_url = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            save_path = os.path.join(current_app.config['USER_PROFILE_PATH'], filename)
            image.save(save_path)
            image_url = url_for('static', filename=os.path.join('assets/images/profile/', filename))
        elif image_url_input:  # Use the URL input if no file is uploaded
            image_url = image_url_input

        new_post = BlogPost(title=title, content=content, image_url=image_url,
                            post_date=datetime.now(), read_time=read_time, author=author)

        db.session.add(new_post)
        db.session.commit()

        flash('Blog post created successfully!', 'success')
        return redirect(url_for('homepage'))

    return render_template('light/admin.html', form=form)



def calculate_read_time(content):
    words_per_minute = 200  # Average reading speed
    words = content.split()
    number_of_words = len(words)
    read_time_minutes = max(1, number_of_words // words_per_minute)
    return f"{read_time_minutes} min read"

from datetime import datetime

@app.route('/submit_comment/<int:post_id>', methods=['POST', 'GET'])
def submit_comment(post_id):
    # CSRF protection is already handled by Flask-WTF if set up correctly
    name = request.form.get('name')
    comment_text = request.form.get('comment')
    
    # Create a new Comment object with the current date and time
    comment = Comment(
        post_id=post_id,
        name=name,
        comment=comment_text,
        comment_date=datetime.utcnow()  # Set the current date and time
    )
    
    # Save the comment to the database
    db.session.add(comment)
    db.session.commit()
    
    flash('Your comment has been posted.', 'success')
    return redirect(url_for('blog_single', post_id=post_id))  # Redirect to the blog post page
