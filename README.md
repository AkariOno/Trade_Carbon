# EITEs

This repository includes codes for "Which Industries Are Prone To Carbon Leakage?". To start, 
1. Clone this repository
2. Get raw data from various sources
   - WIOD 2016 edition
   - WIOD environmental account
   - EXIOBASE
        - Flow/transactions matrix
        - CO2 emissions (production based accounts per sector)
   - Trade elasticity (WIOD 2016)
3. Change current directory in MainDo.do
4. Run MainDo.do

By running these programs, the following data and figures will be output from each do file stored in this repository:

```mermaid
graph LR;

%% Main Process Section
subgraph Main_Process [Main Data Processing]
    [MainDo.do]
    [CleanEXIOBASE.do]
    [DecomposeElasticityNetCarbonLeakage.do]
    [DecomposeElasticityVariance.do]
    [DrawAlphaScatterplot.do]
    [DrawCarbonLeakageRate.do]
end

%% Data Generation Section
subgraph Data_Generation [Data Generation]
    ([Flow/transactions matrix])
    [GOABSts.dta]
    [EXIOBASE_NCLI.dta]
    ([CO2 emissions])
    [EXOBASE_CLR.dta]
end

%% Data Visualization Section
subgraph Data_Visualization [Visualization & Analysis]
    (Figures of CLR)
    (Barplot of decomposed NCLI)
    (NCLItable)
    (Scatterplot of alphas)
end

%% Connections between nodes
[MainDo.do] --> |Data clearing for EXIOBASE| [CleanEXIOBASE.do]
[MainDo.do] --> |Decompose and analyze NCLI| [DecomposeElasticityNetCarbonLeakage.do]
[MainDo.do] --> |Variance-covariance analysis| [DecomposeElasticityVariance.do]
[MainDo.do] --> |Draw alphas, create figures| [DrawAlphaScatterplot.do]
[MainDo.do] --> |Calculate and draw CLR| [DrawCarbonLeakageRate.do]

([Flow/transactions matrix]) --> |Create trade matrix| [GOABSts.dta]
([CO2 emissions]) --> |Input| [EXIOBASE_NCLI.dta]
[CleanEXIOBASE.do] --> |Calculate Net Carbon Leakage Index| [EXIOBASE_NCLI.dta]
[GOABSts.dta] --> |Input| [EXIOBASE_NCLI.dta]
[GOABSts.dta] --> |Input| [EXOBASE_CLR.dta]
[DrawCarbonLeakageRate.do] --> [EXOBASE_CLR.dta]
[EXOBASE_CLR.dta] --> (Figures of CLR)
[EXIOBASE_NCLI.dta] --> |Input| (Barplot of decomposed NCLI)
[DecomposeElasticityNetCarbonLeakage.do] --> |Analysis and barplot| (Barplot of decomposed NCLI)
[EXIOBASE_NCLI.dta] --> |Input| (NCLItable)
[DecomposeElasticityVariance.do] --> |Analysis| (NCLItable)
[EXIOBASE_NCLI.dta] --> |Input| (Scatterplot of alphas)
[DrawAlphaScatterplot.do] --> |Scatterplot| (Scatterplot of alphas)
   
```
