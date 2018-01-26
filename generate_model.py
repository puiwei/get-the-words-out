#!/usr/bin/env python
from packages.twittercache.twitter_db import TwitterDB
import numpy as np
from sklearn import linear_model, ensemble, model_selection, base, neighbors
from sklearn.feature_extraction import DictVectorizer
from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import LinearSVR
import os.path
import dill

class ColumnSelectTransformer(base.BaseEstimator, base.TransformerMixin):

    def __init__(self, col_names):
        self.col_names = col_names  # We will need these in transform()

    def fit(self, X, y=None):
        # This transformer doesn't need to learn anything about the data,
        # so it can just return self without any further processing
        return self

    def transform(self, X):
        # Return an array with the same number of rows as X and one
        # column for each in self.col_names
        # Return a list of lists which represent the rows
        transformed = X[self.col_names].values.tolist()
        return transformed


class DictEncoder(base.BaseEstimator, base.TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # X will come in as a list of lists of list.  Return a list of
        # dictionaries corresponding to those inner lists.

        listokwdicts = []

        for i in X:
            # Use OrderedDict if order of categories matter
            kwdict = {}
            # for j in ast.literal_eval(i[0]):   #read_csv read in the lists of keywords as strings, need literal_eval to eval them as lists
            for j in i[0].split():
                # print j
                kwdict[j] = 1
            listokwdicts.append(kwdict)

        return listokwdicts


class EstimatorTransformer(base.BaseEstimator, base.TransformerMixin):

    def __init__(self, estimator):
        # What needs to be done here?
        self.estimator = estimator

    def fit(self, X, y):
        # Fit the stored estimator.
        # Question: what should be returned?
        self.estimator.fit(X, y)
        return self

    def transform(self, X):
        # Use predict on the stored estimator as a "transformation".
        # Be sure to return a 2-D array.
        return np.array(self.estimator.predict(X)).reshape(-1, 1)


class EnsembleTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, base_estimator, residual_estimators):
        self.base_estimator = base_estimator
        self.residual_estimators = residual_estimators

    def fit(self, X, y):
        self.base_estimator.fit(X, y)
        y_err = y - self.base_estimator.predict(X)
        for est in self.residual_estimators:
            est.fit(X, y_err)
        return self

    def transform(self, X):
        all_ests = [self.base_estimator] + list(self.residual_estimators)
        return np.array([est.predict(X) for est in all_ests]).T


def model(test_data):

    if os.path.exists('estimator.dill'):
        estimator = dill.load(open('estimator.dill', 'rb'))
    else:
        db = TwitterDB()
        DB_df = db.get_data_frame()
        Retweet_Ct = [t for t in DB_df['tweet_retweet_ct']]
        #kw_cst = ColumnSelectTransformer(['tweet_keywords'])

        kw_pipe = Pipeline([
            ('ColSelectTransformer', ColumnSelectTransformer(['tweet_keywords'])),
            ('DictEncoder', DictEncoder()),
            ('DictVectorizer', DictVectorizer()),  #considers HashingVectorizer or TfidfVectorizer
            #('SGDR', linear_model.SGDRegressor(random_state=42))
            #('SVR', LinearSVR(random_state=0))
            ('Ridge', linear_model.Ridge(alpha = 0.7))
        ])


        numfeatures_pipe = Pipeline([
            ('ColSelectTransformer', ColumnSelectTransformer(['user_followers_ct','user_statuses_ct','tweet_length','polarity','subjectivity','tweet_has_links'])),
            #('SGDR', linear_model.SGDRegressor(random_state=42))
            ('SVR', LinearSVR(random_state=0))
            #('Ridge', linear_model.Ridge(alpha = 0.7))
        ])

        union = FeatureUnion([
            # FeatureUnions use the same syntax as Pipelines
            ('keywords', EstimatorTransformer(kw_pipe)),
            ('numfeatures', EstimatorTransformer(numfeatures_pipe)),
        ])

        ensemble_pipe = Pipeline([
            ('full', union),
            ('ensemble', EnsembleTransformer(
                # linear_model.SGDRegressor(random_state=42),
                #LinearSVR(random_state=0),
                linear_model.Ridge(alpha = 0.7),
                #linear_model.LinearRegression(),
                (neighbors.KNeighborsRegressor(n_neighbors=5),
                 ensemble.RandomForestRegressor(min_samples_leaf=20)))),

            #('blend', linear_model.LinearRegression())
            ('blend', linear_model.Ridge(alpha = 0.7))
            #('blend', LinearSVR(random_state=0))
        ])

        ensemble_pipe.fit(DB_df, Retweet_Ct)
        dill.dump(ensemble_pipe, open('estimator.dill', 'wb'))
        estimator = ensemble_pipe

    #test_data = predictRT('ucbclaudia','Prove them wrong, #sidehustle startups are growing in #sanfrancisco!')
    #test_data = DB_df[0:10]
    #test_data = predict_df

    a = estimator.predict(test_data)
    if a[0] < 0:
        return 0
    else:
        return a[0]

#prediction = model()
#print (prediction)
