import pandas as pd # work with the datasets
import numpy as np # work with the datasets
from sklearn.metrics.pairwise import cosine_similarity # calculate the cosine similiratry


def recommendation_item (user, nb_item, nb_reco, matrix, matrix_norm):
    unwatched_movie = matrix_norm[user].loc[matrix_norm[user].isna()].sort_values(ascending=False)\
                                            .reset_index()\
                                            .rename(columns={user:'pred_rating'})

    watched_movie = matrix_norm[user].loc[matrix_norm[user].notna()].sort_values(ascending=False)\
                                            .reset_index()\
                                            .rename(columns={user:'rating'})

    for movie in unwatched_movie['title']:
        movie_sim = matrix.loc[movie].reset_index()\
            .rename(columns={movie :'similarity_score'})
        movie_pred = pd.merge(watched_movie, 
                       movie_sim, 
                       on = 'title', 
                       how = 'inner'
                      )[:nb_item]


        unwatched_movie.loc[unwatched_movie['title'] == movie, 'pred_rating']=round(
                        np.average(movie_pred['rating'], 
                        weights=movie_pred['similarity_score']), 
                        6
                        )


    reco = unwatched_movie.sort_values('pred_rating', ascending=False)[:nb_reco]
    
    return reco


def cf_item_pearson(df, user):
    matrix = pd.pivot_table(df, 
                        values = ['rating'],
                        index = ['title'],
                        columns = ['userId'],
                       )
    matrix_norm = matrix.subtract(matrix.mean(axis=1), axis = 0) # normalization
    matrix_norm.columns = matrix_norm.columns.droplevel()
    
    movie_corr = matrix_norm.T.corr() # pearson correlation matrix

    nb_item = 5 # nb of item for comparison
    nb_reco = 6 # nb of recommandations
    matrix = movie_corr # matrix type for correlation
    matrix_norm = matrix_norm # based matrix for recommandations

    reco = recommendation_item (user, nb_item, nb_reco, matrix, matrix_norm)

    reco =reco.to_html(index = False)

    return reco



