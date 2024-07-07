import pandas as pd
import sqlite3

# File names and corresponding table names
files_and_tables = {
    'Module Administration & handy tools.csv': 'AdministrationHandyTools',
    'Module Cooperation tools.csv': 'CooperationTools',
    'Module Finance tools.csv': 'FinanceTools',
    'Module Integrations.csv': 'Integrations',
    'Module Projects and remote work.csv': 'ProjectsRemoteWork',
    'Module Recruitment and HR tools.csv': 'RecruitmentHRTools',
    'Pricing of packages.csv': 'PricingPackages'
}

# Connect to SQLite database (or create it)
conn = sqlite3.connect('data/firmbee_offering.db')
cursor = conn.cursor()


# Function to clean column names
def clean_columns(df):
    df.columns = df.columns.str.strip()
    return df


# Function to create a table and insert data
def create_table_and_insert_data(df, table_name):
    df = clean_columns(df)
    df = df.set_index(df.columns[0]).T.reset_index()
    df.rename(columns={'index': 'package_name'}, inplace=True)

    # Create table SQL
    columns = ', '.join([f'"{col}" TEXT' for col in df.columns])
    create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns});'
    cursor.execute(create_table_sql)

    # Insert data SQL
    placeholders = ', '.join(['?' for _ in df.columns])
    insert_sql = f'INSERT INTO {table_name} VALUES ({placeholders});'

    for index, row in df.iterrows():
        cursor.execute(insert_sql, tuple(row))


# Process each file
for file_name, table_name in files_and_tables.items():
    df = pd.read_csv(f'data/{file_name}')
    create_table_and_insert_data(df, table_name)

# Commit changes and close the connection
conn.commit()
conn.close()
