from flask import Blueprint, redirect, url_for, render_template, make_response
from application.models import NotebookPost, NotebookTag, UserProfile
from application import db

notebook_blueprint = Blueprint("notebook", __name__, template_folder="templates")

@notebook_blueprint.route("/tags")
@notebook_blueprint.route("/tags/")
@notebook_blueprint.route("/tags/<tag_path>")
def tags(tag_path=None):
    if tag_path:
        source_tag = NotebookTag.query.filter(NotebookTag.tag_path == tag_path).one_or_none()
        if not source_tag:
            redirect(url_for('notebook.tags', tag_path=None)) 
        #get all posts with the tag
        all_posts = NotebookPost.query.filter(NotebookPost.public=="True").all()
        with_tag = [p for p in all_posts if source_tag in p.tags]
   
        return render_template("tag_main.html", with_tag=with_tag, source_tag=source_tag)
              
    else:    
        #get all tags 
        all_tags = NotebookTag.query.all()
        all_posts = NotebookPost.query.filter(NotebookPost.public=="True").all()
        
        #count notebook posts for each user/notebook and get 
        post_counts = []
        for tag in all_tags:
            post_count = len([i for i in all_posts if tag in i.tags])
            post_counts.append(post_count)
        
        return render_template("all_tags.html", all_tags=all_tags, post_counts=post_counts)

@notebook_blueprint.route("/notebook")
@notebook_blueprint.route("/notebook/")
@notebook_blueprint.route("/notebook/<post_path>")
@notebook_blueprint.route("/notebook/<post_path>/")
def notebook(post_path=None):
    if post_path:
        # look up by title
        this_post = NotebookPost.query.filter(NotebookPost.post_path == post_path).filter(NotebookPost.public=="True").one_or_none()
        if not this_post:
            redirect(url_for('notebook.notebook', post_path=None)) 
        return render_template("notebook_post.html", this_post=this_post)
            
    else:
        all_posts = NotebookPost.query.filter(NotebookPost.public=="True").all()

        return render_template("notebook_main.html", all_posts=all_posts) 

@notebook_blueprint.route("/feed")
def feed():
    all_posts = NotebookPost.query.filter(NotebookPost.public=="True").all()
    template = render_template('rss.xml', all_posts=all_posts)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response