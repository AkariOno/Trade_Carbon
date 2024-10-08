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
    %% direction TB
    A[MainDo.do]
    B[CleanEXIOBASE.do]
    F[DecomposeElasticityNetCarbonLeakage.do]
    G[DecomposeElasticityVariance.do]
    H[DrawAlphaScatterplot.do]
    I[DrawCarbonLeakageRate.do]
end

%% Data Generation Section
subgraph Data_Generation [Data Generation]
    direction TB
    C([Flow/transactions matrix])
    K[GOABSts.dta]
    D[EXIOBASE_NCLI.dta]
    E([CO2 emissions])
    J[EXOBASE_CLR.dta]
end

%% Data Visualization Section
subgraph Data_Visualization [Visualization & Analysis]
    direction TB
    L(Figures of CLR)
    M(Barplot of decomposed NCLI)
    N(NCLItable)
    O(Scatterplot of alphas)
end

%% Connections between nodes
A --> |Data clearing for EXIOBASE| B
A --> |Decompose and analyze NCLI| F
A --> |Variance-covariance analysis| G
A --> |Draw alphas, create figures| H
A --> |Calculate and draw CLR| I

C --> |Create trade matrix| K
E --> |Input| D
B --> |Calculate Net Carbon Leakage Index| D
K --> |Input| D
K --> |Input| J
I --> J
J --> L
D --> |Input| M
F --> |Analysis and barplot| M
D --> |Input| N
G --> |Analysis| N
D --> |Input| O
H --> |Scatterplot| O


   
```
