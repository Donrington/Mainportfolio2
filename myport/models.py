from flask import Flask
from datetime import datetime,time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TEXT
db = SQLAlchemy()

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    post_date = db.Column(db.Date, nullable=False)
    read_time = db.Column(db.String(50), nullable=True)
    author = db.Column(db.String(100), nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False)
    blog_post = db.relationship('BlogPost', backref=db.backref('comments', lazy=True))


