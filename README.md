# README #

Hello, and welcome to the Archlet Data Science Coding Challenge!

## Description and Goals##

In this coding challenge the goal is to create a simple data pipeline.
The most basic version should consist of a data cleaning operation, a currency conversion operation and an outlier detection.
Feel free to implement other operations or even provide some analysis on the data to showcase your strengths regarding anything related to data science.
The goal of this task is to have a clean version of the provided data so that it can serve as the input for further operations.
For example imagine that this pipeline would be used to prepare data to input in a machine learning algorithm that might take hours to train.
Obviously, one would like that the training itself would never fail due to unexpected inputs.
Apart from the accuracy of your pipeline we will also evaluate your coding style.
Many programmers can implement awesomely complex alorithms, the crux lies however in making such code easily understandable for the rest of the team.

### Input ###
The input of the pipeline will be an excel file with one sheet.
You can assume that there is exactly one row which specifies the names of the columns in the sheet.
Other than that there are no restrictions.
We provide one example file, but be sure to make your solution general enough such that it can handle any file that follows the description above.

### Data Cleaning ###
In this step it is important to unify the data in a column.
What often happens in human-input data is that some cells contain a wrong type, are empty, have some symbol to indicate that there is no value, etc.
Concretely your solution should enforce the following two points in the output:
* all the types in one column are the same
* per type there is one way to indicate that a cell is empty
Feel free to add some assumptions if you think that it will simplify your task without compromising the data.
(Just returning a completely empty table will therefore not satisfy these constraints)

### Currency Conversion ###
The next step is to convert each column that is a price in a certain currency to US dollar.
For , if there is a column named "Currency" and EUR, CHF, GBP etc. are given as values, all prices of that specific row should be transformed to be the equivalent price in USD.
Here you have some freedom in how to implement this exactly.
For example an acceptible way is to provide a public function that takes as inputs: a table with the data, a column name and an exchange rate.
This function would then return a table with the prices of the specified column converted according to the provided exchange rate.
A slightly more advanced solution can also fetch the necessary exchange rate from a public API and use that instead of requiring a manual input.
An even more automated solution would detect columns that are most likely a price and converts these using exchange rates from public apis.

### Outlier Detection ###
Finally the outlier detection should be able to flag suspicious values in any numeric column.
This functionality should be able to produce a report with an overview of which cells are probably not correct.
The interpretation of what an outlier should be is up to you.
In the review meeting we will discuss your proposed solution.

## Output ##
Using your solution it should be possible to create a table of the same size as the input containing the updated values.
The level of automation to obtain this solution is up to you.
It is totally fine if this requires a handfull of API calls, as long as it is clear what each of these calls needs as an input and what it produces as output.

## Allowed Tools ##
Since our data science code base is in Python, the main interface should be implemented in Python.
However, if you know other languages or tools that are extremely useful for solving specific subtasks, feel free to integrate them.
Also, any package or open source library available for Python can be used. Just be sure to be able to explain what they exactly do.

## Closing Remarks ##
This task is designed to take a few hours to complete. 
It is not necessary to spend much more time than this in order to complete every task.
Instead of rushing to make sure that all the minimal functionality is there we would rather see a few well implemented tasks and clear API definitions for the remaining functionalities.
This way we will have at least a good starting point to start the review meeting.
In case you find yourself with time to spare after completing all the subtasks, feel free to improvise on next steps of data analysis.
However, in the case that you are not able to complete at least the minimal requirements, we will not go over any other solutions you provide.

Good luck and may your coding be blessed!