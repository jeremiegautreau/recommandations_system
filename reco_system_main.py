#! C:/Users/jerem/AppData/Local/Programs/Python/Python310/python.exe

from db_request import *
from reco_cf_item import *

def main():

    connection = db_connect()

    df = data_request(connection)

    user = user_request(connection)

    moteur = moteur_request(connection)

    df_movie = data_movie(connection)

    close_connection(connection)

    if moteur == 'fc_item':
        reco = cf_item_pearson(df, user, df_movie)
    elif moteur == 'fc_user':
        reco = cf_user_cos (df, user, df_movie)
    elif moteur == 'knn':
        reco = reco_item_knn (df, user, df_movie)
    

    print(reco)


if __name__ == "__main__":
    main()


