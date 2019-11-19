import mgt_benchmark as mgt
import mgt_lp_comparison as mgt_lp
import exp_script as plot
import setup


# sample script 

mgt.main_varying_maxhs(250, 0.03, True, 1)
plot.parser(1)

mgt_lp.main_comparison_maxhs_lp(250, 0.03, True, 1)
plot.parser_comparison(1)

