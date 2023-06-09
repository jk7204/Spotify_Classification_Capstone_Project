# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qtHxMTJs5w7UtLTWNGnMQCE9tKSxVs7G
"""

import random
random.seed(19116930)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
import torch
from torch import nn, optim
from sklearn.preprocessing import LabelEncoder
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics, tree
from sklearn.ensemble import AdaBoostClassifier
from sklearn.multiclass import OneVsRestClassifier
import warnings
from mpl_toolkits.mplot3d import Axes3D
import IPython
from sklearn.preprocessing import StandardScaler
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22']

"""## Data Preprocessing"""

data = pd.read_csv('musicData.csv')
print(data.shape)

data.head()

data[data.isna().any(axis=1)]
data = data.dropna()

plt.figure()
data["music_genre"].value_counts().sort_index().plot.bar()
plt.title("Distribution of Genre")

plt.hist(data["duration_ms"], bins=20)
plt.show()
# not normally distributed

print(data["duration_ms"].median())
data.loc[data["duration_ms"] == -1.0, "duration_ms"] = data["duration_ms"].median()

plt.hist(data["tempo"], bins=20)
plt.show()
# not normally distributed

temp = [data[data["tempo"] != "?"]["tempo"]]
tempo_med = np.median(np.array(temp, dtype=float))
print(tempo_med)

data.loc[data["tempo"] == "?", "tempo"] = str(tempo_med)
data["tempo"] = data['tempo'].astype(float)

le = LabelEncoder()

data["key_encoded"] = le.fit_transform(data["key"])
data["mode_encoded"] = le.fit_transform(data["mode"])
data["genre_encoded"] = le.fit_transform(data["music_genre"])
data.drop(["key", "music_genre", "mode"], axis=1, inplace=True)
data.head()

data.drop(["artist_name", "track_name", "obtained_date"], axis=1, inplace=True)
data.info()

genres = data['genre_encoded'].unique()
test_data = pd.DataFrame()
train_data = pd.DataFrame()

for genre in range(len(genres)):
    # Select songs for this genre
    genre_data = data[data['genre_encoded'] == genre]
    
    # Split the genre data into train and test sets
    train, test = train_test_split(genre_data, train_size=4500, test_size=500, random_state=50)
    
    # Add the train and test sets to the overall data splits
    test_data = pd.concat([test_data, test])
    train_data = pd.concat([train_data, train])

print("Test Data Shape: ", test_data.shape)
print("Train Data Shape: ", train_data.shape)

X_train = train_data.drop("genre_encoded", axis=1)
y_train = train_data["genre_encoded"]
X_test = test_data.drop("genre_encoded", axis=1)
y_test = test_data["genre_encoded"]

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

"""## Dimensionality Reduction & Clustering"""

numerical_col = X_train.columns[1:12]
sc = StandardScaler()
X_train[numerical_col] = sc.fit_transform(X_train[numerical_col])
X_test[numerical_col] = sc.fit_transform(X_test[numerical_col])

lda = LinearDiscriminantAnalysis(n_components=3)
lda.fit(X_train, y_train)
X_lda_train = lda.transform(X_train)
X_lda_test = lda.transform(X_test)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

target_ids = [i for i in range(10)]
feature_names = ['Electronic', 'Anime','Jazz','Alternative','Country','Rap',
                 'Blues','Rock','Classical','Hip-Hop']

for i, color, label in zip(target_ids, colors, feature_names):
    ax.scatter(X_lda_train[y_train == i, 0], X_lda_train[y_train == i, 1], X_lda_train[y_train == i, 2], c=color, label=label)
    
ax.set_xlabel('LDA Component 1')
ax.set_ylabel('LDA Component 2')
ax.set_zlabel('LDA Component 3')
ax.legend(loc='best')
plt.show()

coefficients = lda.coef_

fig, ax = plt.subplots(figsize=(20, 10))
im = ax.imshow(coefficients, cmap='coolwarm')
ax.set_xticks(range(X_train.shape[1]))
ax.set_xticklabels(X_train.columns.values)
ax.set_yticks(range(len(feature_names)))
ax.set_yticklabels(feature_names)
ax.set_xlabel('Features')
ax.set_ylabel('Classes')
ax.set_title('Coefficients of Linear Discriminants')
fig.colorbar(im, ax=ax)
plt.show()

"""## Classification Model

### AdaBoost (X_train)
"""

bdt = OneVsRestClassifier(AdaBoostClassifier(tree.DecisionTreeClassifier(max_depth=10)))
bdt.fit(X_train, y_train)

y_pred_bdt = bdt.predict_proba(X_test)
auc_bdt = metrics.roc_auc_score(y_test, y_pred_bdt, multi_class="ovo", average="weighted")
print("AUC score: ", auc_bdt)

warnings.filterwarnings("ignore")
fig, ax = plt.subplots(figsize=(8, 6))
for i in range(10):
    metrics.plot_roc_curve(bdt.estimators_[i], X_test, (y_test == i), ax=ax, name=f'Class {i}')

ax.set_title('ROC curve')
ax.set_ylabel("TPR")
ax.set_xlabel("FPR")
ax.legend(loc='lower right')
plt.show()

"""### AdaBoost (X_lda_train)"""

bdt = OneVsRestClassifier(AdaBoostClassifier(tree.DecisionTreeClassifier(max_depth=10)))
bdt.fit(X_lda_train, y_train)

y_pred_bdt = bdt.predict_proba(X_lda_test)
auc_bdt = metrics.roc_auc_score(y_test, y_pred_bdt, multi_class="ovo", average="weighted")
print("AUC score: ", auc_bdt)

fig, ax = plt.subplots(figsize=(8, 6))
for i in range(10):
    metrics.plot_roc_curve(bdt.estimators_[i], X_lda_test, (y_test == i), ax=ax, name=f'Class {i}')

ax.set_title('ROC curve')
ax.set_ylabel("TPR")
ax.set_xlabel("FPR")
ax.legend(loc='lower right')
plt.show()

"""### Random Forest (X_train)"""

rf = OneVsRestClassifier(RandomForestClassifier(max_depth=10, criterion='entropy', n_jobs=5))
rf.fit(X_train, y_train)

y_pred_rf = rf.predict_proba(X_test)
auc_rf = metrics.roc_auc_score(y_test, y_pred_rf, multi_class='ovo', average="weighted")
print("AUC score: ", auc_rf)

fig, ax = plt.subplots(figsize=(8, 6))
for i in range(10):
    metrics.plot_roc_curve(rf.estimators_[i], X_test, (y_test == i), ax=ax, name=f'Class {i}')

ax.set_title('ROC curve')
ax.set_ylabel("TPR")
ax.set_xlabel("FPR")
ax.legend(loc='lower right')
plt.show()

"""### Random Forest (X_lda_train)"""

rf = OneVsRestClassifier(RandomForestClassifier(max_depth=10, criterion='entropy', n_jobs=5))
rf.fit(X_lda_train, y_train)

y_pred_rf = rf.predict_proba(X_lda_test)
auc_rf = metrics.roc_auc_score(y_test, y_pred_rf, multi_class='ovo', average="weighted")
print("AUC score: ", auc_rf)

fig, ax = plt.subplots(figsize=(8, 6))
for i in range(10):
    metrics.plot_roc_curve(rf.estimators_[i], X_lda_test, (y_test == i), ax=ax, name=f'Class {i}')

ax.set_title('ROC curve')
ax.set_ylabel("TPR")
ax.set_xlabel("FPR")
ax.legend(loc='lower right')
plt.show()