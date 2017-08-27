from datetime import date, timedelta
from application import *
from application.models import Week, Day

start = date(2017, 8, 28)
end = date(2017, 12, 10)
topics = [
"From Papyri to Print",
"From Papyri to Print",
"From Papyri to Print",
"From Papyri to Print",
"From Papyri to Print",
"Rise of the Machines",
"Rise of the Machines",
"Rise of the Machines",
"Rise of the Machines",
"Rise of the Machines",
"The Disembodied Book",
"The Disembodied Book",
"The Disembodied Book",
"The Disembodied Book",
"The Disembodied Book",
]

delta = start - end

classdays = []
week = []
for i in range(abs(delta.days + 1)):
    a = start + timedelta(days=i)
    z = a.strftime('%A, %B %d, %Y')


    if "Tuesday" in z or "Thursday" in z:
        week.append(z)
    if "Sunday" in z:
        classdays.append(week)
        week = []

classdays.append(week)


for i,j in enumerate(classdays):
    week_num = i+1
    days = j

    #create week object by week number, plus a draft topic
    wk = Week(week_number=week_num, week_topic=topics[i])
    #commit
    db.session.add(wk)
    db.session.commit()
    #get week id by number
    wk = db.session.query(Week).filter(Week.week_number==week_num).one_or_none()
    #create days with week ids and names
    for y in days:
        dy = Day(name=y, week_id=wk.id)
        #commit
        db.session.add(dy)
        db.session.commit()
