# Studying Bad Practices in JMH Benchmarks - Online Appendix


This repository contains the appendix of the Bad Practices in JMH Benchmarks study. 
This appendix holds the following data:
1. The full list of bad JMH practices occurrences on 123 projects (RQ1).
2. The results of our impact analysis on 6 projects (RQ2). 
3. A reference to our tool: SpotJMHBugs (submodule).
4. References to the studied projects repositories, containing the fix patches and the pull requests.

Our paper is still under revision.

## RQ1. Ocurrence of bad JMH practices
This folder contains...

## RQ2. Impact of bad JMH practices
This folder contains the data collected and the scripts used to analyze the impact assessment of bad JMH practices. The structure of the folder is as follows:
- `projects`: the studied projects as git submodules. Each project contains the fixt-patches used to evaluate the impact if bad JMH practices as well as the pull requests made into the respective main projects.
- `results`: folder containing the 1) raw results per project, 2) the combined raw results and the 3) summarized aggregated results. 
- `scripts`: the python and Jupyter notebook scripts used to analyze the data.
- `plots`: plots presented and/or cited in the paper. 
For more details, see also the README in their respective sub-folders.


