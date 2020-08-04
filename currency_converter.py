
import pandas as pd
import requests
import json

"""
    Currency Conversion Pipeline
"""

class CurrencyConverter:
    
        
    '''
        Set main dataframe, main currency and store real time conversion rates
    '''
    def __init__(self, df, currency='USD'):
        self._df = df
        self._main_currency = currency
        self._currency_rates = {}
        self.store_rates()


    '''
        Currency Getter
    '''
    def get_currency(self):
        return self._main_currency
    
    '''
        Get current currency conversion rates for a currency of choice
    '''
    def get_rates_from_api(self, to_currency):
        query = 'https://api.exchangeratesapi.io/latest?base={}'.format(to_currency)
        response = requests.get(
            query,
            headers = {'Content-Type':'application/json'}
        )
        
        response_body = response.json()
        
        return response_body['rates']
    
    '''
        Helper method to store all unique currencies' rates found in excel spreadsheet for conversion to the main one
    '''
    def store_rates(self):
        currencies = self._df['Currency'].unique()
        for currency in currencies:
            self._currency_rates[currency] = self.get_rates_from_api(currency)[self._main_currency]

    '''
        Convert all records of a currency in the main dataframe, convert all desired price values to main currency
    '''
    def convert_to_currency(self, from_currency, rate, columns):
        for column in columns:
            self._df.loc[self._df['Currency'] == from_currency, column] = self._df.loc[self._df['Currency'] == from_currency][column].apply(lambda x: x * rate)
    
    '''
        Function to automatically convert all desired columns to main currency
        and edit the Currency column to show the current price currency
    '''       
    def convert_all(self, column_type):
        columns = self._df.select_dtypes(include=[column_type]).columns.to_list()
        for currency, rate in self._currency_rates.items():
            self.convert_to_currency(currency, rate, columns)
        self._df['Currency'] = self._main_currency
        