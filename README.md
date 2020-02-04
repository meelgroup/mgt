# MGT (MaxSAT-based framework for Group Testing)

MGT is a novel MaxSAT-based framework for solving the decoding phase of group testing. This tool is based on our [AAAI-20 paper](https://bishwamittra.github.io/publication/aaai_2020/AAAI-CiampiconiL.690.pdf).   

## Installation
In order to use this tool, Python 3 is to be installed in the system. 
The tool primarily uses [MaxHS](https://github.com/fbacchus/MaxHS) as the underlying MaxSAT solver. However, any off-the-shelf MaxSAT solver can be used with a minor modification in the source file. MaxHS requires [CPLEX](https://www.ibm.com/support/pages/downloading-ibm-ilog-cplex-optimization-studio-v1290) to process the arithmetic computation of the MaxSAT problem.
To setup the Python API of CPLEX, please follow the instruction from [here](https://www.ibm.com/support/knowledgecenter/SSSA5P_12.7.0/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/Python_setup.html).

## Usage
Open your terminal and go to the code folder.

In general the framework works with two separated modules. The first (mgt_benchmark.py or mgt_lp_comparison.py), generate the group testing instance, perform the encoding and solve it generating the solution data output file (saved in data-output subfolder). The second parse the output data and then plot it using matplotlib(saved in plot-output subfolder).

You can modify the sample script or import the python module and run them. 
In the first case there is already a script example, so please refer to that.

```bash
python experiment_script.py
```

There are two main function, one for each of the two process (generate data, plot it)
To generate data from MGT
```python
main_varying_maxhs(n, p, noiseless, u)
```
To generate data from MGT vs LP
```python
main_comparison_maxhs_lp(n, p, noiseless, u)
```
n is the number of items, p is the ratio faulty/items and noiseless is True for noiseless settings and False for noisy. u is and index number to save the data. (MGT and MGTvsLP data output will be not overwritten if are saved with same u).
So if you want to use the framework from the console:
open the python console
```bash
python
```
then
```python
import mgt_benchmark as mgt
mgt.main_varying_maxhs(250,0.03,True,1)
import data_to_plot as dtp
dtp.parser(1)
```

or for comparison between MGT and LP-relax (this will plot also computation effort in terms of time, in order to visualize phase transition)

```python
import mgt_lp_comparison as mgt_lp
mgt_lp.main_comparison(250,0.03,True,1)
import data_to_plot as dtp
dtp.parser_comparison(1)
```

You can modify the script "exp_script.py" or create a new if you prefer. 
You will find further documentation inside the python modules.

Thank You

## License
[AAAI2020](http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=90881)
