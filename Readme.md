# EDR_ACC_Data_Converter

## About This Program
This program automatically converts the raw EDR and ACC test data in .xml form into Excel .xlsx files, with calculation functions and Excel Template pre-set and subject to change.

This program has been tested on PyCharm and IDLE for Windows10.

## Program Requirements
- Python 3.5 + (**must be installed beforehand**)
- openpyxl
- BeautifulSoup4
- lxml
- pandas
- progressbar
- yaml
- tkinter

## Download Required Modules
(1) Download and unzip the whole project folder

(2) Open **cmd** and change directory to the location of the project folder:
    
    cd /yourpath/EDR_ACC_Data_Converter

(3) Run the command below to install the required Python modules:
   
    pip install -r modules_to_import/requirements.txt

## Run the Program
Run `main.py`, assign the directories for source data (.xml), template excel (.xlsx), and the target folder for putting the processed excel files in the tkinter window, and wait until the progressbar reaches 100%.

## Some Parameters Subject to Change
In `var_conf.yaml`:

- *coeff*: a **dictionary** storing the default coefficients for generating the formulas of calculating different types of ACC data in Excel;

    The dictionary's keys are the data types' names, and the dictionary's values represent the corresponding coefficient when generating the calculation formula in Excel.
        
- *name_to_description*: a **dictionary** storing the descriptions of different data types that will be shown on the Excel columns;
        
    The dictionary's keys are the data types' names, and its values are the description texts of the corresponding data type.
        
You can add, delete or refine the key-value pairs in these dictionaries if the coefficients for calculation or data types' descriptions have been changed.

## Project Structure
```
EDR_ACC_Data_Converter/
├── modules_to_import/                               # modules to download and import for this program
│   ├── beautifulsoup4-4.9.1-py3-none-any.whl        # beautifulsoup
│   ├── lxml-4.5.2-cp37-cp37m-win_amd64.whl          # lxml
│   ├── openpyxl-3.0.4-py2.py3-none-any.whl          # openpyxl
│   ├── progressbar2-3.51.4-py2.py3-none-any.whl     # progressbar
│   ├── requirements.txt                             # use this txt to pip install
│   └── soupsieve-2.0.1-py3-none-any.whl             # soupsieve (pre-req for beautifulsoup)
├── copy_acc_edr.py                                  # copy the formats of the excel cells into the current test case's excel file
├── excel.py                                         # operations of creating excel file and filling data into excel
├── function.py                                      # pre-processing of .xml file and creating pandas dataframe for each test cases' data
├── main.py                                          # the main function to run
├── Readme.md
├── select_file.py                                   # the tkinter functions for window display
├── Template.xlsx                                    # template .xlsx file
└── var_conf.yaml                                    # configuration file for some changeable variables
```