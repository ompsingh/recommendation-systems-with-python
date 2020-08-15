# -*- coding: utf-8 -*-
"""c3:build_a_tiny_recommendation_engine.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vI_KX3TD798WOjKvhU9LG7itA_q-G8mv

## IMPORTING PACKAGES
"""

import numpy as np
import pandas as pd

"""## DATA SAMPLE OF MOVIE RATINGS"""

sample_rank_data = [
  {"critic": "Jack Matthews", "title": "Lady in the Water", "rating": 3.0},
  {"critic": "Jack Matthews", "title": "Snakes on a Plane", "rating": 4.0},
  {"critic": "Jack Matthews", "title": "You Me and Dupree", "rating": 3.5},
  {"critic": "Jack Matthews", "title": "Superman Returns", "rating": 5.0},
  {"critic": "Jack Matthews", "title": "The Night Listener", "rating": 3.0},
  {"critic": "Mick LaSalle", "title": "Lady in the Water", "rating": 3.0},
  {"critic": "Mick LaSalle", "title": "Snakes on a Plane", "rating": 4.0},
  {"critic": "Mick LaSalle", "title": "Just My Luck", "rating": 2.0},
  {"critic": "Mick LaSalle", "title": "Superman Returns", "rating": 3.0},
  {"critic": "Mick LaSalle", "title": "You Me and Dupree", "rating": 2.0},
  {"critic": "Mick LaSalle", "title": "The Night Listener", "rating": 3.0},
  {"critic": "Claudia Puig", "title": "Snakes on a Plane", "rating": 3.5},
  {"critic": "Claudia Puig", "title": "Just My Luck", "rating": 3.0},
  {"critic": "Claudia Puig", "title": "You Me and Dupree", "rating": 2.5},
  {"critic": "Claudia Puig", "title": "Superman Returns", "rating": 4.0},
  {"critic": "Claudia Puig", "title": "The Night Listener", "rating": 4.5},
  {"critic": "Lisa Rose", "title": "Lady in the Water", "rating": 2.5},
  {"critic": "Lisa Rose", "title": "Snakes on a Plane", "rating": 3.5},
  {"critic": "Lisa Rose", "title": "Just My Luck", "rating": 3.0},
  {"critic": "Lisa Rose", "title": "Superman Returns", "rating": 3.5},
  {"critic": "Lisa Rose", "title": "The Night Listener", "rating": 3.0},
  {"critic": "Lisa Rose", "title": "You Me and Dupree", "rating": 2.5},
  {"critic": "Toby", "title": "Snakes on a Plane", "rating": 4.5},
  {"critic": "Toby", "title": "Superman Returns", "rating": 4.0},
  {"critic": "Toby", "title": "You Me and Dupree", "rating": 1.0},
  {"critic": "Gene Seymour", "title": "Lady in the Water", "rating": 3.0},
  {"critic": "Gene Seymour", "title": "Snakes on a Plane", "rating": 3.5},
  {"critic": "Gene Seymour", "title": "Just My Luck", "rating": 1.5},
  {"critic": "Gene Seymour", "title": "Superman Returns", "rating": 5.0},
  {"critic": "Gene Seymour", "title": "The Night Listener", "rating": 3.0},
  {"critic": "Gene Seymour", "title": "You Me and Dupree", "rating": 3.5}
]

"""## LOADING AND PROCESSING DATA"""

rating_df = pd.DataFrame(sample_rank_data)

rating_df.head()

rating_df.shape

rating_df.title.unique()

rating_df.critic.unique()

rating_df.describe()

rating_df.critic.describe()

rating_df.title.describe()



"""## CREATING PIVOT MATRIX"""

pivot_table = pd.pivot_table(rating_df, index='critic',
                            columns='title', aggfunc=np.max)

pivot_table

pivot_table.columns = np.arange(6.)
pivot_table.index = pd.Index(np.arange(6.))

pivot_table = pivot_table.fillna(0)

"""## MATRIX FACTORIZATION CLASS"""

class MF():
  def __init__(self, R, K, alpha, beta, iterations):
    self.R = R
    self.num_users, self.num_items = R.shape
    self.K = K
    self.alpha = alpha
    self.beta = beta
    self.iterations = iterations
  def train(self):
    self.P = np.random.normal(scale=1./self.K, size=(self.num_users, self.K))
    self.Q = np.random.normal(scale=1./self.K, size=(self.num_items, self.K))
    self.b_u = np.zeros(self.num_users)
    self.b_i = np.zeros(self.num_items)
    self.b = np.mean(np.where(self.R != 0)[0])
    self.samples = [
      (i, j, self.R.iloc[i, j])\
      for i in range(self.num_users)\
      for j in range(self.num_items)\
      if self.R.iloc[i, j] > 0
    ]
    training_process = []
    for i in range(self.iterations):
      np.random.shuffle(self.samples)
      self.sgd()
      mse = self.mse()
      training_process.append((i, mse))
      if (i+1) % 20 == 0:
        print("Iteration: %d ; error = %.4f" % (i+1, mse))
    return training_process
  def mse(self):
    predicted = self.full_matrix()
    error = 0
    for x in range(self.num_users):
      for y in range(self.num_items):
        if self.R.iloc[x, y] != 0:
          error += pow(self.R.iloc[x, y] - predicted[x, y], 2)
    return np.sqrt(error)
  def sgd(self):
    for i, j, r in self.samples:
      prediction = self.get_rating(i, j)
      e = (r - prediction)
      self.b_u[i] += self.alpha * (e - self.beta * self.b_u[i])
      self.b_i[j] += self.alpha * (e - self.beta * self.b_i[j])
      self.P[i, :] += self.alpha * (e * self.Q[j, :] - self.beta * self.P[i,:])
      self.Q[j, :] += self.alpha * (e * self.P[i, :] - self.beta * self.Q[j,:])
  def get_rating(self, i, j):
    prediction = self.b + self.b_u[i] + self.b_i[j] + self.P[i, :].dot(self.Q[j, :].T)
    return prediction
  def full_matrix(self):
    return mf.b + mf.b_u[:,np.newaxis] + mf.b_i[np.newaxis:,] + mf.P.dot(mf.Q.T)

"""## CREATING A MATRIX FACTORIZATION RATING PREDICTOR"""

mf = MF(pivot_table, K=20, alpha=0.001, beta=0.01, iterations=500)
training_process = mf.train()

"""## COMPARE..."""

print("P x Q:")
pd.DataFrame(mf.full_matrix())

pivot_table