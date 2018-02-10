import numpy as np
import sys
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from sklearn import  metrics
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.tree import  DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier



input_fname = sys.argv[1]
output_fname = sys.argv[2]

#input_fname = 'input3.csv'
#output_fname = 'output3.csv'

#Classifier comparison function:
def clf_comp(input_fname, output_fname):

    # Get Data:
    X_D = np.genfromtxt(input_fname, delimiter=",")
    X_D = np.delete(X_D, 0, 0)

    # Cleaning Data
    Y_D = (X_D[:,2])

    X_D = np.delete(X_D, 2, 1)

    # Normalization:
    m = np.mean(X_D, axis=0)
    s = np.std(X_D, axis=0)

    x1 = (X_D[:,0] - m[0])/s[0]
    x2 = (X_D[:,1] - m[1])/s[1]

    X_D = np.column_stack((x1,x2));

    #Splitting Data
    X_train, X_test, Y_train, Y_test = train_test_split(X_D, Y_D, test_size=.4, random_state=42, stratify=Y_D)

    # Array for output
    fp = open(output_fname, 'w')

    #Linear
    parameters = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
    svr = svm.SVC(kernel="linear")
    clf = GridSearchCV(svr, parameters, cv=5)
    clf.fit(X_train, Y_train)
    best_score = clf.best_score_
    test_score = metrics.accuracy_score(Y_test, clf.predict(X_test))
    fp.write("svm_linear, "+str(best_score)+", "+str(test_score)+'\n')

    #Poly
    parameters = {'C' : [0.1, 1, 3], 'degree' : [4, 5, 6], 'gamma' : [0.1, 1]}
    svr = svm.SVC(kernel="poly")
    clf = GridSearchCV(svr, parameters, cv=5)
    clf.fit(X_train, Y_train)
    best_score = clf.best_score_
    test_score = metrics.accuracy_score(Y_test, clf.predict(X_test))
    fp.write("svm_polynomial, "+str(best_score)+", "+str(test_score)+'\n')

    #rbf
    parameters = {'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'gamma' : [0.1, 0.5, 1, 3, 6, 10]}
    svr = svm.SVC(kernel="rbf")
    clf = GridSearchCV(svr, parameters, cv=5)
    clf.fit(X_train, Y_train)
    best_score = clf.best_score_
    test_score = metrics.accuracy_score(Y_test, clf.predict(X_test))
    fp.write("svm_rbf, "+str(best_score)+", "+str(test_score)+'\n')

    #Logistic Regression

    parameters = { "C" : [0.1, 0.5, 1, 5, 10, 50, 100]}
    LR = LogisticRegression()
    clf = GridSearchCV(LR, parameters, cv=5)
    clf.fit(X_train, Y_train)
    best_score = clf.best_score_
    test_score = metrics.accuracy_score(Y_test, clf.predict(X_test))
    fp.write("logistic, "+str(best_score)+", "+str(test_score)+'\n')

    #K-Neighbours
    n_arr = []
    leaf_arr = []
    for i in range(1,60):
        if i <=50:
            n_arr.append(i)
        if i%5 == 0:
            leaf_arr.append(i)

    parameters = {'n_neighbors': n_arr, 'leaf_size' : leaf_arr}

    est = KNeighborsClassifier()
    clf = GridSearchCV(est, parameters, cv=5)
    clf.fit(X_train, Y_train)
    best_score = clf.best_score_
    test_score = metrics.accuracy_score(Y_test, clf.predict(X_test))
    fp.write("knn, "+str(best_score)+", "+str(test_score)+'\n')

    #Decision Trees
    depth_arr = []
    split_arr = []
    for i in range(1,60):
        if i <=50:
            depth_arr.append(i)
        if i > 1 and i <=10:
            split_arr.append(i)

    parameters = {'max_depth': depth_arr, 'min_samples_split' : split_arr}

    est = DecisionTreeClassifier()
    clf = GridSearchCV(est, parameters, cv=5)
    clf.fit(X_train, Y_train)
    best_score = clf.best_score_
    test_score = metrics.accuracy_score(Y_test, clf.predict(X_test))
    fp.write("decision_tree, "+str(best_score)+", "+str(test_score)+'\n')

    #Random Forest Classifier
    est = RandomForestClassifier()
    clf = GridSearchCV(est, parameters, cv=5)
    clf.fit(X_train, Y_train)
    best_score = clf.best_score_
    test_score = metrics.accuracy_score(Y_test, clf.predict(X_test))
    fp.write("random_forest, "+str(best_score)+", "+str(test_score)+'\n')

    fp.close()

clf_comp(input_fname, output_fname)



