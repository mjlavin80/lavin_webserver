from flask import Flask
import os
import sqlalchemy
from config import dbuser, dbpass

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World from Flask again"
@app.route("/setup")
def setup():
    try:
        uri = "mysql://root:%s@127.0.0.1:3306/digiped_fall_2016" % 'goblin55'
        engine = sqlalchemy.create_engine(uri) # connect to server
        a = engine.execute("SELECT * FROM test")
        test = ""
        for i in a:
            test += str(i)
        return test
    except Exception, e:
        return repr(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
