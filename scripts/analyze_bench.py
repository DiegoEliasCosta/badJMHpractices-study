import pandas as pd
import os
import argparse
import numpy as np
from utils import createIfNotExist
from analysis.normality import checkNormality, plotNormalityComparison
from analysis.anova import anovaCheck
from analysis.comparison_plot import comparissonPlot
from analysis.median import medianTest
from analysis.wilcoxon import wilcoxonTest
from analysis.cliffsdelta import applyCliffsDelta
from jmh_parser import parseFolder
from scipy import stats

ALPHA = 0.001

EXPERIMENT_COLS = ['Benchmark Mode', 'Measurement Unit', 'Package', 'Class', 'Method', 'Full params']
RELEVANT_COLS = ['Benchmark Mode', 'Measurement Unit', 'Package', 'Class', 'Method', 'Full params', 'Iteration',
                 'Fork', 'Trial', 'Score']

def analyze_bench(original_df, fixed_df, output):

    # Specify the numeric columns
    original_df['Score'] = pd.to_numeric(original_df['Score'])
    fixed_df['Score'] = pd.to_numeric(fixed_df['Score'])

    # Remove warmups
    fixed_df = fixed_df[fixed_df['Iteration Type'] == 'measured']
    original_df = original_df[original_df['Iteration Type'] == 'measured']

    # Normalize NAN
    fixed_df = fixed_df.fillna('')
    original_df = original_df.fillna('')

    # Focus on relevant columns
    fixed_df = fixed_df[RELEVANT_COLS]
    original_df = original_df[RELEVANT_COLS]

    # Remove Outliers > 3 STD
    original_df = original_df.groupby(EXPERIMENT_COLS).apply(filter_outlines)
    fixed_df = fixed_df.groupby(EXPERIMENT_COLS).apply(filter_outlines)

    # Join both Original + Fixed
    join_columns = ['Benchmark Mode', 'Measurement Unit', 'Package', 'Class', 'Method', 'Full params', 'Fork', 'Iteration', 'Trial']
    dataset = original_df.merge(fixed_df, on=join_columns, suffixes=['_original', '_fixed'])


    print(dataset.head())
    # ----------------- Normality Analysis ---------------------
    dataset = normality_analysis(dataset, EXPERIMENT_COLS, output)

    #  ---------------- ANOVA Analysis -------------------
    dataset = anova_analysis(dataset, EXPERIMENT_COLS, output)

    # ----------------- Median Analysis ------------------
    dataset = median_analysis(dataset, EXPERIMENT_COLS, output)

    # ----------------- Wilcoxon Analysis ------------------
    dataset = wilcoxon_analysis(dataset, EXPERIMENT_COLS, output)

    # ----------------- Cliffs Delta ------------------
    dataset = cliffsdelta_analysis(dataset, EXPERIMENT_COLS, output)

    # ----------------- Summary --------------------------

    summary = summarize(dataset, EXPERIMENT_COLS)
    print('Saving summary to %s' % os.path.join(output, 'summary.csv'))
    summary.to_csv(os.path.join(output, 'summary.csv'))

    pass


def filter_outlines(df):
    return df[np.abs(stats.zscore(df.Score)) < 3]

def summarize(dataset, experiment_cols):

    def summaryze_benchmarks(df):

        original = df['Score_original'].median()
        fixed = df['Score_fixed'].median()

        factor = fixed / original

        wilcoxon = df['Wilcoxon Test'].iloc[0]
        cliffs_size = df['Cliffs Delta Size'].iloc[0]
        cliffs_d = df['Cliffs Delta d'].iloc[0]

        return pd.DataFrame({
            'Original': [original],
            'Fixed': [fixed],
            'Factor': [factor],
            'Wilcoxom': [wilcoxon],
            'Cliffs Delta Size': [cliffs_size],
            'Cliffs Delta d': [cliffs_d],
        })

    summary = dataset.groupby(by=experiment_cols).apply(summaryze_benchmarks)
    return summary


def wilcoxon_analysis(dataset, experiment_cols, output):

    median_dir = os.path.join(output, 'wilcoxon')
    createIfNotExist(median_dir)

    dataset = dataset.groupby(by=experiment_cols).apply(wilcoxonTest, ALPHA)

    # Filter only benchmarks that have ANOVA significant difference
    median_diff = dataset.groupby(by=experiment_cols).filter(lambda x: x['Wilcoxon Test'].iloc[0] == True)
    median_diff.groupby(by=experiment_cols).apply(comparissonPlot, median_dir)
    return dataset

def cliffsdelta_analysis(dataset, experiment_cols, output):

    dataset = dataset.groupby(by=experiment_cols).apply(applyCliffsDelta, ALPHA)
    return dataset


def median_analysis(dataset, experiment_cols, output):

    median_dir = os.path.join(output, 'median')
    createIfNotExist(median_dir)

    dataset = dataset.groupby(by=experiment_cols).apply(medianTest, ALPHA)

    # Filter only benchmarks that have ANOVA significant difference
    median_diff = dataset.groupby(by=experiment_cols).filter(lambda x: x['Median Test'].iloc[0] == True)
    median_diff.groupby(by=experiment_cols).apply(comparissonPlot, median_dir)
    return dataset


def anova_analysis(dataset, experiment_cols, output):

    anova_dir = os.path.join(output, 'ANOVA')
    createIfNotExist(anova_dir)

    dataset = dataset.groupby(by=experiment_cols).apply(anovaCheck, ALPHA)

    # Filter only benchmarks that have ANOVA significant difference
    anova_diff = dataset.groupby(by=experiment_cols).filter(lambda x: x['ANOVA'].iloc[0] == True)
    anova_diff.groupby(by=experiment_cols).apply(comparissonPlot, anova_dir)
    return dataset


def normality_analysis(dataset, experiment_cols, output):

    normality_dir = os.path.join(output, 'normality')
    createIfNotExist(normality_dir)

    dataset = dataset.groupby(by=experiment_cols).apply(checkNormality, ALPHA)

    # Normality Plot
    normality_diff = dataset.groupby(by=experiment_cols).filter(
        lambda x: x['Normality_original'].sum() != x['Normality_fixed'].sum())
    normality_diff.groupby(by=experiment_cols).apply(plotNormalityComparison, normality_dir)
    return dataset


def read_pandas(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        raise argparse.ArgumentTypeError('not a valid result csv file - %s' % e)


def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


def writable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        try:
            os.makedirs(prospective_dir)
        except:
            argparse.ArgumentTypeError("outputfolder:{0} is not a writable dir".format(prospective_dir))
    return prospective_dir


def parse_input(original, originalfolder, fixed, fixedfolder):

    original_df = original
    if originalfolder:
        # If original folder then first parse the .out files
        original_file = os.path.join(originalfolder, 'original-all.csv')
        original_df = parseFolder(originalfolder)
        # Save in disk for debugging purposes
        original_df.to_csv(original_file)

    fixed_df = fixed
    if fixedfolder:
        # If fixed folder then first parse the .out files
        fixed_file = os.path.join(fixedfolder, 'fixed-all.csv')
        fixed_df = parseFolder(fixedfolder)
        # Save in disk for debugging purposes
        fixed_df.to_csv(fixed_file)

    return original_df, fixed_df


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compare two JMH benchmarks.')

    parser.add_argument('--original', type=read_pandas,
                        help='The file with the results of the benchmark from the original jar.')

    parser.add_argument('--originalfolder', type=readable_dir,
                        help='The folder containing the experiments for the original jar. '
                             'Every .out file will be first parsed into the aggregated csv.')

    parser.add_argument('--fixed', type=read_pandas,
                        help='The file with the results of the benchmark from the fixed jar.')

    parser.add_argument('--fixedfolder', type=readable_dir,
                        help='The folder containing the experiments for the original jar. '
                             'Every .out file will be first parsed into the aggregated csv.')

    parser.add_argument('--outputfolder', type=writable_dir, default=os.getcwd(), help='The output folder'
                                                                                        'where the charts will be stored')
    args = parser.parse_args()

    original_df, fixed_df = parse_input(original=args.original,
                                        originalfolder=args.originalfolder,
                                        fixed=args.fixed,
                                        fixedfolder=args.fixedfolder)

    print('------------------------------------------')
    print('         Analyzing the benchmarks')
    print('------------------------------------------')
    analyze_bench(original_df=original_df, fixed_df=fixed_df, output=args.outputfolder)