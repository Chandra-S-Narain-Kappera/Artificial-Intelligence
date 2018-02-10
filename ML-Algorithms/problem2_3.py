import numpy as np
import pandas as pd
import math
import sys
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import  linear_model

input_fname = sys.argv[1]
output_fname = sys.argv[2]

#input_fname = 'input2.csv'
#output_fname = 'output2.csv'


def plot_figs(X, Y, B):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    Z = np.matmul(X, B.reshape(3,1))
    np.delete(X, 0, 1)

    ax.plot_surface(X[:,0], X[:,1], Z, color='b')

    ax.scatter(X[:, 0], X[:, 1], Y, c='r', marker='o')


    ax.set_xlabel('Age (years)')
    ax.set_ylabel('Weight (Kilograms)')
    ax.set_zlabel('Height (Metres)')
    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])

    plt.savefig("linear_regression.png")

def plot_learn(plot_vals, alpha):
    temp = plot_vals[7]
    plot_vals[7] = plot_vals[6]
    plot_vals[6] = temp
    plt.clf()
    plt.plot(alpha, plot_vals)
    plt.xlabel('alpha')
    plt.ylabel('value')
    plt.savefig("convergence_rate.png")

def linear_regression(input_fname, output_fname):
    X_D = np.genfromtxt(input_fname, delimiter=",")

    # Data Scaling:
    m = np.mean(X_D, axis=0)
    s = np.std(X_D, axis=0)

    x1 = (X_D[:,0] - m[0])/s[0]
    x2 = (X_D[:,1] - m[1])/s[1]
    Y_D = (X_D[:,2])

    # Adding one:
    X_D = np.column_stack((x1,x2));
    X_D = np.insert(X_D, 0, values=1, axis=1)


    # Defining Beta:
    B = np.zeros(3)

    # Calculate
    arr = []
    t = [B[0], B[1], B[2]]
    num_iter = 100
    
    # Iterate
    plot_val = []
    for alpha in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.9]:
        B = np.zeros(3)
        conv_rate = 0
        t_prev = 99999999999
        if alpha == 0.9:
            num_iter = 25
        else:
            num_iter = 100
        for k in range(0,num_iter):

            # B matrix
            R = np.zeros(3)
            for i in range(0, len(X_D)):
                prod = (np.inner(B,X_D[i]) - Y_D[i])
                R  = R +  prod*X_D[i]

            B = B - (alpha/len(X_D))*R

            # Convergence Rate
            t = np.linalg.norm(np.inner(B,X_D) - Y_D)

            if math.fabs(t_prev - t) > 0.00001:
                conv_rate = conv_rate + 1
            t_prev = t

        # Convergence Rate Plot
        if alpha < 5:
            plot_val.append(conv_rate)

        """ optional plotting
        if alpha == 0.9:
            plot_figs(X_D, Y_D, B)
        """

        t = [alpha, num_iter, B[0], B[1], B[2]]

        arr.append(t)

    # Convergence Plot:
    alpha_arr = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 0.9, 1]
    #plot_learn(plot_val, alpha_arr)
    arr = np.array(arr)
    np.savetxt(output_fname, arr, delimiter=',', fmt='%.3f, %d, %.3e, %.3e, %.3e')


linear_regression(input_fname, output_fname)

"""
About my choice of learning rate:
I have plotted convergence rate plot - number of iterations required to converge vs alpha.
From the plot it can be seen that for alpha = 0.9 it is the minimum and hence I have chosen this to be my learning rate.

Observation about learning rate:
Very small alphas took more number of iterations to converge, where as very large alphas failed to converge.
The optimal solution lied somewhere between the extremes and was determined to be around 0.9 from the convergence rate plot.
"""





