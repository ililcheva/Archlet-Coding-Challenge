
import pandas as pd
import re

"""
    Outlier Detection Pipeline
"""

# Theory Reference: https://sphweb.bumc.bu.edu/otlt/mph-modules/bs/bs704_summarizingdata/bs704_summarizingdata7.html

class OutlierDetector:
    
    '''
        Set main dataframe and create empty dataframe to store Tukey fences for columns
    '''
    def __init__(self, df):
        self._df = df
        self._dfranges = pd.DataFrame({},index=['Outer Lower Fence', 'Inner Lower Fence', 'Inner Upper Fence', 'Outer Upper Fence'])
        
        
    
    '''
        Ranges Dataframe Getter
    '''
    def get_ranges(self):
        return self._dfranges
    
    
    
    '''
        Compute outling ranges for a single column according to Tukey fences theory and store them
    '''
    def compute_ranges_per_column(self, column):
        Q1 = self._df.quantile(.25)[column]
        Q3 = self._df.quantile(.75)[column]
        IQR = Q3 - Q1

        inner_lower_fence = Q1 - 1.5 * IQR
        outer_lower_fence = Q1 - 3.0 * IQR
        
        inner_upper_fence = Q3 + 1.5 * IQR
        outer_upper_fence = Q3 + 3.0 * IQR
    
        self._dfranges[column] = [outer_lower_fence, inner_lower_fence, inner_upper_fence, outer_upper_fence]
        
    
    
    '''
        Compute outling ranges ranges for all columns
    '''
    def compute_ranges(self, columns_list):
        for column in columns_list:
            self.compute_ranges_per_column(column)
    
    
    
    '''
        Define outlier cell colours based on position of value to Tukey fences
    '''
    def color_outlier(self, column):
        
        rows = []

        for value in self._df[column]:
            # darkblue background
            if value < self._dfranges[column]['Outer Lower Fence']:
                rows.append('background-color: #0066ff')
            # lightblue background
            elif value > self._dfranges[column]['Outer Lower Fence'] and value < self._dfranges[column]['Inner Lower Fence']:
                rows.append('background-color: #cce0ff')
            # lightred background
            elif value > self._dfranges[column]['Inner Upper Fence'] and value < self._dfranges[column]['Outer Upper Fence']:
                rows.append('background-color: #ffb3b3')
            # darkred background
            elif value > self._dfranges[column]['Outer Upper Fence']:
                rows.append('background-color: #cc0000')
            # no background
            else:
                rows.append('')

        return rows
    
    
    
    '''
        Apply outlier colours to the whole dataframe
    '''
    def highlight_outlier_cells(self, df, columns=['Material Cost', 'Blending Cost', 'Production Cost', 'Transportation Cost', 'Duty Cost', 'Total Cost']):

        df_containing_colours = pd.DataFrame('', index=df.index, columns=df.columns)
        for column in columns:
            df_containing_colours[column] = self.color_outlier(column)
    
        return df_containing_colours
    