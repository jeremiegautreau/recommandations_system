
from db_request import *
from reco_cf_item import *

def main():

    db, cursor = db_connect()

    df = data_request(db)

    user = user_request(cursor)

    close_connection(db, cursor)

    reco = cf_item_pearson(df, user)
    
    return reco

if __name__ == "__main__":
    main()


