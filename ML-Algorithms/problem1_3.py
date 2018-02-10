import numpy as np
import pandas as pd
import math
import sys
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

input_fname = sys.argv[1]
output_fname = sys.argv[2]

#input_fname = 'input1.csv'
#output_fname = 'output1.csv'

def visData2(df, W):

    for l, c, m in zip({-1, 1}, ('blue', 'red'), ('^', 's')):
        plt.scatter(df[df["label"] == l][1], df[df["label"] == l][2],
                    color=c,
                    label='class %s' % l,
                    alpha=0.5,
                    marker='o'
                    )
    # get the separating hyperplane
    a = -W[1] / W[2]
    xx = np.linspace(0, 16)
    yy = a * xx - (W[0]) / W[2]
    plt.plot(xx, yy, 'k-')

    plt.tight_layout()

    plt.savefig("perceptron_final.png")


def PLA(i_fname, o_fname):
    # Read input data
    X_D = np.genfromtxt (i_fname, delimiter=",")
    Y_D = X_D[:,2]
    X_D = X_D[:,[0,1]]
    X_D = np.insert(X_D, 0, values=1, axis=1)

    # Perceptron Algorithm:

    #Initiliaze weights:
    Wn = np.zeros(3)
    Wo = np.ones(3)
    tol = 0.005
    error = 1

    #Loop

    arr = []

    while (True):
        for i in range(0, len(X_D)):
            if Y_D[i]*np.inner(Wn,X_D[i]) <= 0:
                Wn = Wn + Y_D[i]*X_D[i]

        t = [Wn[1], Wn[2], Wn[0]]
        arr.append(t)

        if np.array_equal(Wn, Wo):
            break
        else:
            Wo = np.copy(Wn)


    arr = np.array(arr)
    np.savetxt(o_fname, arr, delimiter=',', fmt='%.3f')

    np.delete(X_D, 0, 1)
    df = pd.DataFrame(X_D)

    df["label"] = Y_D
    #visData2(df, Wn)


PLA(input_fname, output_fname)







