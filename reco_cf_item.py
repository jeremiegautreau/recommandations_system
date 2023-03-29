import pandas as pd # work with the datasets
import numpy as np # work with the datasets
from sklearn.metrics.pairwise import cosine_similarity # calculate the cosine similiratry
from sklearn.neighbors import NearestNeighbors



def recommendation_item (user, nb_item, nb_reco, matrix, matrix_norm):
    # print(matrix_norm.index)
    unwatched_movie = matrix_norm[user].loc[matrix_norm[user].isna()].sort_values(ascending=False)\
                                            .reset_index()\
                                            .rename(columns={user:'pred_rating'})

    watched_movie = matrix_norm[user].loc[matrix_norm[user].notna()].sort_values(ascending=False)\
                                            .reset_index()\
                                            .rename(columns={user:'rating'})
    

    for movie in unwatched_movie['index']:
        movie_sim = matrix.loc[movie].reset_index()\
            .rename(columns={movie :'similarity_score'})
        movie_pred = pd.merge(watched_movie, 
                       movie_sim, 
                       on = 'index', 
                       how = 'inner'
                      )[:nb_item]


        unwatched_movie.loc[unwatched_movie['index'] == movie, 'pred_rating']=round(
                        np.average(movie_pred['rating'], 
                        weights=movie_pred['similarity_score']), 
                        6
                        )


    reco = unwatched_movie.sort_values('pred_rating', ascending=False)[:nb_reco]
    
    return reco


def cf_item_pearson(df, user, df_movie):
    matrix = df.T
    """ matrix = pd.pivot_table(df, 
                        values = ['rating'],
                        index = ['title'],
                        columns = ['userId'],
                       ) """
    matrix_norm = matrix.subtract(matrix.mean(axis=1), axis = 0) # normalization
    # matrix_norm.columns = matrix_norm.columns.droplevel()
    
    movie_corr = matrix_norm.T.corr() # pearson correlation matrix
    
    # print(movie_corr.head())

    nb_item = 5 # nb of item for comparison
    nb_reco = 6 # nb of recommandations
    matrix = movie_corr # matrix type for correlation
    matrix_norm = matrix_norm # based matrix for recommandations

    pred = recommendation_item (user, nb_item, nb_reco, matrix, matrix_norm)
    

    pred_mov = pd.merge(pred, df_movie, left_on='index', right_on = 'movieId', how = 'left')

    reco =pred_mov[['title', 'genres', 'pred_rating']].to_html(index = False)

    return reco

def cf_user_cos (df, user, df_movie):

    matrix_norm = df.subtract(df.mean(axis=1), axis = 0) # normalization

    movie_cos = cosine_similarity(matrix_norm.fillna(0))
    movie_cos = pd.DataFrame(movie_cos, columns = matrix_norm.index, index = matrix_norm.index)

    item_score = {}

    user_sim = movie_cos[user].loc[movie_cos.index != user].sort_values(ascending = False)[:10]

    watched_movie = matrix_norm.loc[matrix_norm.index == user].dropna(
                                                                axis = 1,
                                                                how = 'all'
                                                                )

    watched_sim = matrix_norm.loc[matrix_norm.index.isin(user_sim.index)]\
                    .dropna(axis = 1, how = 'all')\
                    .drop(watched_movie.columns, axis = 1, errors = 'ignore')

    for i in watched_sim.columns:
        rating = watched_sim[i]

        total = 0
        count = 0

        for j in user_sim.index:
            if pd.isna(rating[j]) == False:
                score = user_sim[j]*rating[j]
                total += score
                count += 1
        item_score[i] = total / count

    item_score = pd.DataFrame(item_score.items(), 
                                  columns=['movie', 'movie_score'])

    ranked_item = item_score.sort_values(by='movie_score', 
                                               ascending=False)[:10]
    
    reco = pd.merge(ranked_item, df_movie, left_on='movie', right_on = 'movieId', how = 'left')

    reco = reco[['title', 'genres']].to_html(index=False)

    return reco


def reco_item_knn (df, user, df_movie):
    matrix = df.T

    matrix_norm = matrix.subtract(matrix.mean(axis=1), axis = 0)

    matrix_norm.fillna(0, inplace=True)

    unwatched_movie = matrix_norm[user].loc[matrix_norm[user]==0].reset_index().iloc[:,0:1]

    watched_movie = matrix_norm[user].loc[matrix_norm[user].notna()].sort_values(ascending=False)\
                                                .reset_index()\
                                                .rename(columns={user:'rating'})


    model_nn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=7, n_jobs=-1)

    model_nn.fit(matrix_norm)

    recommand = []

    for movie in watched_movie['index'][:10]:
        distances, indices = model_nn.kneighbors(matrix_norm.loc[movie,:].values.reshape(1,-1))



        for i in range(0, len(distances.flatten())):
            if i != 0:
                rec = {}
                rec['movieId'] = matrix_norm.index[indices.flatten()[i]]
                rec['distance'] =distances.flatten()[i]
                recommand.append(rec)

    result = pd.DataFrame(recommand).sort_values(by='distance')   

    result = result.drop_duplicates(subset =['movieId'])
    
    result = result.loc[result['movieId'].isin(unwatched_movie['index'])]

    reco = pd.merge(result, df_movie, left_on='movieId', right_on = 'movieId', how = 'left')
    
    reco = reco[['title', 'genres']][:5].to_html(index = False) 
    
    return reco

