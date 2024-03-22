# Data quality

## Flow
```mermaid
graph TD;
    A[Configure variables] --> B[Read SQL database];
    B --> V[Validation of input schema];
    V --> |Failure| X[Error alert];
    V --> |Success| C[Transform KPIs];
    C --> Y[Validation of output schema];
    Y --> |Failure| Z[Error alert]; 
    Y --> |Success| D[Save to DuckDB]; 
```

## Data Contract

::: app.schema.ProductSchema

## Functions

## Configure variables

::: app.etl.load_settings

## Read from SQL database

::: app.etl.extract_from_db

## Create KPIs

::: app.etl.transform

## Save to DuckDB

::: app.etl.load_to_duckdb