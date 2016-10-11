from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_security import login_required
from flask_admin import Admin#, AdminIndexView, BaseView, expose
from application.models import *
from application.views import *
from flask_bcrypt import Bcrypt
from application.forms import *
from config import *
from datetime import datetime
import json

def setkeys(d):
    #build href using id
    d["more_link"] = "".join(["<a href='/resources/", str("".join([i for i in str(d["id"]) if i.isalpha() == False])), "'>Full Record</a>"])
    d["excerpt"] = "".join([" ".join(d["description"].split(" ")[:9]), " ..."])
    d["date_submitted"] = d["date_submitted"].isoformat()
    del d["id"]
    del d["_sa_instance_state"]
    return d
    
def compile_errors(form):
    errs = []
    for field, errors in form.errors.items():
        for error in errors:
            text = u"Error in the %s field - %s" % (getattr(form, field).label.text, error)
            errs.append(text)
    return errs

def handle_tags_on_submit(tag_list, ins):
    # split on commas, make sure no single tag is too long
    suggested_tags = [x.strip() for x in tag_list.split(',')]
    for a_tag in suggested_tags:
        if len(a_tag) > 30:
            return "len_error"
        else:
            # append tags to tags
            for i in suggested_tags:
                #insert
                newtag = Tag.query.filter(Tag.tagname==i).one_or_none()
                if newtag is not None:
                    ins.tags.append(newtag)
                else:
                    newtag = Tag(tagname=i)
                    db.session.add(newtag)
                    db.session.commit()
                    just_added = Tag.query.filter(Tag.tagname==i).one_or_none()
                    if newtag is not None:
                        ins.tags.append(just_added)
            return ins

def process_resource(request, _type, resource_type, _id=None,):
    tags = ""
    #instantiate form
    add_resource = AddResource(request.form)
    if request.method == 'POST':
        if add_resource.validate() or _type == "edit":
            #get from or add to db
            if _type == "submit":
                new_resource = Resource()

            elif _type == "edit":
                new_resource = Resource().query.filter(Resource.id == _id).one_or_none()
                date_sub = new_resource.date_submitted
            for field in add_resource.data.keys():
                if field != "tags":
                    try:
                        setattr(new_resource, field, add_resource.data[field])
                    except:
                        pass
            #handle tags
            new_resource = handle_tags_on_submit(add_resource.data["tags"], new_resource)
            if new_resource == "len_error":
                render_template("submit.html", status="errors", errors=['One or more tags exceeds max tag length (30 characters)'], resource_type=resource_type)

            if _type == "submit":
                new_resource.date_submitted = datetime.now()
            if _type == "edit":
                new_resource.date_submitted = date_sub
            if current_user.is_admin:
                new_resource.status = "published"
            else:
                new_resource.status = "draft"

            db.session.add(new_resource)
            db.session.commit()
            if _type == "submit":
                return render_template("submit.html", add_resource=add_resource, status="success", resource_type=resource_type)
            else:

                #return render_template("submit.html", add_resource=add_resource, status="success", resource_type=resource_type)
                new_resource = Resource().query.filter(Resource.id == _id).one_or_none()
                #convert to dictionary
                resource_dict = new_resource.__dict__
                #fill in values and pass to template
                tags = ",".join([str(i.tagname) for i in new_resource.tags])
                return render_template("submit.html", _id=_id, tags=tags, add_resource=add_resource, status="success", resource_type=add_resource.data["resource_type"], resource_dict=resource_dict)

        else:
            print "error in form"
            errors = compile_errors(add_resource)
            if _type=="submit":
                return render_template("submit.html", add_resource=add_resource, status="error", errors=errors, resource_type=add_resource.data["resource_type"])
            if _type=="edit":
                    #get values by id
                new_resource = Resource().query.filter(Resource.id == _id).one_or_none()
                #convert to dictionary
                resource_dict = new_resource.__dict__
                #fill in values and pass to template
                tags = ",".join([str(i.tagname) for i in new_resource.tags])
                return render_template("submit.html", _id=_id, tags=tags, add_resource=add_resource, status="error", errors=errors, resource_type=add_resource.data["resource_type"], resource_dict=resource_dict)

    else:
        if _type=="submit":
            return render_template("submit.html", add_resource=add_resource, resource_type=resource_type)
        if _type=="edit":
                #get values by id
            new_resource = Resource().query.filter(Resource.id == _id).one_or_none()

            #convert to dictionary
            resource_dict = new_resource.__dict__
            #fill in values and pass to template
            tags = ",".join([str(i.tagname) for i in new_resource.tags])
            return render_template("submit.html", _id=_id, tags=tags, add_resource=add_resource, resource_type=resource_dict["resource_type"], resource_dict=resource_dict)
