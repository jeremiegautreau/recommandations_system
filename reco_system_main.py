#! C:/Users/jerem/AppData/Local/Programs/Python/Python310/python.exe

from db_request import *
from reco_cf_item import *

def main():

    connection = db_connect()

    df = data_request(connection)

    user = user_request(connection)
    
    # user = 1

    df_movie = data_movie(connection)

    close_connection(connection)

    reco = cf_item_pearson(df, user, df_movie)

    print(reco)
    
    # return reco

if __name__ == "__main__":
    main()


