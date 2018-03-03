'''
this file contains the code to evaluate a model using both cross-validation
and using a seperate test set of data.
'''

import pandas as pd
import math, random
from sklearn.model_selection import KFold, cross_val_score
from sklearn import tree, svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Performs cross validation using scikit learn's cross validation function
def cross_val(data, features, scoring):
    from Regression import LinRegression
    dt = tree.DecisionTreeClassifier()
    rf = RandomForestClassifier()
    sv = svm.SVC()
    log = LogisticRegression()
    lin = LinRegression()
    matchers = [dt, rf, sv, log, lin]
    matcher_names = ['Decision Tree', 'Random Forest', 'SVM', 'Logistic Regression', 'Linear Regression']
    rows = []
    cols = ['Classifier']

    for i, matcher in enumerate(matchers):
        # Create the iterater
        cv = KFold(10, shuffle=True, random_state=0)

        # Run the cross validation
        scores = cross_val_score(matcher, data[features], data['Label'], scoring=scoring, cv=cv)

        # Create a dataframe row to display the scores
        tuple = {}
        total = 0
        tuple['Classifier'] = matcher_names[i]
        for j, score in enumerate(scores):
            tuple['Run ' + str(j+1)] = score
            total += score

            # Create dataframe columns on first run
            if i == 0:
                cols.append('Run ' + str(j+1))
        tuple['Average'] = float(total) / len(scores)
        rows.append(tuple)

    cols.append('Average')
    return pd.DataFrame(rows, columns=cols)

# Computes the precision and recall of a model given the predicted and labeled data
def evaluate(data):

    total_pos = len(data[data['Label'] == 1])
    total_pred_pos = len(data[data['Prediction'] == 1])

    predictions = data[data['Label'] == 1]
    true_pos = len(predictions[predictions['Prediction'] == 1])

    if total_pred_pos > 0:
        precision = true_pos / float(total_pred_pos)
    else:
        precision = float('nan')

    if total_pos > 0:
        recall = true_pos / float(total_pos)
    else:
        recall = float('nan')
    if precision + recall > 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = float('nan')

    return precision, recall, f1

# Split the given feature vectors into a training set and a test set
def split_train_test(data, test_size, feats, random_state=0):

    # Split the input data set into X and y
    features = ['String', 'Position', 'Article', 'Previous', 'Previous_2', 'Following']
    features.extend(feats)
    features.append('Label')

    X = data[features]
    y = data['Label']

    # Use the function from scikit learn
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


