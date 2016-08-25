from flask import Flask
import mysql.connector as mdb

app = Flask(__name__)

@app.route("/")
def hello():
    maria_connec = mdb.connect(user='root', password='goblin55', database='digital-pedagogy')
    cursor = maria_connect.cursor()
    return "Hello World from Flask"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
