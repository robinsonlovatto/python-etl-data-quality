import duckdb

def read_from_duckdb_and_print(table_name: str, db_file: str = 'my_duckdb.db'):
    """
    Read data from a DuckDB table and print thr results

    Attributess:
    - table_name: Duckdb tablename to be read
    - db_file: DuckDB file.
    """
    # Connect to DuckDB
    con = duckdb.connect(database=db_file)

    # Execute SQL
    query = f"SELECT * FROM {table_name}"
    result = con.execute(query).fetchall()

    # Close connection
    con.close()

    # Print the results
    for row in result:
        print(row)

if __name__ == "__main__":
    # Tablename to be read
    table_name = "kpi_table"
    
    # read data and print result
    read_from_duckdb_and_print(table_name)