
import pandas as pd
import numpy as np
import mysql.connector as mysql
from sqlalchemy import create_engine, text


def db_connect():
    """ connection with database 'recosyst' """
    
    url = 'mysql+pymysql://root:jro35all!@localhost/recosyst'
    engine = create_engine(url)
    connection = engine.connect()

    return connection 

def data_request(connection):
    """Get all data from 'user' table
        :param connection: cursor to query the database"""

    query = text('SELECT * FROM user') 
    df=pd.read_sql_query(sql = query, con = connection)

    df.drop(columns= ['nom', 'prenom', 'moteur'], inplace= True)
    df.set_index('userId', inplace=True)

    return df

def user_request(connection):
    """Get the userId of the user for the recommandation
        :param connection: cursor to query the database"""

    query =connection.execute(text("SELECT MAX(userId) FROM user"))
    user =query.fetchone()

    return user[0]

def moteur_request(connection):
    """Get the engine choice of the user for the recommandation
        :param connection: cursor to query the database"""

    query =connection.execute(text("SELECT moteur FROM user WHERE userId = (SELECT MAX(userId) from user)"))
    moteur =query.fetchone()

    return moteur[0]

def data_movie(connection):
    """Get movies data from 'movie' table
        :param connection: cursor to query the database"""

    query = text('SELECT * FROM movie') 
    df=pd.read_sql_query(sql = query, con = connection)

    return df

def close_connection(connection):
    """Close connection with recosyst databse
        :param connection: cursor to query the database"""
    
    connection.close()
    
if __name__ == '__main__':
    pass
