#!/usr/bin/env python3
import max_sat_interface as mxs
import group_testing_function as gtf
import numpy as np
import scipy.spatial.distance as sd
import general_lp_interface as lp

from setup import DIR
from setup import OUT_NAME
from setup import EXTENSION
from setup import CMP
from setup import number_of_trials

# Class of object to contain trials information
class Trial:
    def __init__(self, var):
        self.E = []  # mean error
        self.P = []  # probability of success (after number_of_trials)
        self.t_e = []  # temporary error
        self.t_h = []  # temporary hamming distance
        self.lp_E = []  # on number of tests
        self.lp_P = []
        self.lp_E_C = []  # on number of tests
        self.lp_P_C = []  # probability of success (after number_of_trials)
        self.lp_t_e = []  # temporary error
        self.lp_t_h = []  # temporary hamming distance
        self.lp_t_e_c = []  # temporary error
        self.lp_t_h_c = []  # temporary hamming distance
        self.var = var

def main_comparison_maxhs_lp(n=100, p=0.03, noiseless=True,noise_probability = 0.05, u=0, verbose=False):

    if(verbose):
        print("Comparative performance of MaxSAT and LP-relaxed encoding while solving the decoding phase of group testing")
        print("- number of items: ", n)
        print("- probability of defectivity: ", p)
        print("- noiseless testing:", noiseless)
        if(not noiseless):
           print("- probability of noise: ", noise_probability)
        print("- index of experiment:", u)



    k = round(n * p)

    x = gtf.generate_input_k(n, k)

    x_s = [1 if i in x else 0 for i in range(1, n + 1)]

    
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

    lambda_w = round((np.log((1-noise_probability)/noise_probability)) / (np.log((1-(k/n))/(k/n))), 2)

    if not noiseless:
        noise_weight = [lambda_w]

    for i in noise_weight:
        nw_trials.append(Trial(i))

    mean_time_lp = []
    mean_time_maxhs = []

    success_lp = []
    success_maxhs = []

    tr = nw_trials[0]

    # for every t number of tests
    if(verbose):
        print("\nperforming tests\n")
    for t in T:
        if(verbose):
            print("- number of tests: ", t)

        time_lp = []
        time_maxhs = []

        tr.t_h = []
        tr.lp_t_h = []
        tr.lp_t_e = []
        tr.t_e = []

        for i in range(number_of_trials):

            a = gtf.generate_pool_matrix(n, k, t)

            y = gtf.get_results(t, a, x, noiseless, noise_probability)

            # *************MAX_HS*************

            mxs.output(n, t, x, y, a, noiseless, tr.var)

            r, noise, tm = mxs.call_Max_Sat(n)

            # add execution time
            time_maxhs.append(tm)
            # calculating hamming distance between model result and input x
            hamming_distance = sd.hamming(x_s, r)
            tr.t_h.append(hamming_distance)

            # there's an error?
            if hamming_distance > 0:
                tr.t_e.append(1)
            else:
                tr.t_e.append(0)

            # *************LP_RELAX*************
            r_lp_i, tm = lp.solve(y, a, n, noiseless)

            # add execution time
            time_lp.append(tm)

            # ****CAST****

            r_lp = [int(i) for i in r_lp_i[:n]]

            # calculating hamming distance between model result and input x
            hamming_distance = sd.hamming(x_s, r_lp)
            tr.lp_t_h.append(hamming_distance)

            # there's an error?
            if hamming_distance > 0:
                tr.lp_t_e.append(1)
            else:
                tr.lp_t_e.append(0)

        mean_time_lp.append(np.mean(time_lp))
        mean_time_maxhs.append(np.mean(time_maxhs))
        for tr in nw_trials:
            tr.E.append(np.mean(tr.t_h))
            tr.P.append(1 - np.mean(tr.t_e))
            tr.lp_E.append(np.mean(tr.lp_t_h))
            tr.lp_P.append(1 - np.mean(tr.lp_t_e))

    X = []

    for i in range(len(T)):
        X.append(k * np.log2(n / k))

    with open(DIR + OUT_NAME + CMP + "-" + str(u) + EXTENSION, "w+") as output_file:

        output_string = ''

        output_string += str(n) + "\n" + str(k) + "\n" + str(lambda_w) + "\n" + str(noiseless) + "\n"

        output_string += str(T) + "\n"

        for tr in nw_trials:
            output_string += str(tr.E) + "\n" + str(tr.P) + "\n"

        output_string += str(mean_time_maxhs) + "\n"

        for tr in nw_trials:
            output_string += str(tr.lp_E) + "\n" + str(tr.lp_P) + "\n"

        output_string += str(mean_time_lp) + "\n"

        output_file.write(output_string)

