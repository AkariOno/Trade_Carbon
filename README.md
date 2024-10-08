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
graph TD;
   A[MainDo.do] --> |Data Clearing for EXIOBASE|B[CleanEXIOBASE.do]
    C[Flow/transactions matrix] --> |Input|B
    B --> |Calculate export, gross output, gross output share, absorption, trade flow/gross output, and trade flow/absorption|D[GOABSts.dta]
    D --> |Take GO ABS country level|E[GOABS.dta]
    B --> |Calculate energy expenditure|F[Energy.dta]
    B --> |Clean CO2 contents of production|G[CO2.dta]
    E --> |Calculate alpha and beta|H[countrydata.dta]
    F --> H
    G --> H
    H --> |Calculate world alpha|I[alphaw.dta]
    D --> |Calculate alphatilde|J[GOABStsalpha.dta]
    H --> J
    I --> J
    K[final_tariff_WIOD_rev2016_2022.dta] --> |Merge trade elasticity|J
    J --> |Calculate Net Carbon Leakage Index|L[EXIOBASE_NCLI.dta]
    M[CO2 emissions] --> |Input|G
```
