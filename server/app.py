from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import models as dbHandler
import json

app = Flask(__name__)
app.config.from_envvar('CON_FLASK_SETTINGS')

def insertReading(name,date,sent_value,recv_value):
    con = sql.connect(app.config['DB_LOCATION'])
    cur = con.cursor()
    cur.execute("INSERT INTO readings (name,reading_date,sent_value,recv_value) VALUES (?,?,?,?)", (name,date,sent_value,recv_value))
    con.commit()
    con.close()
    return True

def getReadingsDate(date):
    con = sql.connect(app.config['DB_LOCATION'])
    cur = con.cursor()
    cur.execute("SELECT name,reading_date,sent_value,recv_value FROM readings WHERE date(reading_date) == ?", (date,))
    readings = cur.fetchall()
    con.close()
    return readings

def getReadings():
    con = sql.connect(app.config['DB_LOCATION'])
    cur = con.cursor()
    cur.execute("SELECT name,reading_date,sent_value,recv_value FROM readings")
    readings = cur.fetchall()
    con.close()
    return readings

def getNames():
    con = sql.connect(app.config['DB_LOCATION'])
    cur = con.cursor()
    cur.execute("SELECT DISTINCT name FROM readings")
    names = cur.fetchall()
    con.close()
    return names

@app.route('/', methods=['GET'])
def home():
    readings = dbHandler.getReadings()
    return render_template('index.html', readings=readings)

@app.route('/test', methods=['GET'])
def test():
    readings = dbHandler.getReadings()
    return render_template('readings.js', readings=readings)

@app.route('/api/get_names', methods=['GET'])
def get_names():
    names = dbHandler.getNames()

    return jsonify(names), 200

@app.route('/api/get_readings', methods=['GET'])
def get_readings():
    date = request.args.get("date")
    if date:
        readings = dbHandler.getReadingsDate(date)
    else:
        readings = dbHandler.getReadings()

    return jsonify(readings), 200

@app.route('/api/add_reading', methods=['POST'])
def add_reading():
    name = request.form['name']
    date = request.form['date']
    sent_value = request.form['sent_value']
    recv_value = request.form['recv_value']
    test = dbHandler.insertReading(name, date, sent_value, recv_value)
    print(test)
    if not test:
        return jsonify({"success": False, "msg": "Could not add record"}), 500
    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(debug=1, host='0.0.0.0')
