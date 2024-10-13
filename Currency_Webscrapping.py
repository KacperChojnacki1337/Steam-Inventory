import requests
import pandas as pd
import datetime

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
    df = pd.DataFrame(rates, columns=['Date', 'Rate'])
    df
    df['Date'] = pd.to_datetime(df['Date'])
    return df    

# Calling the function for the US dollar in the given period
endDay= datetime.date.today().strftime("%Y-%m-%d")

df_usd = get_nbp_data("USD", "2024-01-01", endDay)

# Wyświetlenie DataFrame
print(df_usd)   
