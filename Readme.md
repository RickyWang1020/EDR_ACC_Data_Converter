# EDR_ACC_Data_Converter

## About This Program
This is a simple program to convert the raw EDR and ACC test data in .xml form into .xlsx files, with calculation functions and Excel Template pre-set and subject to change.

This program has been tested on PyCharm for Windows10.

## Program Requirements
- Python 3.5 +
- openpyxl (https://pypi.org/project/openpyxl/)
- BeautifulSoup4 (https://pypi.org/project/beautifulsoup4/)
- lxml (https://pypi.org/project/lxml/)
- pandas (https://pypi.org/project/pandas2/)
- progressbar (https://pypi.org/project/progressbar2/)
- yaml (https://pypi.org/project/yaml-1.3/)
- tkinter

## 

## How to Use


## Some Parameters Subject to Change
In *var_conf.yaml*:

- **coeff**: a **dictionary** storing the default coefficients for generating the formulas of calculating different types of ACC data in Excel;

    The dictionary's keys are the data types' names, and the dictionary's values represent the corresponding coefficient when generating the calculation formula in Excel.
        
- **name_to_description**: a **dictionary** storing the descriptions of different data types that will be shown on the Excel columns;
        
    The dictionary's keys are the data types' names, and its values are the description texts of the corresponding data type.
        
You can add, delete or refine the key-value pairs in these dictionaries if the coefficients for calculation or data types' descriptions have been changed.
