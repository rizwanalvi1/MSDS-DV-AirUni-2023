import pandas as pd
import joblib
# from sklearn.externals import joblib
from io import StringIO
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from sklearn.model_selection import cross_val_score
import seaborn as sns
from sklearn.metrics import confusion_matrix
# from IPython.display import display

from sklearn.feature_selection import chi2

from sklearn import metrics


df = pd.read_csv('fbr_3.csv')

# frames = [df1, df2, df3]
# result = pd.concat(frames)


# df = df.head(200000)
# df.info()

col = ['NTN', 'NAME']
df = df[col]

df = df[pd.notnull(df['NTN'])]
df = df[pd.notnull(df['NAME'])]

dff = pd.DataFrame(df, columns = ['NTN', 'NAME'])

dff = dff.loc[df['NTN'].str.len() == 13]
dff['GENDER'] = 2

male_vals = ['1','3','5','7','9']
female_vals = ['2','4','6','8','0']

for i, row in dff.iterrows():
    if(row[0][12] in male_vals):
        dff._set_value(i, 'GENDER', 1)
    elif (row[0][12] in female_vals):
        dff._set_value(i, 'GENDER', 0)

# dff.info()
X_train, X_test, y_train, y_test = train_test_split(dff['NAME'], dff['GENDER'],test_size=0.2, random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, y_train)
#
joblib.dump(count_vect,'vectorizer.pkl')
joblib.dump(clf, 'fbr_3.pkl')

print(clf.predict(count_vect.transform(["Rizwan Alvi"])))
print('Completed...')
