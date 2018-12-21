from flask import Blueprint, redirect, url_for, render_template, make_response
from application.models import BlogPost, Tag, UserProfile
from application import db
from sqlalchemy.sql import or_
from urllib.parse import quote

blogs_blueprint = Blueprint('blogs', __name__, template_folder='templates')

@blogs_blueprint.route("/tags")
@blogs_blueprint.route("/tags/")
@blogs_blueprint.route("/tags/<tag_path>")
def tags(tag_path=None):
    # assume custom title, try to translate to user_id, if it fails treat blog id as a user id
    if tag_path:
        source_tag = Tag.query.filter(Tag.tag_path == tag_path).one_or_none()

        if not source_tag:
            abort(404)
        #get all posts with the tag
        all_posts = BlogPost.query.filter(BlogPost.public=="True").all()
        if all_posts: 
            with_tag = [p for p in all_posts if source_tag in p.tags]
            if with_tag:
                blog_paths = []
                for post in with_tag:
                    source_user = UserProfile.query.filter(UserProfile.id == post.user_id).one_or_none()
                    blog_path = source_user.custom_blog_path
                    blog_paths.append(blog_path)
                # return template
                return render_template("tag_main.html", with_tag=with_tag, source_tag=source_tag, blog_paths=blog_paths)
            else:
                #return template
                return render_template("tag_main.html", with_tag=[], source_tag=source_tag, blog_paths=[])
        else:
            #return template
            return render_template("tag_main.html", with_tag=[], source_tag=source_tag, blog_paths=[])      
    else:    
        #get all tags 
        all_tags = Tag.query.all()
        all_posts = BlogPost.query.filter(BlogPost.public=="True").all()
        #count blog posts for each user/blog and get 
        post_counts = []
        for tag in all_tags:
            post_count = len([i for i in all_posts if tag in i.tags])
            post_counts.append(post_count)
        
        #return template
        return render_template("all_tags.html", all_tags=all_tags, post_counts=post_counts)

@blogs_blueprint.route("/blogs")
@blogs_blueprint.route("/blogs/")
@blogs_blueprint.route("/blogs/<blog_id>")
@blogs_blueprint.route("/blogs/<blog_id>/")
@blogs_blueprint.route("/blogs/<blog_id>/posts")
@blogs_blueprint.route("/blogs/<blog_id>/posts/")
@blogs_blueprint.route("/blogs/<blog_id>/posts/<post_id>")
def blogs(blog_id=None, post_id=None):
    # assume custom title, try to translate to user_id, if it fails treat blog id as a user id
    if blog_id:
        source_user = UserProfile.query.filter(or_(UserProfile.id == blog_id, UserProfile.custom_blog_path==quote(blog_id))).filter(BlogPost.public=="True").one_or_none()
        
        if not source_user:
            abort(404)
        if post_id:
            # look up by path or id
            this_post = BlogPost.query.filter(or_(BlogPost.id == post_id, BlogPost.post_path == quote(post_id))).filter(BlogPost.public=="True").one_or_none()
            if not this_post:
                abort(404)
            return render_template("blog_post.html", this_post=this_post, source_user=source_user)
            
        else:
            all_posts = BlogPost.query.filter(BlogPost.user_id == source_user.id).filter(BlogPost.public=="True").all()
            if not all_posts:
                # return template
                return render_template("blog_main.html", all_posts=[], source_user=source_user)
            else:
                #return template
                return render_template("blog_main.html", all_posts=all_posts, source_user=source_user) 
    else:
        #get titles and urls of all user blogs 
        bloggers = UserProfile.query.all()
        
        #count blog posts for each user/blog
        blog_counts = []
        for blogger in bloggers:
            post_count = len(BlogPost.query.filter(BlogPost.user_id == blogger.id).filter(BlogPost.public=="True").all())
            blog_counts.append(post_count)
        #return template
        return render_template("all_blogs.html", bloggers=bloggers, blog_counts=blog_counts)

@blogs_blueprint.route("/feeds")
@blogs_blueprint.route("/feeds/")
@blogs_blueprint.route("/feeds/<blog_id>")
def feeds(blog_id=None):
    if blog_id:
        source_user = UserProfile.query.filter(or_(UserProfile.id == blog_id, UserProfile.custom_blog_path==quote(blog_id))).one_or_none()
        if not source_user:
            abort(404)
        all_posts = BlogPost.query.filter(BlogPost.user_id == source_user.id).filter(BlogPost.public=="True").all()
        if not all_posts:
            all_posts = []
        template = render_template('rss.xml', all_posts=all_posts, source_user=source_user)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        return response
            
    else:
        return redirect(url_for('blogs.blogs'))