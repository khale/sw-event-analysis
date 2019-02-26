#!/usr/bin/env python
import numpy as np
from optparse import OptionParser

parser = OptionParser(
        usage="usage: %prog [options]",
        description="Generate a synthetic software event experiment trace of a given type. Data "
                    "points will be sampled from an (approximately) normal distribution.")

parser.add_option("-t", 
                  "--type",
                  dest="exp_type",
                  default="one_core",
                  type="string",
                  help="The type of experiment to mimic. 'one_core' means an experiment "
                       "which only runs for N trials on a single core. 'many_core' means "
                       "an experiment with an additional independent variable represented by "
                       "a tuple (s,d), where s is source and d is destination. This means that "
                       "with c cores and n trials, there will be nc^2 data points.")

parser.add_option("-c",
                  "--core-count",
                  dest="core_count",
                  default=1,
                  type="int",
                  help="If this is an experiment meant to run on a multi-core machine, this "
                       "represents the number of total cores on which to run the experiment. The "
                       "default is 1.")

parser.add_option("-s",
                  "--scale-factor",
                  dest="scale_factor",
                  type="int",
                  default=1000,
                  help="The random samples used for the fake values are by default scaled by 1000 "
                       "(to reflect reasonable cycle counts). This will change that scaling factor.")

parser.add_option("-n",
                  "--trials",
                  dest="trials",
                  default=100,
                  type="int",
                  help="How many times to measure each event. Default is 100.")


def sample_pos_int(mu, sig):
    x = int(np.random.normal(mu, sig, None))
    return (x if x >= 0 else sample_pos_int(mu, sig))

def do_many_cores(trials, cores, sf):
    print("Generating {} trials, {} cores".format(trials, cores))

    for i in xrange(trials):
        for j in xrange(cores):
            for k in xrange(cores):
                if (j == k): # don't need values along the diag
                    continue
                val = sample_pos_int(sf, sf/10)
                print("{},{},{},{}".format(i, j, k, val))


def do_one_core(trials, sf):
    print("# Generating {} fake trials".format(trials))

    for i in xrange(trials):
        val = sample_pos_int(sf, sf/10)
        print("{},{}".format(i, val))


def main():

    (opts, args) = parser.parse_args()

    if opts.exp_type == "one_core":
        do_one_core(opts.trials, opts.scale_factor)
    else:
        do_many_cores(opts.trials, opts.core_count, opts.scale_factor)


# output is 
if __name__ == "__main__":
    main()
