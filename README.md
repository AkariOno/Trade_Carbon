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
style Main_Process font-size:20px
    A[MainDo.do]
    B[CleanEXIOBASE.do]
    C[DecomposeElasticityNetCarbonLeakage.do]
    D[DecomposeElasticityVariance.do]
    E[DrawAlphaScatterplot.do]
    F[DrawCarbonLeakageRate.do]
end

%% Data Generation Section
subgraph Data_Generation [Data Generation]
style Data_Generation font-size:20px
    G([Flow/transactions matrix])
    H[GOABSts.dta]
    I[EXIOBASE_NCLI.dta]
    J([CO2 emissions])
    K[EXOBASE_CLR.dta]
end

%% Data Visualization Section
subgraph Data_Visualization [Visualization & Analysis]
style Data_Visualization font-size:20px
    L(Figures of CLR)
    M(Barplot of decomposed NCLI)
    N(NCLItable)
    O(Scatterplot of alphas)
end

%% Connections between nodes
A --> |Data clearing for EXIOBASE| B
A --> |Decompose and analyze NCLI| C
A --> |Variance-covariance analysis| D
A --> |Draw alphas, create figures| E
A --> |Calculate and draw CLR| F

G --> |Create trade matrix| H
J --> |Input| I
B --> |Calculate gross output and absorption| H
H --> |Calculate Net Carbon Leakage Index| I
H --> |Input| K
F --> K
K --> L
I --> |Input| M
I --> |Input| N
I --> |Input| O
C --> |Analysis and barplot| M
D --> |Analysis| N
E --> |Scatterplot| O
   
```
