import numpy as np
import numpy.random as nrndm
import random as rndm


# this file contains the functions needed to generate an instance of a
# group testing decoding problem


# generate_input function generate the vector x, called input vector,
# which is at the same time the input to the Group Testing problem
# and the solution to be recovered
# n is the number of variables that need to be generate
# p_i is the probability that an item is faulty
def generate_input(n, p_i):
    # generate a sparse input to recover
    x = rndm.sample(range(1, n + 1), nrndm.binomial(n, p_i))

    # counting number of faulty items
    k = len(x)

    return x, k


# generate_input_k function generate the vector x, called input vector,
# which is at the same time the input to the Group Testing problem
# and the solution to be recovered
# n is the number of variables that need to be generate
# k is the fixed number of faulty item
def generate_input_k(n, k, verbose=False):

    if(verbose):
        print("\ngenerating a random item vector with ", n ,"items and ", k ," defective items")
    # generate a sparse input to recover
    x = rndm.sample(range(1, n + 1), k)

    return x


# generate_pool_matrix generate the recovery matrix, following a binomial model
# where each item has a probability to belong to a group
# the probability here is considered with respect to k number of faulty,
# this parameter should be known
# n is the number of elements of the input vector
# k is the number of faulty
# t is the number of groups (number of tests to be performed)
def generate_pool_matrix(n, k, t):
    a = []
    for i in range(t):
        a.append(rndm.sample(range(1, n + 1), nrndm.binomial(n, (np.log(2) / k))))
    # print("matrix generated, getting result")
    return a


# get_results considering the input x, the pool matrix a return
# the results for the every group tested (a vector y)
# n is the number of elements of the input vector
# a is the recovery matrix
# t is the number of groups (number of tests to be performed)
# noiseless is a boolean, True if the problem is noiseless, False otherwise
# noise_probability is the probability that a test result is turned, considered if NOT noiseless
def get_results(t, a, x, noiseless, noise_probability):
    # vector of the tests
    y = [0] * t
    # get result of test
    if noiseless:
        for i in range(t):
            if any(x_i in a[i] for x_i in x):
                y[i] = 1
    else:
        for i in range(t):
            if any(x_i in a[i] for x_i in x):
                y[i] = 1
            y[i] = abs(y[i] - nrndm.choice(range(0, 2), p=[1 - noise_probability, noise_probability]))

    return y

