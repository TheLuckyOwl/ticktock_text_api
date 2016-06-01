import sklearn
import pickle
import numpy as np
from sklearn import cross_validation
from sklearn import datasets
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn import preprocessing
import random
import pprint

features = pickle.load(open('features.pkl'))
labels = pickle.load(open('labels.pkl'))
file_list = pickle.load(open('file_list.pkl'))
def convert(x):
    if x == 1 or x == 2:
        return 0
    else:
        return 1

labels = map(convert, labels)
#t_s = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
t_s = [0.2]
for thresh in t_s:
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size=thresh,random_state=0)

    #normalization
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train_org = X_train
    X_test = scaler.transform(X_test)
    X_train = scaler.transform(X_train)

    # a list of parameters to tune for the rbf kernal svm. need to beat the baseline of acc= 0.712
    #C_list = [0.1,1,10,100,200,300,400,500,600,700,1000]
    C_list = [1]
    #gamma_list = [0.01,0.001,0.0001,0.0004,0.00045,0.0005,0.00055,0.0006,0.001,0.01,0.1]
    gamma_list =[1]
    nu_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    #nu_list = [0.1]
    coef_list = [0, 0.001, 0.01, 0.1, 1.0, 2.0, 3.0, 10.0]
    #coef_list = [1.0]
    #degree_list = [1, 2, 3, 4, 5, 6, 7, 8]
    degree_list = [1]

    score_matrix =[]
    score_list_all = []
    clf_list = []
    for c in C_list:
        score_list = []
        for g in gamma_list:
            for coef in coef_list:
                for ho in nu_list:
                    for dg in degree_list:
                        clf = svm.NuSVC(nu = ho, degree = dg, coef0 = coef, gamma=g, kernel='sigmoid').fit(X_train,y_train)
                        #clf = svm.NuSVC(nu = ho, kernel='poly').fit(X_train,y_train)
                        clf_list.append(clf)
                        score = clf.score(X_test,y_test)
                        #print 'C: ' + str(c) + ', gamma:' +str(g) + ', mean accuracy:'+ str(score)
                        score_list.append(score)
                        score_list_all.append(score)
                """
                if score_matrix == []:
                    score_matrix = score_list
                else:
                    score_matrix = np.vstack((score_matrix,score_list))
                """
    max_score = max(score_list_all)
    #print max_score
    index = score_list_all.index(max_score)
    max_percent = 0
    best_guess = None
    for thing in clf_list:
        #clf_max = clf_list[index]
        clf_max = thing
        predicted_y = clf_max.predict(features)
        y_diff = predicted_y - labels
        wrong = y_diff !=0
        index = np.where(np.array(wrong)!=0)[0]
        #for idx in index:
            #file_wrong = file_list[idx]
            #print features[idx]
            #print file_wrong
        #print len(index)

        cur = float(len(index)) / float(len(wrong))

        if max_percent == 0:
            max_percent = cur
            best_guess = predicted_y
        elif max_percent < cur:
            max_percent = cur
            best_guess = predicted_y

        pickle.dump((X_train_org, scaler, clf_max), open('depth_rater.pkl', 'wb'))

    baseline = reduce(lambda x, y : x + y, labels) / float(len(labels))
    baseline = max(baseline, 1.0 - baseline)
    print max_percent
    print baseline
    print best_guess
    print labels
