import os
import pandas as pd
from analyze_bench import parse_input, analyze_bench

"""
    This file is simply to facilitate the run of analysis and it is not meant 
    to be used by command-line.
"""

log4j = os.path.join('../results/log4j2')
druid = os.path.join('../results/druid')
pgdbc = os.path.join('../results/pgdbc')
netty = os.path.join('../results/netty')
h2o3 = os.path.join('../results/h2o-3')
gscollections = os.path.join('../results/gs-collections')

projects = [log4j, druid, pgdbc, netty, h2o3, gscollections]

LOOP = 'exp-LOOP-out'
RETU = 'exp-RETU-out'
FORK = 'exp-FORK-out'
FINA = 'exp-FINA-out'
INVOv2 = 'exp-INVOv2-out'
INVO = 'exp-INVO-out'


experiments = [INVO, INVOv2, LOOP, FINA, RETU, FORK]

parse_before_analyze = True

output = 'analysis'

if __name__ == '__main__':

    for p in projects:
        for exp in experiments:
            output_folder = os.path.join(p, exp, 'analysis')

            inputConsistency = True
            original = None
            original_folder = None
            fixed = None
            fixed_folder = None

            if parse_before_analyze:

                original_folder = os.path.join(p, exp, 'original')
                fixed_folder = os.path.join(p, exp, 'fixed_full')

                if not os.path.isdir(original_folder) or not os.path.isdir(fixed_folder):
                    print("Directories %s and/or %s do not exist in the file system." % (original_folder, fixed_folder))
                    inputConsistency = False

            else:
                original = os.path.join(p, exp, 'original','original-all.csv')
                fixed = os.path.join(p, exp, 'fixed_full', 'fixed-all.csv')

                if os.path.isfile(original) and os.path.isfile(fixed):
                    original = pd.read_csv(original)
                    fixed = pd.read_csv(fixed)

                else:
                    print("Aggregated files %s and/or %s do(es) not exist in the file system." % (
                    original, fixed))
                    inputConsistency = False

            if inputConsistency:
                # Parse
                original_df, fixed_df = parse_input(original=original, originalfolder=original_folder,
                                                    fixed=fixed, fixedfolder=fixed_folder)
                # Analyze
                analyze_bench(original_df, fixed_df, output_folder)
