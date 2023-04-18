#!/usr/bin/env python
# coding: utf-8

"""Creation of the tables 'user and 'movie' in the database 'reco_syst' """

import pandas as pd
import numpy as np
from sqlalchemy import create_engine


df_movie = pd.read_csv('movies.csv')
df_ratings = pd.read_csv('ratings.csv')

"""merge df_ratings and df_movie"""


df = pd.merge(df_ratings, df_movie, on='movieId', how='inner')


"""filtering of movies under 100 ratings and movie not in our formulaire"""


topmovie = [778,
            608,
            1527,
            3000,
            2324,
            2329,
            2028,
            2858,
            3147,
            2762,
            2571,
            2959,
            3578,
            3949,
            4011,
            7022,
            5618,
            4878,
            4963,
            27368,
            6502,
            27773,
            7153,
            6874,
            6711,
            6539,
            7254,
            7361,
            32587,
            33493,
            48780,
            44191,
            51255,
            54001,
            55247,
            58559,
            63082,
            64614,
            60069,
            79132,
            60684,
            72998,
            70286,
            52319,
            76251,
            92259,
            89745,
            96079,
            99114,
            109487                    
        ]

"""Formatting and filtering of the table user before insertion in database"""

nb_ratings = pd.pivot_table(df, 
                            values=['rating'],
                            index=['movieId'],
                            aggfunc = 'count'
                           )



nb_ratings.reset_index(inplace = True)

nb_ratings = nb_ratings.loc[nb_ratings['rating'] > 100] 

df_result = df.loc[((df['movieId'].isin(nb_ratings['movieId'])) | (df['movieId'].isin(topmovie)))]

df_result.sort_values(by=['movieId'], inplace=True)

df_result['movieId'] = 'm' + df_result['movieId'].astype(str) 

matrix = pd.pivot_table(df_result, 
                        values = ['rating'],
                        index = ['userId'],
                        columns = ['movieId'],
                       )


matrix.columns = matrix.columns.droplevel()

"""Creation of new columns for the table user"""

matrix["prenom"]=""
matrix["nom"]=""
matrix["moteur"]=""

third = matrix.pop("moteur")
second = matrix.pop("prenom")
first = matrix.pop("nom")

matrix.insert(0,"moteur", third)
matrix.insert(0,"prenom", second)
matrix.insert(0,"nom", first)

matrix['userId']= np.arange(len(matrix))

"""Connection to the database reco_syst"""

url = 'mysql://root:jro35all!@localhost/recosyst'
engine = create_engine(url, echo=True)
connection = engine.connect()


"""Creation of the table user in the database"""

matrix.to_sql('user', con = engine , if_exists='replace', index= False)

"""Creation of the table movie in the database"""

df_movie['movieId'] = 'm' + df_movie['movieId'].astype(str)  # modification of the movieId
df_movie.to_sql('movie', con = engine , if_exists='replace', index= False)

