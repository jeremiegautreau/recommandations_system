
import pandas as pd
import numpy as np
import mysql.connector as mysql
from sqlalchemy import create_engine, text


""" def db_connect():
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

    return db, cursor """

def db_connect():
    
    url = 'mysql+pymysql://root:jro35all!@localhost/recosyst'
    engine = create_engine(url)
    connection = engine.connect()

    return connection

# def data_request(db):
#     df=pd.read_sql(""" SELECT * FROM user""", con = db)

#     df.drop(columns= ['nom', 'prenom'], inplace= True)
#     df.set_index('userId', inplace=True) 

def data_request(connection):
    # with engine.connect().execution_options(autocommit=True) as conn:
    query = text('SELECT * FROM user') 
    df=pd.read_sql_query(sql = query, con = connection)

    df.drop(columns= ['nom', 'prenom', 'moteur'], inplace= True)
    df.set_index('userId', inplace=True)

    return df

# def user_request(cursor):
#     cursor.execute("SELECT MAX(userId) FROM user")
#     user = cursor.fetchone()

#     return user[0]

def user_request(connection):
    query =connection.execute(text("SELECT MAX(userId) FROM user"))
    # user =pd.read_sql_query (sql = query, con = connection)
    user =query.fetchone()

    return user[0]

def moteur_request(connection):
    query =connection.execute(text("SELECT moteur FROM user WHERE userId = (SELECT MAX(userId) from user)"))
    # user =pd.read_sql_query (sql = query, con = connection)
    moteur =query.fetchone()

    return moteur[0]

def data_movie(connection):
    # with engine.connect().execution_options(autocommit=True) as conn:
    query = text('SELECT * FROM movie') 
    df=pd.read_sql_query(sql = query, con = connection)

    return df

# def close_connection(db, cursor):
#     cursor.close()
#     db.close()

def close_connection(connection):
    connection.close()
    
