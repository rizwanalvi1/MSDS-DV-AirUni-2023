import joblib

vectorizer = joblib.load('vec_airuni.pkl')
clf = joblib.load('mod_airuni.pkl')

# input_name = 'Rizwan Alvi'
input_name = 'Faisal'

if(clf.predict(vectorizer.transform([input_name])[0]) == 1):
    print('Male')
elif(clf.predict(vectorizer.transform([input_name])[0]) == 0):
    print('Female')

# if(clf.predict(vectorizer.transform(["Imran Alvi"])[0]) == 1):
#     print('Male')
# elif(clf.predict(vectorizer.transform(["Imran Alvi"])[0]) == 0):
#     print('Female')
