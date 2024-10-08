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
graph LR;
    A[MainDo.do] --> |Data clearing for EXIOBASE|B[CleanEXIOBASE.do]
    C([Flow/transactions matrix]) --> |Input|D[EXIOBASE_NCLI.dta]
    E([CO2 emisions]) --> |Input|D
    B --> |Calculate Net Carbon Leakage Index|D
    A --> |Calculate and draw CLR|F[DrawCarbonLeakageRate.do]
    A --> |Decompose and analyze NCLI|G[DecomposeElasticityNetCarbonLeakage.do]
    A --> |Variance-covariance analysis|H[DecomposeElasticityVariance.do]
    A --> |Draw alphas, create figures|I[DrawAlphaScatterplot.do]
    F --> J[EXOBASE_CLR.dta]
    C --> |Create trade matrix|K[GOABSts.dta]
   
```
