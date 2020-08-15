# -*- coding: utf-8 -*-
"""c9:data_mining_techniques_used_in_recommender_systems.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UTrfj1JfPSMo52T6tTXPs3V9Q67zJ7OD
"""

from sklearn.metrics.pairwise import paired_euclidean_distances
X = [[0, 1, 2, 3]]
Y = [[1, 2, 3, 4]]

paired_euclidean_distances(X, Y)

from sklearn.metrics.pairwise import paired_manhattan_distances
X = [[0, 1, 2, 3]]
Y = [[1, 2, 3, 4]]

paired_manhattan_distances(X, Y)

movie_a = [0, 2, 1, 3] # user_id’s who bought the movie a
movie_b = [0, 1, 2, 3] # user_id’s who bought the movie b

def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection / union)

movie_a = [0, 2, 1, 3] # user_id’s who bought the movie a
movie_b = [0, 1, 2, 3] # user_id’s who bought the movie b

print(jaccard_similarity(movie_a, movie_b))

from sklearn.metrics.pairwise import cosine_similarity
X = [[0, 1, 2, 3]]
Y = [[1, 2, 3, 4]]

cosine_similarity(X, Y)

from scipy.stats import pearsonr

# two correlated vectors
X = [1, 2, 3, 4, 5]
Y = [2, 4, 6, 8, 10]

corr, p_value = pearsonr(X, Y)
print(corr)      # 1.0
print(p_value)   # 0.0

# two uncorrelated vectors
X = [1, 2, 3, 4, 5]
Y = [5, 6, 5, 6, 5]

corr, p_value = pearsonr(X, Y)
print(corr)      # 0.0
print(p_value)   # 1.0
