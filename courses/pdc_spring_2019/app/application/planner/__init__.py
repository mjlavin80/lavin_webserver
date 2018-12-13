from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_user
from config import ASANA_CODE, ASANA_PROJECT_ID
import requests, json, datetime
from application.models import *
from application import db

planner_blueprint = Blueprint('planner', __name__, template_folder='templates')

@planner_blueprint.route("/planner")
@planner_blueprint.route("/planner/")
@planner_blueprint.route("/planner/<baseday>")
def planner(baseday=None):
    #for debugging locally
    
    user = UserProfile.query.filter(UserProfile.id==1).one_or_none()
    db.session.add(user)
    db.session.commit()
    login_user(user, force=True)
    message="in"

    #end local debugging block
    try:
        if current_user.is_admin:
            ASANA_BASE_URL = 'https://app.asana.com/api/1.0/'
        
            h = {"Authorization": "Bearer "+ ASANA_CODE}
            r = requests.get(ASANA_BASE_URL + "projects/" + ASANA_PROJECT_ID + "/tasks", headers=h) 
            all_tasks = json.loads(r.text)['data']
            project_tasks = []

            for t in all_tasks:
                r2 = requests.get(ASANA_BASE_URL + "tasks/" + str(t['id']), headers=h)
                full_task = json.loads(r2.text)['data']
                if not full_task['completed']:
                    project_tasks.append(full_task)

            def sort_key(d):
                if d['due_on']:
                    return d['due_on']
                else:
                    return '9999-99-99'

            project_tasks = sorted(project_tasks, key=sort_key, reverse=False)
            
            if baseday:
                t = datetime.strptime(baseday, "%Y-%m-%d").date()
            else: 
                t = datetime.today().date()

            weeks = Week.query.order_by(Week.week_number).all()
            last_due = []
            next_due = []
            days_before = []
            days_after = []

            for week in weeks:
                for day in week.days:
                    try:
                        dayname = datetime.strptime(day.name, "%A, %B %d, %Y").date()
                    except:
                        dayname = t
                    if dayname >= t:
                        days_after.append(day)
                    if dayname < t:
                        days_before.append(day)

            def find_assignment(day_list, mode='before'):
                assign = 0
                due_days = []
                for day in day_list:
                    if mode == 'before' and assign == 0:
                        if len(day.assignments) > 0:
                            due_days.append(day)
                            #if found, append and change assign var to a 1
                            assign += 1
                    elif mode != 'before':
                        if len(day.assignments) > 0:
                            due_days.append(day)
                if mode == 'before':
                    due_days = due_days[-1:]
                return due_days

            last_due = find_assignment(days_before)
            next_due = find_assignment(days_after, mode='after')

            try:
                _next_three = days_after[0:3]
            except:
                _next_three = []
                fake = Day()
                fake.name = "No data to display"
                _next_three.append(fake)
            try:
                _last = days_before[-1]
            except:
                _last = Day()
                _last.name = "No data to display"
            try:
                last_due_date = last_due[0]
                days_passed = t - datetime.datetime.strptime(last_due_date.name, "%A, %B %d, %Y").date()
                days_ago = days_passed.days
            except:
                last_due_date = Day()
                last_due_date.name = "No data to display"
                fake_assignment = Assignment()
                fake_assignment.link_title = "all"
                fake_assignment.title = "No data to display"
                last_due_date.assignments.append(fake_assignment)
                days_ago = 0
            try:
                next_due_date = next_due[0]
                days_to = datetime.datetime.strptime(next_due_date.name, "%A, %B %d, %Y").date() - t
                days_to_next = days_to.days
            except:
                next_due_date = Day()
                next_due_date.name = "No data to display"
                fake_assignment = Assignment()
                fake_assignment.link_title = "all"
                fake_assignment.title = "No data to display"
                next_due_date.assignments.append(fake_assignment)
                days_to_next = 0
            

            today = t.strftime("%A, %B %d, %Y").replace(" 0", " ")
            return render_template("planner.html", project_tasks=project_tasks, last=_last, next_three=_next_three, next_due_date=next_due_date, last_due_date=last_due_date, days_ago=days_ago, days_to_next=days_to_next, today=today) 
        else:
            return redirect(url_for('status'))
    except:
        return redirect(url_for('status'))