import sqlite3 as sql

db_path = "path"

def insertReading(name,date,sent_value,recv_value):
    con = sql.connect(db_path+"database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO readings (name,reading_date,sent_value,recv_value) VALUES (?,?,?,?)", (name,date,sent_value,recv_value))
    con.commit()
    con.close()
    return True

def getReadingsDate(date):
    con = sql.connect(db_path+"database.db")
    cur = con.cursor()
    cur.execute("SELECT name,reading_date,sent_value,recv_value FROM readings WHERE date(reading_date) == ?", (date,))
    readings = cur.fetchall()
    con.close()
    return readings

def getReadings():
    con = sql.connect(db_path+"database.db")
    cur = con.cursor()
    cur.execute("SELECT name,reading_date,sent_value,recv_value FROM readings")
    readings = cur.fetchall()
    con.close()
    return readings

def getNames():
    con = sql.connect(db_path+"database.db")
    cur = con.cursor()
    cur.execute("SELECT DISTINCT name FROM readings")
    names = cur.fetchall()
    con.close()
    return names
