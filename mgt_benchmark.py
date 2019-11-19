#!/usr/bin/env python3
import max_sat_interface as mxs
import group_testing_function as gtf
import numpy as np

from setup import DIR
from setup import OUT_NAME
from setup import EXTENSION
from setup import number_of_trials

# Class of object to contain trials information
class Trial:
    def __init__(self, var):
        self.E = []  # mean error
        self.P = []  # probability of success (after number_of_trials)
        self.t_e = []  # temporary error
        self.t_h = []  # temporary hamming distance
        self.var = var


def main_varying_maxhs(n, p, noiseless, u):

    n_trials = number_of_trials

    k = round(n * p)

    x = gtf.generate_input_k(n, k)

    x_s = [1 if i in x else 0 for i in range(1, n + 1)]

    noise_probability = 0.05

    lambda_w = round((np.log((1 - noise_probability) / noise_probability)) / (np.log((1 - (k / n)) / (k / n))), 2)

    T = [1, int(n / (5 * np.log2(n)) + 1)]

    # generate T
    i = 1
    # until we reach the condition of success have more dense trials
    while T[i] < k * np.log2(n / k):
        if T[i] - T[i - 1] > round(n / 100):
            T.append(int(2 * T[i] - T[i - 1] - round(n / 100)))
        else:
            T.append(int(T[i] + round(n / 100)))
        i += 1

    # dense trials around k* log2(n/k)
    while T[i] < n:
        T.append(int(2 * T[i] - T[i - 1] + round(n / 100)))

        i += 1

    # T = [1, 10, 30]

    nw_trials = []

    noise_weight = [0.0]

    if not noiseless:
        noise_weight = [lambda_w]

    for i in noise_weight:
        nw_trials.append(Trial(i))

    t_maxhs = []

    # for every t number of tests
    for t in T:
        print(t)

        for tr in nw_trials:
            tr.t_e = []  # blank temporary
            tr.t_h = []  # blank temporary

        time_MAXHS = []

        for i in range(n_trials):
            a = gtf.generate_pool_matrix(n, k, t)

            for tr in nw_trials:
                y = gtf.get_results(t, a, x, noiseless, noise_probability)
                mxs.output(n, t, x, y, a, noiseless, tr.var)

                tests = (k*t*np.log10(n))/(n)

                r, noise, tm = mxs.call_Max_Sat(n)

                # add execution time
                time_MAXHS.append(tm)

                # calculating hamming distance between model result and input x

                vs = [[r[j], x_s[j]] for j in range(len(r))]
                hamming_distance = sum([1 if vs_i[0] != vs_i[1] else 0 for vs_i in vs])

                tr.t_h.append(hamming_distance)

                # there's an error?
                if hamming_distance > 0:
                    tr.t_e.append(1)
                else:
                    tr.t_e.append(0)

        for tr in nw_trials:
            tr.E.append(np.mean(tr.t_h))
            tr.P.append(1 - np.mean(tr.t_e))

        t_maxhs.append(np.mean(time_MAXHS))

    X = []

    for i in range(len(T)):
        X.append(k * np.log2(n / k))

    with open(DIR + OUT_NAME + "-" + str(u) + EXTENSION, "w+") as output_file:

        output_string = ''

        output_string += str(n) + "\n" + str(k) + "\n" + str(lambda_w) + "\n" + str(noiseless) + "\n"

        output_string += str(T) + "\n"

        for tr in nw_trials:
            output_string += str(tr.E) + "\n" + str(tr.P) + "\n"

        output_string += str(t_maxhs) + "\n"

        output_file.write(output_string)

