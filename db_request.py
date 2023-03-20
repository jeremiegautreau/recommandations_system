
import pandas as pd
import numpy as np
import mysql.connector as mysql

def db_connect():
    db = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "jro35all!",
        database='recosyst',
        auth_plugin='mysql_native_password'
    )


    cursor = db.cursor()

    if db.is_connected():
        print('connection sucessful')
    else:
        print ('connection failed')

    return db, cursor

def data_request(db):
    df=pd.read_sql(""" SELECT * FROM user""", con = db)

    return df

def user_request(cursor):
    cursor.execute("SELECT MAX(id) FROM user")
    user = cursor.fetchall()

    return user

def close_connection(db, cursor):
    cursor.close()
    db.close()

