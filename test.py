import mgt_benchmark as mgt
import mgt_lp_comparison as mgt_lp
import exp_script as plot
import setup

# solve noiseless group testing by MaxSAT
mgt.main_varying_maxhs(n=200, p=0.03, noiseless=True, verbose=True)
plot.parser()

# solve noisy group testing by MaxSAT
mgt.main_varying_maxhs(n=200, p=0.03, noiseless=False, noise_probability=0.03,  verbose=True)
plot.parser()


# compare MaxSAT based solution to LP-based solution
mgt_lp.main_comparison_maxhs_lp(n=200, p=0.03, noiseless=True, verbose=True)
plot.parser_comparison()


# extend the comparison in noisy group testing
mgt_lp.main_comparison_maxhs_lp(n=200, p=0.03, noiseless=False, noise_probability=0.03,  verbose=True)
plot.parser_comparison()
