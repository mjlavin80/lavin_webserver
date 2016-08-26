from flask import Flask
import os
import sqlalchemy
from config import dbuser, dbpass
app = Flask(__name__)

@app.route("/")
def hello():
    try:
        uri = "mysql://%s:%s@mysql:3306/digiped_fall_2016" % (dbuser, dbpass)
        engine = sqlalchemy.create_engine(uri) # connect to server
        a = engine.execute("SELECT * FROM test")
        test = ""
        for i in a:
            test += str(i)
        return test
    except:
        try:
            uri = "mysql://%s:%s@mysql:3306" % (dbuser, dbpass)
            engine = sqlalchemy.create_engine(uri) # connect to server
            a = engine.execute("CREATE DATABASE digiped_fall_2016 CHARACTER SET='utf8' COLLATE='utf8_general_ci'")
            return "created database. Reload to see contents."
        except Exception, e:
            return repr(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
