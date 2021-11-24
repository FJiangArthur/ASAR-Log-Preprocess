"""
For 2470 Team: There is a hardcoded column id "Content" in logparser.
"""

import argparse
import sys
sys.path.append('../')
from logparser import IPLoM, Drain, LenMa, LFA, LogCluster, LogMine, SLCT, LogSig, Spell
#
# parser = argparse.ArgumentParser()
# parser.add_argument("--IPLoM", default=False, type=bool)
# parser.add_argument("--Drain", default=False, type=bool)
# parser.add_argument("--LenMa", default=True, type=bool)
# parser.add_argument("--LFA", default=False, type=bool)
# parser.add_argument("--LogCluster", default=False, type=bool)
# parser.add_argument("--LogMine", default=False, type=bool)
# parser.add_argument("--SLCT", default=False, type=bool)
# parser.add_argument("--LogSig", default=False, type=bool)
# parser.add_argument("--Spell", default=False, type=bool)
# parser.add_argument("--file_path", type=str)
# params = vars(parser.parse_args())

def parse_util(input_dir, log_name, regex, log_format):
    input_dir  = input_dir
    log_file     = log_name

    output_dir = 'Lenma_result_msg_only/'
    threshold  = 0.9 # TODO description (default: 0.9)

    parser = LenMa.LogParser(input_dir, output_dir, log_format, threshold=threshold, rex=regex)
    parser.parse(log_file)

    rsupport   = 10 # The minimum threshold of relative support, 10 denotes 10%
    output_dir = 'LogCluster_result_msg_only/' # The output directory of parsing results
    parser = LogCluster.LogParser(input_dir, log_format, output_dir, rsupport=rsupport)
    parser.parse(log_file)

    levels     = 2 # The levels of hierarchy of patterns
    max_dist   = 0.001 # The maximum distance between any log message in a cluster and the cluster representative
    k          = 1 # The message distance weight (default: 1)
    output_dir = 'LogMine_result_msg_only/' # The output directory of parsing results
    parser = LogMine.LogParser(input_dir, output_dir, log_format, rex=regex, levels=levels, max_dist=max_dist, k=k)
    parser.parse(log_file)

    group_number = 14 # The number of message groups to partition
    output_dir   = 'LogSig_result_msg_only/' # The output directory of parsing results
    parser = LogSig.LogParser(input_dir, output_dir, group_number, log_format, rex=regex)
    parser.parse(log_file)

    support    = 10  # The minimum support threshold
    output_dir = 'SLCT_result_msg_only/'  # The output directory of parsing results
    parser = SLCT.LogParser(log_format=log_format, indir=input_dir, outdir=output_dir,
                            support=support, rex=regex)
    parser.parse(log_file)

    tau        = 0.5  # Message type threshold (default: 0.5)
    output_dir = 'Spell_result_msg_only/'  # The output directory of parsing results
    parser = Spell.LogParser(indir=input_dir, outdir=output_dir, log_format=log_format, tau=tau, rex=regex)
    parser.parse(log_file)

    output_dir = 'Drain_result_msg_only/'  # The output directory of parsing results
    st         = 0.5  # Similarity threshold
    depth      = 4  # Depth of all leaf nodes
    parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex)
    parser.parse(log_file)

    maxEventLen  = 2000  # The maximal token number of log messages (default: 200)
    step2Support = 0  # The minimal support for creating a new partition (default: 0)
    CT           = 0.35  # The cluster goodness threshold (default: 0.35)
    lowerBound   = 0.25  # The lower bound distance (default: 0.25)
    upperBound   = 0.9  # The upper bound distance (default: 0.9)
    regex        = []  # Regular expression list for optional preprocessing (default: [])
    output_dir = 'IPLoM_result_msg_only/'  # The output directory of parsing results
    parser = IPLoM.LogParser(log_format=log_format, indir=input_dir, outdir=output_dir,
                             maxEventLen=maxEventLen, step2Support=step2Support, CT=CT,
                             lowerBound=lowerBound, upperBound=upperBound, rex=regex)
    parser.parse(log_file)

    output_dir = 'LFA_result_msg_only/' # The output directory of parsing results
    parser = LFA.LogParser(input_dir, output_dir, log_format, rex=regex)
    parser.parse(log_file)


if __name__ == '__main__':
    log_format = '<LineID>,<BLOCK_TIME_UNIQUE_ID>,<Content>'
    input_dir = './'
    log_name = 'Intrepid_RAS_0901_0908_scrubbed.log'

