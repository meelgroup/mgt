import ast
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import os.path
import pandas as pd
import seaborn as sns
import operator as op
from functools import reduce

from setup import DIR   # DIR to get data to plot
from setup import DIR2  # DIR
FILE_GENERAL = "output_file-"
FILE_GENERAL_CMP = "output_file_comparison-"
EXTENSION = ".out"
d = 0.05
FILE_2 = "output_file"

# binomial cofficient, n choosr r


def ncr(n, r):
    # print(n)
    # print(r)
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

# calculate binary entropy of Bernoulli(p)


def bin_entropy(p):
    return (-p)*np.log2(p)-(1-p)*np.log2(1-p)


# function to parse output file that contains both MGT and LP accuracy and time results
def parser_comparison(u=0):

    for i in range(u + 1):

        if os.path.isfile(DIR + FILE_GENERAL_CMP + str(i) + EXTENSION):

            with open(DIR + FILE_GENERAL_CMP + str(i) + EXTENSION) as out:
                data = [ast.literal_eval(line) for line in out if line.strip()]

            n = data[0]
            k = data[1]
            lambdam = data[2]
            noiseless = data[3]
            T = data[4]
            E = data[5]
            P = data[6]
            T_CPU = data[7]
            lp_E = data[8]
            lp_P = data[9]
            lp_T_CPU = data[10]

            print_phase_transition(n, k, lambdam, T, noiseless, T_CPU, lp_T_CPU)

            print_accuracy(n, k, lambdam, T, noiseless, E, P, lp_E, lp_P)


def parser(u=0, verbose=False):

    for i in range(u + 1):

        if(verbose):
            print("showing the plot")

        if os.path.isfile(DIR + FILE_GENERAL + str(i) + EXTENSION):

            with open(DIR + FILE_GENERAL + str(i) + EXTENSION) as out:
                data = [ast.literal_eval(line) for line in out if line.strip()]

            n = data[0]
            k = data[1]
            lambdam = data[2]
            noiseless = data[3]
            T = data[4]
            E = data[5]
            P = data[6]

            E = [e/n for e in E]

            print_accuracy_maxsat(n, k, lambdam, T, noiseless, E, P)


def print_accuracy_maxsat(n, k, lambda_w, tests, noiseless, E, P):

    bound = []
    non_asym_bound = []
    bound_string = ''
    non_asym_string = ''
    title = "$n = $" + str(n) + ", $k = $" + str(k)

    if noiseless:
        name = "noiseless"
        bound_string = r'$klog_2(\frac{n}{k})$'
        non_asym_string = '(2^m) / (n choose k)'

    else:
        name = "noisy"
        bound_string = r'$log_2\binom{n}{k} / (1 - h(d))$'
        non_asym_string = 'm*(1 - h(d))) / (log2(n choose k))'
        title = title + ", $d = 0.05$"

    plt.plot(tests, P, "b", label="MGT", linewidth=2.5)
    plt.plot(tests, P, "bo")

    plt.title(title, fontsize=20)
    plt.xlabel("number of tests, $m$", fontsize=19)
    plt.ylabel("probability of success", fontsize=19)
    plt.legend(loc="best", fontsize=16.5)
    plt.tight_layout()
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.tick_params(axis='both', which='major', labelsize=15.5)
    ax.tick_params(axis='both', which='minor', labelsize=13.5)
    plt.savefig(DIR2 + str(name) + "_n" + str(n) + "k" + str(k) + ".png")
    plt.show()


def print_accuracy(n, k, lambda_w, tests, noiseless, E, P, lp_E, lp_P):
    bound = []
    non_asym_bound = []
    bound_string = ''
    non_asym_string = ''
    title = "$n = $" + str(n) + ", $k = $" + str(k)

    if noiseless:
        name = "noiseless"
        bound_string = r'$log_2\binom{n}{k}$'
        non_asym_string = r'(2^m) / (n \choose k)'

        for i in range(len(tests)):
            bound.append(np.log2(ncr(n, k)))

        if n < 1000:
            for m in tests:
                non_asym_bound.append((2**m) / (ncr(n, k)))

    else:
        name = "noisy"
        bound_string = r'$\frac{log_2\binom{n}{k}}{1 - h(d)}$'
        non_asym_string = r'$m*(1 - h(d))) / (log_2({n \choose k}))$'
        title = title + ", $d = 0.05$"

        if n < 1000:
            for i in range(len(tests)):
                bound.append(np.log2(ncr(n, k)) / (1 - bin_entropy(d)))

        if n < 1000:
            for m in tests:
                non_asym_bound.append((m*(1 - bin_entropy(d))) / (np.log2(ncr(n, k))))

    plt.plot(tests, P, "b", label="MGT", linewidth=2.5)
    plt.plot(tests, lp_P, "r--", label="LP", linewidth=2.5)
    plt.plot(tests, P, "bo")
    plt.plot(tests, lp_P, "rx")

    if noiseless or n < 1000:
        plt.plot(bound, P, "k", label=bound_string, linewidth=2.5)
    plt.title(title, fontsize=20)
    plt.xlabel("number of tests, $m$", fontsize=19)
    plt.ylabel("probability of success", fontsize=19)
    plt.legend(loc="best", fontsize=16.5)
    plt.tight_layout()
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.tick_params(axis='both', which='major', labelsize=15.5)
    ax.tick_params(axis='both', which='minor', labelsize=13.5)
    plt.savefig(DIR2 + str(name) + "_n" + str(n) + "k" + str(k) + ".png")
    plt.show()


def print_phase_transition(n, k, lambda_w, tests, noiseless, t_maxsat, t_lp):

    bound = []
    non_asym_bound = []
    bound_string = ''
    non_asym_string = ''
    title = "$n = $" + str(n) + ", $k = $" + str(k)

    if noiseless:
        name = "noiseless"
        bound_string = r'$log_2\binom{n}{k}$'
        non_asym_string = '(2^m) / {n \choose k}'

        for i in range(len(tests)):
            bound.append(np.log2(ncr(n, k)))

        if n < 1000:
            for m in tests:
                non_asym_bound.append((2**m) / (ncr(n, k)))

    else:
        name = "noisy"
        bound_string = r'$\frac{log_2\binom{n}{k}}{1 - h(d)}$'
        non_asym_string = r'$m*(1 - h(d))) / (log_2({n \choose k}))$'
        title = title + ", $d = 0.05$"

        if n < 1000:
            for i in range(len(tests)):
                bound.append(np.log2(ncr(n, k)) / (1 - bin_entropy(d)))

        if n < 1000:
            for m in tests:
                non_asym_bound.append((m*(1 - bin_entropy(d))) / (np.log2(ncr(n, k))))

    a = [0] + t_maxsat[1:]
    plt.plot(tests, t_lp, "r--", label="LP", linewidth=2.5)
    plt.plot(tests, t_maxsat, "b", label="MGT", linewidth=2.5)
    plt.plot(tests, t_lp, "rx")
    plt.plot(tests, t_maxsat, "bo")
    if noiseless or n <= 1000:
        plt.plot(bound, a, "k", label=bound_string, linewidth=2.5)
    plt.title(title, fontsize=20)
    plt.xlabel("number of tests, $m$", fontsize=19)
    plt.ylabel("time (s)", fontsize=17)
    plt.legend(loc="best", fontsize=16.5)
    plt.tight_layout()
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.tick_params(axis='both', which='major', labelsize=14.5)
    ax.tick_params(axis='both', which='minor', labelsize=12.5)
    plt.savefig(DIR2 + "time_" + str(name) + "_n" + str(n) + "k" + str(k) + ".png")
    plt.show()
