### Performance Impact Results

In this folder we store the benchmark results of the experiment of assessment of anti-pattern performance impact .

Each project folder has a similar folder structure. Take the ```pgdbc``` project for example:

```
pgdbc
│   
│	FINA.html -> Summary of the results for the FINA antipattern
│
└───exp-FINA-out -> Contain results for benchmarks that fixed the FINA antipattern.
│   │   
│   └── analysis -> Here we store the charts and analyzed csv files
│   │   │  
│   │   │ 		summary.csv -> Aggregated summary of all benchmarks results for the FINA antipattern
│   │   │   
│   │   └─ ANOVA  -> Contains charts of benchmarks with significant avg differences according to ANOVA test 
│   │   │
│   │   └─ median -> Contains charts of benchmarks with significant median differences according to Mood's median test 
│   │   │
│   │   └─ normality -> Contains charts with significant different distributions according to D’Agostino and Pearson’ test
│   │
│   └─ original -> Raw data of the tests with the original jar from pgdbc project
│   │
│   └─ fixed_full -> Raw data of the tests with the .jar with the anti-patterns fixed.
│
└───exp-RETU-out
│   ...
└───exp-FORK-out
    ...
    
```

