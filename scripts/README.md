### Scripts for running and analyzing the benchmarks

TODO: Add a proper documentation in the scripts

Main scripts:

* execute-bench: Run the experiment on multiple jars and multiple benchmarks. See --help for the correct usage.

* jmh-parser: Parse the .out jmh output files into an aggregated .csv file. See --help for the correct usage.
		Currently, this script can also be executed within analyze_bench. 

* analyze-bench: Parse and analyze the benchmark results. This script uses the /analysis function to generate:
    * normality: Analyze the distribution of the results.
    * anova: Run the anova significant test on the results and plot only statistically different benchmarks.
    * median: Run the Mood's median test and plot only only statistically different benchmarks
    * wilcoxon: Rnu the Wilcoxon non-parametric test 
    * cliffsdelta: Calculate the cliffs-delta effect sizes
    * Summarize the results into summary.csv

