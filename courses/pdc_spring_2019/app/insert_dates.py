from datetime import date, timedelta
from application import *
from application.models import Week, Day

start = date(2018, 8, 26)
end = date(2018, 12, 14)
topics = [
"Are Close and Distant Reading Equivalent?",
"Is Computational Analysis a Subset of Logical Positivism?",
"What is an Author?",
"Are Topic Models Unobtrusive Measures?",
"Is Style the Answer to Everything?",
"Do Computational Methods Find Stereotypes or Make Them?",
"Research Design",
"Data and Corpora",
"Text Processing and its Implications",
"TF-IDF and Clustering",
"Collocations and Word2Vec",
"Logistic and Linear Regression",
"NER and Place Name Recognition",
"Textual Networks",
"Visualizing Textual Material",
"Text Data and the Visual Page"
]

delta = start - end

classdays = []
week = []
for i in range(abs(delta.days + 1)):
    a = start + timedelta(days=i)
    z = a.strftime('%A, %B %d, %Y')


    if "Thursday" in z:
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
