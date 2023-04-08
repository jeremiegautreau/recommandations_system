#! C:/Users/jerem/AppData/Local/Programs/Python/Python310/python.exe

from db_request import *
from reco_cf_item import *

def main():

    connection = db_connect() # connect to 'recosyst' database

    df = data_request(connection) # get data from user table

    user = user_request(connection) # get userId for the recommandation

    moteur = moteur_request(connection) # get recommandation engine choice from the user

    df_movie = data_movie(connection) # get movies information

    close_connection(connection) # close connection to the database

   
    if moteur == 'fc_item':  # recommandations engines functions 
        reco = cf_item_pearson(df, user, df_movie)
    elif moteur == 'fc_user':
        reco = cf_user_cos (df, user, df_movie)
    elif moteur == 'knn':
        reco = reco_item_knn (df, user, df_movie)
    

    print(reco)


if __name__ == "__main__":
    main()


