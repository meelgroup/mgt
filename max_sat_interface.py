import subprocess as sbp

SOLVER = "maxhs"
BSTSOL = "-printBstSoln"
CPULIM = "-cpu-lim=100"
fixed_header = "c\nc comments Weighted Max-SAT\nc\np wcnf "
hard_weight = 1000000000
soft_weight = 1
input_for_max_HS = "temp/max_sat_input"
output_data_set = "data set"
SEP1 = "nv"
SEP12 = "Best Model Found:"
SEP2 = "nc"
CPUTIME = "CPU: "
TEMP = r"../max-sat-tester/temp"


# call_Max_Sat call the MaxSAT solver, in this case maxhs
# with the input file previously generate and the option of
# then it parse the solution and return the model found and the time needed to found it
def call_Max_Sat(n):

    # get the output
    # BSTSOL requires to output the best solution found in case the solving is stopped before finding the actual optimum
    # CPULIM limit the time in finding the optimum solution
    output_string = str(sbp.run([SOLVER, BSTSOL, CPULIM, input_for_max_HS], stdout=sbp.PIPE).stdout)

    time_string = output_string.split(CPUTIME)[1]
    time = float(time_string.split("\\")[0])

    # get the interesting output
    if(output_string.__contains__("Best Model Found:")):
        output_string = (output_string.split(SEP12))[1]
        output_string = (output_string.split(SEP2)[1]).split(SEP2)[0]
        output_string = (output_string.split(" \\")[0])
        model_string = (output_string[0:len(output_string) - 1]).split(" ")[1:]
    else:
        output_string = (output_string.split(SEP1)[1]).split(SEP2)[0]
        model_string = (output_string[0:len(output_string) - 1]).split(" ")[1:]

    # parse the model into integer
    model = list(map(int, model_string))
    noise = model[n:]
    model = model[:n]
    model = list(map(lambda x : 1 if x>0 else 0,model))

    return model, noise, time


# function to generate file to be read by Max_HS and file of data_set
# output generate the MaxSAT instance in the compact encoding without XOR
# n is the number of variables
# t is the number of group that has been tested
# y is the output result of the group testing instance
# a is the recovery matrix
# noiseless is a boolean, True if the problem is noiseless, False otherwise
# noise_weight is the weight associated to the noise constraint, it expresses the lambda
# lambda is the trade-off between noisy and faulty, we express only the noise weight as
# the weight associated to the faultiness is fixed to 1
# for optimization purpose the function directly generate the string to be included in the input file
def output(n, t, x, y, a, noiseless, noise_weight):
    if noiseless:
        m = n
    else:
        m = n + t
    max_HS_input = fixed_header + " " + str(m)
    hard_clauses_string = ''
    soft_clauses_string = ''
    neg = []
    nc = 0

    # building hard constraint input to max_HS input
    if noiseless:
        for i in range(t):
            if y[i] == 1:
                if a[i]:
                    local_hard = str(hard_weight) + " "
                    nc = nc + 1
                    for element in a[i]:
                        local_hard += str(element) + " "
                    local_hard += " 0\n"
                    hard_clauses_string += local_hard
            else:
                if a[i]:
                    for element in a[i]:
                        if element not in neg:
                            nc = nc + 1
                            neg.append(element)
                            local_hard = str(hard_weight) + " -" + str(element) + " 0\n"
                            hard_clauses_string += local_hard
    # noisy settings
    else:
        for i in range(t):
            if y[i] == 1:
                if a[i]:
                    local_hard = str(hard_weight) + " "
                    nc = nc + 1
                    for element in a[i]:
                        local_hard += str(element) + " "
                    local_hard += (str(n + i + 1))
                    local_hard += " 0\n"
                    soft_clauses_string += str(noise_weight) + " -" + str(n + i + 1) + " 0\n"
                    hard_clauses_string += local_hard
            else:
                if a[i]:
                    for element in a[i]:
                        nc = nc + 1
                        local_hard = str(hard_weight) + " -" + str(element) + " " + str(n + i + 1) + " 0\n"
                        hard_clauses_string += local_hard
                    soft_clauses_string += str(noise_weight)  + " -" + str(n + i + 1) + " 0\n"

    # add soft constraint to ensure minimum number of item faulty to max_HS input
    for j in range(1, n + 1):
        if j not in neg:
            nc += 1
            soft_clauses_string += str(soft_weight) + " -" + str(j) + " 0\n"

    max_HS_input += " " + str(nc) + " " + str(hard_weight) + "\n"

    max_HS_input += hard_clauses_string + soft_clauses_string

    with open(input_for_max_HS, "w") as output_file:
        output_file.write(max_HS_input)

    return

# non compact output is create output a file containing a MaxSAT instance
# in the format of the non-compact XOR enconding
# n is the number of variables
# t is the number of group that has been tested
# y is the output result of the group testing instance
# a is the recovery matrix
# noiseless is a boolean, True if the problem is noiseless, False otherwise
# noise_weight is the weight associated to the noise constraint, it expresses the lambda
# lambda is the trade-off between noisy and faulty, we express only the noise weight as
# the weight associated to the faultiness is fixed to 1
# for optimization purpose the function directly generate the string to be included in the input file
def non_compact_output(n, t, x, y, a, noiseless, noise_weight):

    m = n + t

    max_HS_input = fixed_header + " " + str(m)
    hard_clauses_string = ''
    soft_clauses_string = ''
    neg = []
    nc = 0

    # noisy settings
    for i in range(t):
        if y[i] == 1:
            if a[i]:

                # first part of XOR constraint
                for element in a[i]:
                    local_hard = str(hard_weight) + " "
                    nc = nc + 1
                    local_hard += " -" + str(element) + " "
                    local_hard += "-" + (str(n + i + 1))
                    local_hard += " 0\n"
                    hard_clauses_string += local_hard

                # second part of XOR constraint
                local_hard = str(hard_weight) + " "
                nc = nc + 1
                for element in a[i]:
                    local_hard += str(element) + " "
                local_hard += (str(n + i + 1))
                local_hard += " 0\n"
                hard_clauses_string += local_hard

                soft_clauses_string += str(noise_weight) + " -" + str(n + i + 1) + " 0\n"
        else:
            if a[i]:
                # first part of XOR constraint
                for element in a[i]:
                    nc = nc + 1
                    local_hard = str(hard_weight) + " -" + str(element) + " " + str(n + i + 1) + " 0\n"
                    hard_clauses_string += local_hard

                # second part of XOR constraint
                nc = nc + 1
                local_hard = str(hard_weight) + " "
                for element in a[i]:
                    local_hard += str(element) + " "
                local_hard += "-" + (str(n + i + 1))
                local_hard += " 0\n"
                hard_clauses_string += local_hard

    # add soft constraint to ensure minimum number of item faulty to max_HS input
    for j in range(1, n + 1):
        if j not in neg:
            nc += 1
            soft_clauses_string += str(soft_weight) + " -" + str(j) + " 0\n"

    max_HS_input += " " + str(nc) + " " + str(hard_weight) + "\n"

    max_HS_input += hard_clauses_string + soft_clauses_string

    with open(input_for_max_HS, "w+") as output_file:
        output_file.write(max_HS_input)

    return


