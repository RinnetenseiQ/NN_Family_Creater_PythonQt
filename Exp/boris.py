import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC, LinearSVC
from mpl_toolkits.mplot3d import Axes3D


def plot_svc(svc, X, y, h=0.02, pad=0.25):
    x_min, x_max = X[:, 0].min() - pad, X[:, 0].max() + pad
    y_min, y_max = X[:, 1].min() - pad, X[:, 1].max() + pad
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = svc.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.2)
    # plt.contourf(xx, yy, Z)

    plt.scatter(X[:, 0], X[:, 1], s=70, c=y, cmap=plt.cm.Paired)
    # plt.scatter(X[:,0], X[:,1], s=70, c=y)
    # Support vectors indicated in plot by vertical lines
    sv = svc.support_vectors_
    plt.scatter(sv[:, 0], sv[:, 1], c='k', marker='|', s=100, linewidths='1')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()
    print('Number of support vectors: ', svc.support_.size)

def plot_svc2(svc, X, y, h=0.02, pad=0.25):
    x_min, x_max = X[:, 0].min() - pad, X[:, 0].max() + pad
    y_min, y_max = X[:, 1].min() - pad, X[:, 1].max() + pad
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = svc.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plt.scatter(xx, yy, Z, cmap=plt.cm.Paired)
    plt.scatter(xx, yy, Z)
    # plt.contourf(xx, yy, Z)

    plt.scatter(X[:, 0], X[:, 1], s=70, c=y, cmap=plt.cm.Paired)
    # plt.scatter(X[:,0], X[:,1], s=70, c=y)
    # Support vectors indicated in plot by vertical lines
    sv = svc.support_vectors_
    plt.scatter(sv[:, 0], sv[:, 1], c='k', marker='|', s=100, linewidths='1')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()
    print('Number of support vectors: ', svc.support_.size)

def get_data_for_3D(svc, X, y, h=0.02, pad=0.25):
    x_min, x_max = X[:, 0].min() - pad, X[:, 0].max() + pad
    y_min, y_max = X[:, 1].min() - pad, X[:, 1].max() + pad
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = svc.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    return xx, yy, Z


if __name__ == "__main__":
    # Generating random data: 20 observations of 2 features and divide into two classes.
    np.random.seed(5)

    # Return a sample (or samples) from the “standard normal” distribution.
    X = np.random.randn(20, 2)
    # Repeat elements of an array.
    y = np.repeat([1, -1], 10)
    X[y == -1] = X[y == -1] + 1
    # plt.scatter(X[:, 0], X[:, 1], s=70, c=y, cmap=plt.cm.Paired)
    # plt.xlabel('X1')
    # plt.ylabel('X2')
    svc = SVC(C=1.0, kernel='linear')
    # S: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
    svc.fit(X, y)

    plot_svc2(svc, X, y)

    # fig = plt.figure()
    # ax = Axes3D(fig)
    # xx, yy, Z = get_data_for_3D(svc, X, y)
    # plt.scatter(xx, yy, Z)
    # plt.show()
