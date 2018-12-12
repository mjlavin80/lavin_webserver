from application.models import *
from application import db

#helper function for decorator to pass global info to templates
def generate_site_data():
    basics = Basics.query.first()
    return basics

#app context processor for sitewide data. Use as a decorator @include_site_data after @app.route to include a variable called basics in rendered template
def include_site_data(fn):
    @planner_blueprint.context_processor
    def additional_context():
        #site_basics
        basics = generate_site_data()
        #user_authorization

        return {"basics":basics}
    return fn