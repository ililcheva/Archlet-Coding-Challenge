
import pandas as pd
import re

"""
    Preprocess Data Pipeline
"""
class DataPreprocessor:
    
    '''
        Construct dataframe
    '''
    def __init__(self, file_path):
        self._df = self.read_input(file_path)
    
    
    '''
        Read input excel spreadsheet
    '''
    def read_input(self, file_path):
        return pd.read_excel(file_path)
    
    
    '''
        Dataframe Getter
    '''
    def get_df(self):
        return self._df
    

    '''
        Remove buggy columns and additional user-desired columns
    '''
    def clean_columns(self, unwanted_columns=[]):
        columns = self._df.columns.values.tolist()
        regex = re.compile(r'Unnamed:')
        columns_for_removal = [buggy_column for buggy_column in columns if regex.search(buggy_column)]
        columns_for_removal = columns_for_removal + unwanted_columns
        self._df.drop(columns_for_removal, inplace=True, axis=1)
    

    '''
        Remove repeated substrings from columns
    '''
    def remove_repeated_substrings(self, column_name, substring):
        regex = re.compile(r' ?{0} ?'.format(substring))
        self._df[column_name] = self._df[column_name].str.replace(regex, "")
     
    '''
        Add Product Name column (it's a product of other columns)
    '''
    def add_product_name(self):
        self._df.insert(2, "Product Name", 0, True)
        self._df['Product Name'] = '' + self._df['Product Criticality'].apply(str) + '-' + self._df['Region'] + '-Plant ' + self._df['Plant'] + '-Group ' + self._df['Product Group']
    
    '''
        Add Total Cost column (it's a product of other columns)
    '''
    def add_total_cost(self, columns):
        self._df['Total Cost'] = self._df[columns].astype(float).sum(axis=1)


    '''
        Find only uppercase strings (like MOSCOW)
    '''
    def find_uppercase_regex(self, string):
        regex = re.compile(r'[A-Z]{2,}')
        uppercase = re.findall(regex, string)
        return uppercase

    '''
        Replace only uppercase strings with capitalized (like MOSCOW -> Moscow)
    '''
    def normalize_group_name(self, name):
        found_uppercase = self.find_uppercase_regex(name)
        
        if len(found_uppercase) == 0:
            return name
        elif len(found_uppercase) == 1:
            return name.replace(found_uppercase[0], found_uppercase[0].capitalize())
        else:
            for uppercase in found_uppercase:
                name.replace(uppercase, uppercase.capitalize())
            return name
    
    '''
        Apply the replacement of only uppercase strings with capitalized
        on the Product Group column
    '''
    def normalize_product_groups_names(self):
        self._df['Product Group'] = self._df['Product Group'].apply(self.normalize_group_name)
    

    '''
        Convert columns to numeric type
    '''
    def convert_columns_to_numeric(self, columns):
        for column in columns:
            self._df[column] = pd.to_numeric(self._df[column], errors='coerce')


    '''
        Substitute missing values with a value of choice
    '''
    def fill_missing_values(self, columns, desired_value):
        self._df[columns] = self._df[columns].fillna(value=desired_value)