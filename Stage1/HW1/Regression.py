'''
This file contains a wrapper function for linear regression. Since scikit learn's
linear regression model doesn't return a classification but rather a number, the wrapper
will take the output and turn it into a classification.
'''

from sklearn.linear_model import LinearRegression
import numpy as np

class LinRegression:

    def __init__(self, *args, **kwargs):
        self.model = LinearRegression(*args, **kwargs)
        self.threshold = 0
        self.classes = np.array([0, 1], np.int64)

    def fit(self, X, y):
        from Eval import evaluate

        # Train the model
        self.model.fit(X, y)

        # Call sklearn's prediction function
        X.loc[:,'Reg_Preds'] = self.model.predict(X)

        # Find the best threshold
        best = 0
        best_score = 0
        preds = [[]]

        for i in range(20):
            thresh = 0 + i / 20.0
            test = X.copy()
            test.loc[:,'Label'] = y
            preds.append([])

            # Change regression predictions to classification based on threshold
            for row in test.itertuples(index=False):

                if row[len(row) - 2] > thresh:
                    preds[i].append(1)
                else:
                    preds[i].append(0)

            test.loc[:,'Prediction'] = preds[i]
            precision, recall, f1 = evaluate(test)

            if (f1+precision)/2 > best_score:
                best = i
                best_score = (f1+precision)/2

        self.threshold = 0 + best / 20.0
        return self

    def predict(self, X):
        # Call sklearn's prediction function
        x_copy = X.copy()
        x_copy.loc[:,'Reg_Preds'] = self.model.predict(x_copy)

        # Change regression predictions to classification based on threshold
        preds = []
        for row in x_copy.itertuples(index=False):
            if row[len(row) - 1] > self.threshold:
                preds.append(1)
            else:
                preds.append(0)

        return preds

    def get_params(self, deep=True):
        return self.model.get_params(deep=deep)
