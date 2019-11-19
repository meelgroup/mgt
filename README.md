# MGT (MaxSAT for Group Testing)

This file contains the information for an AAAI2020 reader/attender to use the prototype of MGT, in particular the two benchmark of MGT and MGT vs LP-relax.

## Installation
In order to use the python script you need to have python 3 and have installed CPlex library from IBM.
You must install [MaxHS](http://www.maxhs.org/) solver. (You will find instruction on the web page)
You must set up the Python [API](https://www.ibm.com/support/knowledgecenter/SSSA5P_12.7.0/ilog.odms.cplex.help/CPLEX/GettingStarted/topics/set_up/Python_setup.html) of CPLEX.

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
