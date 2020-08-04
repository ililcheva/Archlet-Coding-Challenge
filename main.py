# HOW TO RUN: python3 main.py --outliers --currency FILEPATH

"""
Simple command line tool to run the Archlet Data Processing Challenge
"""

import argparse
import os

import pandas as pd
import numpy as np
import re
import requests
import json


from data_preprocessor import DataPreprocessor
from outlier_detector import OutlierDetector
from currency_converter import CurrencyConverter

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='CLI for Archlet Data Processing Challenge')

    parser.add_argument('file_path', help="File path to the data sheet to be processed")

    parser.add_argument('--outliers', help="Flag for outlier detection", action='store_true')
    parser.add_argument('--currency', help="Flag for currency conversion", action='store_true')

    args = parser.parse_args()

    # Data Cleaning
    DP = DataPreprocessor(args.file_path)

    ''' Remove repeated substrings in columns -> (column, substring_to_be_removed) '''
    DP.remove_repeated_substrings('Plant','Plant')
    DP.remove_repeated_substrings('Bidding Round','Offering')
    DP.remove_repeated_substrings('Product Group','Group')

    ''' Remove columns that are product of already existing ones and invalid columns '''
    DP.clean_columns(['Product Name','Total Cost'])

    ''' Utility function to normalize Group Name column records (UPPER -> Capitalized) '''
    DP.normalize_product_groups_names()

    ''' Convert columns of choice to numeric type '''
    DP.convert_columns_to_numeric(['Material Cost','Blending Cost','Production Cost','Transportation Cost','Duty Cost'])
    
    ''' Handle missing values in numeric columns by substituting NaN values with 0 '''
    DP.fill_missing_values(['Material Cost','Blending Cost','Production Cost','Transportation Cost','Duty Cost'], 0)
    
    ''' Optional: Method to add removed relevant columns from clean_methods func '''
    DP.add_product_name()
    DP.add_total_cost(['Material Cost','Blending Cost','Production Cost','Transportation Cost','Duty Cost'])
    
    ''' Saves cleaned data in a new Excel sheet '''
    with pd.ExcelWriter('cleaned.xlsx') as writer:  
        DP.get_df().to_excel(writer, sheet_name='Clean Data')
    print('Preprocessed data excel spreadsheet created: cleaned.xlsx!')

    # Currency Conversion
    if args.currency:
        ''' Currency conversion to USD, but if second argument is added to the constructor below, it converts to any other currency'''
        CC = CurrencyConverter(DP.get_df())
        ''' Converts all columns of type float64 to the specified currency above '''
        CC.convert_all('float64')
        
        ''' Save converted data in a new Excel sheet '''
        with pd.ExcelWriter('converted.xlsx') as writer:  
            DP.get_df().to_excel(writer, sheet_name='Converted Currency To {}'.format(CC.get_currency()))
        print('Currency conversion excel spreadsheet created: converted.xlsx!')

    # Outlier Detection
    if args.outliers:
        DO = OutlierDetector(DP.get_df())
        
        ''' Computes Tukey outlier upper/lower inner/outer ranges '''
        DO.compute_ranges(['Material Cost', 'Blending Cost', 'Production Cost', 'Transportation Cost', 'Duty Cost','Total Cost'])
        
        ''' 
            Adds a style to the dataframe which has the outlier cells coloured in 4 different colours, 
            depending on the range the outlier falls in
        '''
        outliers_df = DP.get_df().style.apply(DO.highlight_outlier_cells, axis=None)
        
        ''' Save outlier data in a new Excel sheet '''
        with pd.ExcelWriter('outliers.xlsx') as writer:  
            outliers_df.to_excel(writer, sheet_name='Detected Outliers')
        print('Outlier detection excel spreadsheet created: outliers.xlsx!')
    

    print('Finished')
