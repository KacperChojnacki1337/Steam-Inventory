import requests
import pandas as pd
import datetime
import psycopg2
from sqlalchemy import create_engine
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def get_nbp_data(currency, start_date, end_date):
    """
    Downloads currency exchange rate data from the NBP API and creates a DataFrame.
    """

    url = f"https://api.nbp.pl/api/exchangerates/rates/A/{currency}/{start_date}/{end_date}/"
    response = requests.get(url)
    data = response.json()

    # Preparing data for DataFrame
    rates = []
    for rate in data['rates']:
        rates.append([rate['effectiveDate'], rate['mid']])

    # Creating DataFrame
    df = pd.DataFrame(rates, columns=['date', 'rate'])
    df['date'] = pd.to_datetime(df['date'])
    return df    

# Calling the function for the US dollar in the given period
endDay= datetime.date.today().strftime("%Y-%m-%d")

df_usd = get_nbp_data("USD", "2024-01-01", endDay)

 
def insert_data_to_postgresql(dataframe):
    #connection
    db_host = "localhost"
    db_port = 5432
    db_name = "steam_inventory"
    db_user = "postgres"
    db_password = "Siadajkurduplu96!sql"
    # Database connection parameters (replace with your credentials)
    try:
        conn1 = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
        print("Połączono z bazą danych")
    except psycopg2.Error as e:
        print("Błąd połączenia z bazą danych:", e)
        return None
    
    cursor = conn1.cursor()
    conn1.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    currency_df = dataframe
    print(currency_df)
    cursor.execute('SELECT current_database()')
    cursor.fetchall()
    
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'currency_table');")
    table_exists = cursor.fetchone()[0]

    if table_exists:
        # Truncate the table to clear existing data
        cursor.execute("TRUNCATE TABLE currency_table;")
        print("Istniejąca tabela 'currency_table' została wyczyszczona.")
    else:
        # Create the table with column names inferred from DataFrame headers
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS currency_table (
            id SERIAL PRIMARY KEY,
            date DATE,
            rate NUMERIC
            );
            """)
        print("Utworzono nową tabelę 'currency_table'.")
    engine = create_engine('postgresql+psycopg2://postgres:Siadajkurduplu96!sql@localhost/steam_inventory')
    #append
    currency_df.to_sql('currency_table',engine,if_exists='append', index=False)
    conn1.close()
insert_data_to_postgresql(df_usd)

