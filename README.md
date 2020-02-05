# MGT (MaxSAT-based framework for Group Testing)

MGT is a novel MaxSAT-based framework for solving the decoding phase of [Group testing](https://en.wikipedia.org/wiki/Group_testing). This tool is based on our [AAAI-20 paper](https://bishwamittra.github.io/publication/aaai_2020/AAAI-CiampiconiL.690.pdf).   

## Installation
The scripts are compatible with Python 3 or higher. 
The tool  uses [MaxHS](https://github.com/fbacchus/MaxHS) as the underlying MaxSAT solver.  MaxHS requires [CPLEX](https://www.ibm.com/support/pages/downloading-ibm-ilog-cplex-optimization-studio-v1290) to process the arithmetic computation of the MaxSAT problem.
To setup the Python API of CPLEX, please follow the instruction from [here](https://www.ibm.com/support/knowledgecenter/SSSA5P_12.7.0/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/Python_setup.html).

## Scripts Description

``mgt_benchmarks.py`` contains the subroutine ``main_varying_maxhs`` to generate  and solve a group testing instance given the number of items `n`, probability of defective items `p`, type of tests (noiseless or noisy), and probability of noisy tests (in case of noisy test). This subroutine calls a set of supporting subroutines from ``group_testing_function.py``,  ``max_sat_interface.py``, and ``exp_script.py``. More specifically,  ``group_testing_function.py`` contains useful scripts to generate the random item vector, the pool matrix, and to compute results after recovering the items. ``max_sat_interface.py`` acts as an interface to call a MaxSAT solver to solve the group testing instance. This script can be modified to use any off-the-shelf MaxSAT solver for solving the same problem. ``exp_script.py`` contains subroutines to show the experimental results as plots. 

To compare MaxSAT-based framework with [LP-relaxed](https://ieeexplore.ieee.org/document/6288622) (linear programming relaxation) approach, one would call the subroutine ``main_comparison_maxhs_lp`` from ``mgt_lp_comparison.py`` script. Moreover, ``general_lp_interface.py`` acts as an interface for calling a LP solver (the default choice is CPLEX) to solve the group testing instance. 

Additionally, ``setup.py`` contains different choices including the directory of temporary files and generated plots.



## Usage

To solve a noiseless group testing instance using MaxSAT, run the following commands.
```
import mgt_benchmark as mgt
import exp_script as plot
mgt.main_varying_maxhs(n=100, p=0.03, noiseless=True, verbose=True)
plot.parser(verbose=True)
```
The above commands solve a noiseless group testing instance for 100 items with 3% defective items. 

To solve a noisy group testing instance with  probability of noise as 5%, run the following command.
```
mgt.main_varying_maxhs(n=100, p=0.03, noiseless=False, noise_probability=0.05, verbose=True)
```

To compare the performance between the  MaxSAT formulation and the LP formulation, run the following commands. 

```
import mgt_lp_comparison as mgt_lp
import exp_script as plot
mgt_lp.main_comparison_maxhs_lp(n=100, p=0.03, noiseless=True, verbose=True)
plot.parser_comparison()
```

Similarly, to compare performance in the noisy group testing, run the following command.
```
mgt_lp.main_comparison_maxhs_lp(n=100, p=0.03, noiseless=False, noise_probability=0.05, verbose=True)
```

Run   ``python test.py``, that combines all above commands. 


# Issues, questions, bugs, etc.
Please click on "issues" at the top and [create a new issue](https://github.com/meelgroup/mgt/issues). All issues are responded to promptly.

# Contact
[Bishwamittra Ghosh](https://bishwamittra.github.io/) (bghosh@u.nus.edu)

# How to cite
@inproceedings{CGSM20,<br />
author={Ciampiconi, Lorenzo and Ghosh, Bishwamittra and Scarlett, Jonathan and  Meel, Kuldeep S.},<br />
title={A {MaxSAT}-based Framework for Group Testing},<br />
booktitle={Proceedings of AAAI},<br />
year={2020},}
