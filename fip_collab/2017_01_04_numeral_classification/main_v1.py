import numpy as np
import h5py
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


def cross_validate(mc, X_cal, y_cal, X_cv, y_cv):
    mc.get_Cvec()

    acc_cv = np.zeros(mc.n_C)

    """find best regularization constant with CV data"""
    for ii in xrange(mc.n_C):

        C = mc.Cvec[ii]

        mc.get_model(C)
        mc.model.fit(X_cal, y_cal)

        """measure prediction accuracy"""
        y_cv_pred = mc.model.predict(X_cv)

        acc = np.mean(y_cv_pred == y_cv)
        acc_ = np.round(100*acc, 3)
        acc_cv[ii] = acc_

        print "prediction accuracy, cross-validation" +\
              " data (C=%s): %s%%" % (C, acc_)

    return acc_cv


def get_sets(X, y, cv_frac, test_frac):

    ns = y.size

    """scramble data"""
    seed = 0
    np.random.seed(seed=seed)

    tmp = np.arange(ns)
    np.random.shuffle(tmp)

    X = X[tmp, :]
    y = y[tmp]

    """split data into calibration, cross-validation and test sets"""
    l1 = np.int64((1-cv_frac-test_frac)*ns)
    l2 = np.int64((1-test_frac)*ns)

    X_cal = X[:l1, :]
    y_cal = y[:l1]
    X_cv = X[l1:l2, :]
    y_cv = y[l1:l2]
    X_test = X[l2:, :]
    y_test = y[l2:]

    return X_cal, y_cal, X_cv, y_cv, X_test, y_test


def loaddata(fname):

    f = h5py.File('digits.hdf5', 'r')
    X = f.get('X')[...]
    y = f.get('y')[...]
    f.close()

    return X, y


def plot_acc(y, y_pred):

    plt.figure(figsize=[5, 3])

    ndig = 10
    acc_vec = np.zeros((ndig,))

    for ii in xrange(ndig):
        tmp = y == ii
        acc = np.mean(y_pred[tmp] == y[tmp])
        acc = np.round(100*acc, 3)
        acc_vec[ii] = acc

    lab = np.arange(ndig)
    plt.bar(lab, acc_vec, align='center', alpha=0.4)
    plt.xticks(lab, lab)

    plt.axis([-.75, 9.75, 80, 101])

    plt.xlabel('digit')
    plt.ylabel('prediction accuracy (%)')

    plt.tight_layout()


def plot_prediction(X, y_pred):
    """randomly select n_sp images, then plot them and
    the associated predicted digits from the classification"""

    n_sp = 15
    vec = np.random.randint(y_pred.size, size=(n_sp,))

    dim = np.int16(np.sqrt(X.shape[1]))

    plt.subplots(figsize=[10, 6])

    for ii in xrange(len(vec)):

        ax = plt.subplot(3, 5, ii+1)

        X_ = X[vec[ii], :].reshape((dim, dim))

        ax.imshow(X_.T, origin='upper',
                  interpolation='none', cmap='gray')

        plt.title('predicted: %s' % y_pred[vec[ii]],
                  fontsize=13)

        ax.axis('off')


def test_acc(mc, acc_cv, X_test, y_test):
    inx = np.argmax(acc_cv)
    C = mc.Cvec[inx]

    mc.get_model(C)
    mc.model.fit(X_cal, y_cal)
    y_test_pred = mc.model.predict(X_test)

    acc = np.mean(y_test_pred == y_test)
    acc = np.round(100*acc, 3)

    print "prediction accuracy, test data (C=%s): %s%%" % (C, acc)

    # print "first 10 true digits followed by predicted digits:"
    # print y_test[:10]
    # print y_test_pred[:10]

    return y_test_pred


class allmodels:

    def __init__(self, modeltype):
        self.modeltype = modeltype

    def get_Cvec(self):
        """assigns the vector of coefficients with which to do
        cross-validation"""

        if self.modeltype == 'GB':
            Cvec = np.arange(10, 200, 20)
        elif self.modeltype == 'LOG':
            Cvec = np.arange(-3, 4)
            Cvec = 10. ** Cvec
        elif self.modeltype == 'NN':
            """C_vec contains regularization parameters"""
            Cvec = np.arange(-7, 1)
            Cvec = 10. ** Cvec
        elif self.modeltype == 'RF':
            Cvec = np.arange(10, 200, 20)
        elif self.modeltype == 'SVM':
            Cvec = np.arange(0, 7)
            Cvec = 10. ** Cvec

        self.Cvec = Cvec
        self.n_C = len(Cvec)

    def get_model(self, C):
        """assigns the model selected by the user and assigns the
        parameter which changes for cross-validation and any
        other parameters"""

        if self.modeltype == 'GB':
            model = GradientBoostingClassifier(n_estimators=C)
        elif self.modeltype == 'LOG':
            model = LogisticRegression(C=C)
        elif self.modeltype == 'NN':
            model = MLPClassifier(hidden_layer_sizes=(125,),
                                  activation='relu', alpha=C,
                                  max_iter=200, solver='lbfgs')
        elif self.modeltype == 'RF':
            model = RandomForestClassifier(n_estimators=C)
        elif self.modeltype == 'SVM':
            model = SVC(C=C, decision_function_shape='ovr',
                        kernel='poly')

        self.model = model


"""load digit images and labels"""
X, y = loaddata('digits.hdf5')

"""assign data to calibration, cross-validation and test sets"""
cv_frac = 0.1
test_frac = 0.1
X_cal, y_cal, X_cv, y_cv, X_test, y_test = get_sets(X, y, cv_frac, test_frac)

"""initialize allmodels class for selected sklearn method"""
mc = allmodels('SVM')
mc.get_Cvec()

"""perform cross validation to select the best parameter"""
acc_cv = cross_validate(mc, X_cal, y_cal, X_cv, y_cv)

"""evaluate prediction accuracy with test data for best parameter selection"""
y_test_pred = test_acc(mc, acc_cv, X_test, y_test)

"""plot the prediction accuracy versus digit"""
plot_acc(y_test, y_test_pred)

"""visualize success of prediction for a couple cases"""
plot_prediction(X_test, y_test_pred)

plt.show()
