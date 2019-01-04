### Scripts for running and analyzing the benchmarks

Main Python scripts:

* `execute-bench`: Run the experiment on multiple jars and multiple benchmarks. See --help for the correct usage.

* `jmh-parser`: Parse the .out jmh output files into an aggregated .csv file. See --help for the correct usage.
		Currently, this script can also be executed within analyze_bench. 

* `analyze-bench`: Parse and analyze the benchmark results. This script uses the /analysis folder functions to generate:
    * normality: Analyze the distribution of the results.
    * anova: Run the anova significant test on the results and plot only statistically different benchmarks.
    * median: Run the Mood's median test and plot only only statistically different benchmarks
    * wilcoxon: Rnu the Wilcoxon non-parametric test 
    * cliffsdelta: Calculate the cliffs-delta effect sizes
    * Summarize the results into summary.csv
    
* `batch-analysis`: Runs the entire analysis parsing all output files of all experiments and grouping them into the `results/raw-results.csv`.

Main Jupyter Notebook scripts: The notebook scripts are used to generate all figures/plots present in the paper. All scripts are runnable and rely on the already processed files from the `results` folder.

* `summarize-results`: Reads from the raw-results and aggregate all experiments iterations by their medians, avg, confidence interval...

* `plot-[badJMHpractice]-examples`: Generates the comparison plots present in the paper and in RQ2 summary. 

Scripts used to generate plots that do not feature in the paper are in the `archived` folder.




