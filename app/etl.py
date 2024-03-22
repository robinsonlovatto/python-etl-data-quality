import os
import sys
from pathlib import Path

import pandas as pd
import pandera as pa
from dotenv import load_dotenv
from sqlalchemy import create_engine

from schema import ProductSchema, ProductSchemaKPI

def load_settings():
    """Load the settings from the environment variables."""
    dotenv_path = Path.cwd() / '.env'
    load_dotenv(dotenv_path=dotenv_path)
    
    settings = {
        "db_host": os.getenv('POSTGRES_HOST'),
        "db_user": os.getenv('POSTGRES_USER'),
        "db_pass": os.getenv('POSTGRES_PASSWORD'),
        "db_name": os.getenv('POSTGRES_DB'),
        "db_port": os.getenv('POSTGRES_PORT')
    }

    return settings

@pa.check_output(ProductSchema)
def extract_from_db(query: str) -> pd.DataFrame:
    """
    Extract data from the SQL database using the query provided.
    
    Args:
        query: The query to extract the data.

    Returns:
        Pandas' dataframe.
    """
    settings = load_settings()

    # create the connection string
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"

    # create connection engine
    engine = create_engine(connection_string)

    with engine.connect() as conn, conn.begin():
        df_crm = pd.read_sql(query, conn)

    return df_crm

@pa.check_input(ProductSchema, lazy=True)
@pa.check_output(ProductSchemaKPI, lazy=True)
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms DataFrame data by applying calculations and normalizations.

    Args:
        df: Pandas' DataFrame with original data.

    Returns:
        Pandas' DataFrame after transformations.
    """
    # Calcular valor_total_estoque
    df['stock_total_price'] = df['quantity'] * df['price']
    
    # Normalizar categoria para maiúsculas
    df['normalized_category'] = df['category'].str.upper()
    
    # Determinar disponibilidade (True se quantidade > 0)
    df['availability'] = df['quantity'] > 0
    
    return df

import duckdb

@pa.check_input(ProductSchemaKPI, lazy=True)
def load_to_duckdb(df: pd.DataFrame, table_name: str, db_file: str = 'my_duckdb.db'):
    """
    Load the DataFrame to DuckDB, creating or replacing the specified table.

    Args:
        df: Pandas' DataFrame to be loaded into DuckDB.
        table_name: Duckdb tablename where the data will be inserted
        db_file: DuckDB file. 
    """

    # connect o duckdb. File will be created if it doesn't exist
    con = duckdb.connect(database=db_file, read_only=False)

    # register the dataframe as a temporary table
    con.register('df_temp', df)

    # uses SQL to insert data from temp table to a permanent one
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df_temp")

    # close the connection
    con.close()

if __name__ == "__main__":

    query = "SELECT * FROM products_bronze"
    df_crm = extract_from_db(query=query)

    df_crm_kpi = transform(df_crm)
    load_to_duckdb(df=df_crm_kpi, table_name="kpi_table")

    #print(df_crm)
    #print(df_crm_kpi)