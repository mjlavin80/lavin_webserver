from flask import Flask
#import sqlalchemy
user='root'
password='goblin55'

app = Flask(__name__)

@app.route("/")
def hello():
    #engine = sqlalchemy.create_engine('mysql://%s:%s@localhost' % user, password) # connect to server
    #engine.execute("CREATE DATABASE IF NOT EXISTS digiped_fall_2016") #create db
    return "Hello World from Flask"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
