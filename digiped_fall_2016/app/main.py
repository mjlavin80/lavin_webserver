from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def hello():
    dbuser = 'root'
    dbpass = 'goblin55'
    dbaddr = os.getenv('DB_PORT_3306_TCP_ADDR')
    #dbdb   = os.getenv('DB_ENV_MYSQL_DATABASE','flask')

    uri = "mysql://%s:%s@mysql:3306/digiped_fall_2016" % (dbuser, dbpass)

    import sqlalchemy
    engine = sqlalchemy.create_engine(uri) # connect to server

    try:
        a = engine.execute("SELECT * FROM test")
        test = ""
        for i in a:
            test += str(i)
        return test

    except Exception, e:
        return repr(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
