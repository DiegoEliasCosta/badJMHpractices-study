import os
import subprocess
import argparse
import time
from datetime import timedelta

DEBUG = False


def retrieve_class_and_method(benchmark):
    tokens = benchmark.split('.')

    class_idx = -1
    for idx, t in enumerate(tokens):
        if t[0].isupper():
            class_idx = idx # Find class by checking the UPERCASE

    if class_idx == -1:
        class_idx = 1 # Get the last term if we can't find it

    return '_'.join(tokens[-class_idx:])


def format_output(output_path, jar, benchmark, suffix, trial, extension):
    file_name = '%s_%s_%s_trial%s' % (os.path.basename(jar).replace('.jar', ''),
                                      retrieve_class_and_method(benchmark),  # Only the class name for now
                                      suffix, trial)

    file_name = '%s.%s' % (file_name.replace('.', '_'), extension)
    file_path = os.path.join(output_path, file_name)
    return file_path


def run_benchmark_series(ntrials, bench_jars, benchmarkSeries, output_path, suffix, params):

    for trial in range(1, ntrials + 1):
        start = time.time()
        print('\n\nRunning the Trial %d' % trial)
        for idx, benchmark in enumerate(benchmarkSeries):
            print('- Running the %d benchmark with ID: %s' % (idx + 1, benchmark))
            for jar in bench_jars:
                print('-- Running the benchmark exported in the jar = %s' % jar.name)
                run_benchmark(benchmark, jar.name, output_path, params, suffix, trial, '---')
        end = time.time()
        elapsed_time = end - start
        estimated_time = elapsed_time * (ntrials - trial)
        print('\n-----------------------------------------------------------------')
        print('Time spent on the trial              %s' % str(timedelta(seconds=elapsed_time)))
        print('Estimated Time to finish all Trials  %s' % str(timedelta(seconds=estimated_time)))
        print('\n-----------------------------------------------------------------')

    print('\n---------------------------------------------------------------')
    print('                             FINISHED!')
    print('\n---------------------------------------------------------------')


def run_benchmark(benchmark, jar, output_path, params, suffix, trial, tabs):

    # Prepare the output JAR_FILE + BENCHMARK
    csvOutput = format_output(output_path, jar, benchmark, suffix, trial, 'csv')
    textOutput = format_output(output_path, jar, benchmark, suffix, trial, 'out')
    errOutput = format_output(output_path, jar, benchmark, suffix, trial, 'err')

    # Prepare the command to be run
    command = 'java -jar "%s" %s %s -rf csv -rff %s -o %s' % (jar, benchmark, params,
                                                              csvOutput,
                                                              textOutput)
    if DEBUG:
        print('%s Running the command:\n\t %s' % (tabs, command))

    print('%s Check the continuously updated output text file  %s' % (tabs, textOutput))
    with open(errOutput, "w") as out:
        subprocess.run(command, shell=True, check=True, stdout=out)
    print('%s Benchmark run sucessfully! ' % tabs)
    print('%s Aggregated benchmark results stores in %s' % (tabs, csvOutput))


def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run a series of JMH benchmarks.')

    parser.add_argument('jars', nargs='+',type=argparse.FileType('r'), help='List of benchmark jar '
                                                                               'files to be run.')

    parser.add_argument('--ntrials', type=int, default=1, help='Amount of trials to be run in the benchmark. '
                                                               'Differently form the fork benchmark parameter, this '
                                                               'parameter allow us to re-run the entire benchmark a number'
                                                               'of times.')

    parser.add_argument('--outputdir', default=os.getcwd(), type=readable_dir,
                        help='The output folder where every benchmark result will be stored.')

    parser.add_argument('--benchmarkfile', type=argparse.FileType('r'),
                        help='A text file containing the benchmarks to be run. '
                             'Each line of the file is run in a separated command.')

    parser.add_argument('--singlecommand', action='store_true', help='If passed together with benchmarkFile'
                                                                     'the script will execute every line in the benhcmarkFile'
                                                                     'with a single command.')

    parser.add_argument('--benchmark', type=str, help='Benchmark identifier to run')

    parser.add_argument('--sanitytest', action='store_true',
                        help='Run the benchmark in the fastest way possible `-wi 1 -i 1 -f 1`.')

    parser.add_argument('--suffix', help='All output files will be saved with the specified suffix.')

    parser.add_argument('--param', type=str, help='Parameters to be used by JMH benchmark. '
                                                  'This parameter will be forwarded to JMH benchmark directly (no '
                                                  'validation will be performed in the script). '
                                                  'Specify this parameter as one single string WITH DOUBLE quotes.')

    parser.add_argument('--verbose', action='store_true', help='Print the executed commands')

    args = parser.parse_args()

    if args.verbose:
        DEBUG = args.verbose

    if args.sanitytest:
        params = '-wi 1 -i 1 -f 1'
        suffix = 'sanity'

    print('Starting execute-bench Script')
    print('Parameters Specified:')
    for arg in vars(args):
        print('\t%s = %s' % (arg, getattr(args, arg)))

    print('List of benchmarks ')

    # Read benchmark file
    if args.benchmarkfile:
        benchmarkfile = args.benchmarkfile
        benchs = benchmarkfile.read().split('\n')
        # Avoid duplicates
        benchSeries = set(benchs)
        if args.singlecommand:
            benchSeries = ['"' + ' '.join(benchSeries) + '"'] # Format as a single element
        print('Total of %d benchmarks specified in benchmark file.' % len(benchSeries))

    elif args.benchmark:
        benchSeries = [args.benchmark]
        print('Benchmarks run with the following regex %s' % args.benchmark)

    else:
        benchSeries = [] # all benchmarks
        print('All benchmarks will be run. ')

    param = ''
    if args.param:
        param = args.param

    # Run the benchmarks
    run_benchmark_series(args.ntrials, args.jars, benchSeries, args.outputdir, args.suffix, param)
