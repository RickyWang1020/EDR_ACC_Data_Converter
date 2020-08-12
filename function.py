"""
Function: pre-processing of .xml file and creating pandas dataframe for each test cases' data
Author: Xinran Wang
Date: 08/11/2020
"""

from bs4 import BeautifulSoup as bs
import pandas as pd
import yaml


# xml file pre-processing
def open_xml(path):
    """
    Open and pre-process the original .xml file
    :param path: the absolute path of the .xml file
    :return: a BeautifulSoup object that stores the whole text of .xml file
    """
    with open(path, "r") as file:
        content = file.readlines()
        content = "".join(content)
        content = content.replace("<BR>", "")
        content = content.replace("</BR>", "")
        bs_content = bs(content, "lxml")
    return bs_content

def parse_test_cases(bs_file):
    """
    Parse the .xml texts by test cases
    :param bs_file: the BeautifulSoup object containing the whole text of .xml file (the output of open_xml)
    :return: a list containing every test case's .xml text as separate elements
    """
    return bs_file.find_all("testcase")

def get_all_results(testcases):
    """
    Generate the test results for every test cases from the raw data
    :param testcases: a list containing every test case's .xml text as separate elements (the output of parse_test_cases)
    :return: a list containing several lists, each list storing several strings representing the raw results
    """
    all_results = []

    for tc in testcases:
        test_result = tc.find_all("command")
        codes = []
        for r in test_result:
            try:
                x = r.find("commname").text.strip().startswith("protocols")
                if x:
                    code = r.find_all("answer")
                    if code:
                        codes.append(code[-1].text.strip()[1:-1])
            except:
                pass
        all_results.append(codes)
    return all_results

def get_name(tc_code):
    """
    Get the names of testcases
    :param tc_code: a list containing every test case's .xml text as separate elements (the output of parse_test_cases)
    :return: a list containing all test case names
    """
    header_block = tc_code.find_all("header")[0]
    name = header_block.find("tcnameunique").text
    return name

def check_status(tc_code):
    """
    Get the pass/fail status of each testcase
    :param tc_code: a list containing every test case's .xml text as separate elements (the output of parse_test_cases)
    :return: a list containing all test case's pass or fail status
    """
    status_val = tc_code.find_all("status")
    for s in status_val:
        result = str(s["value"])
        if result == "fail":
            return False
    return True

def generate_single_testcase(result_code):
    """
    For each test case's raw data, split the data into data type name and data results
    :param result_code: a list containing several strings representing the raw results
    :return: a tuple of two lists, one list contains the name of data type, another list contains the corresponding data list of every data type name
    """
    name_list = []
    data_list = []
    visited = {}

    for c in result_code:
        lst = c.split(', ')
        name = "".join([x[2:] for x in lst[1:3]])
        data = lst[3:]
        if name not in visited:
            visited[name] = 0
        else:
            visited[name] += 1
        if visited[name] == 0:
            name_list.append(name)
        else:
            name_list.append(name + "_" + str(visited[name]))
        data_list.append(data)

    return name_list, data_list


def combine_every_two_rows(to_combine):
    """
    For ACC data, need to combine every two rows of data into one row
    :param to_combine: a list containing the EDR data need to be combined
    :return: a list
    """
    to_return = []
    for m in range(0, len(to_combine), 2):
        current_element, next_element = to_combine[m], to_combine[m+1]
        to_return.append(current_element[2:] + next_element[2:])
    return to_return


def generate_dataframe(name_lst, data_lst, wanted_FA = ["FA13", "FA14", "FA15"], wanted_B0 = ["B032", "B033", "B034", "B035", "B036", "B037", "B042", "B043", "B052", "B053"]):
    """
    From the name and data list of one test case, pick out the data we want and put them in dataframes
    :param name_lst: the list containing all the names of data types
    :param data_lst: the list containing the corresponding data of every data type
    :param wanted_FA: the EDR data type name we want (has default values, subject to changes)
    :param wanted_B0: the ACC data type name we want (has default values, subject to changes)
    :return: a tuple of two dataframes, one is EDR dataframe and another is ACC dataframe
    """
    to_add_FA = {}
    to_add_B0 = {}

    # to keep the patterns of the original data, avoid being shuffled by dictionary
    to_add_FA_names = []
    to_add_B0_names = []

    for i in range(len(name_lst)):
        name = name_lst[i]
        data = data_lst[i]

        if name[:4] in wanted_B0:
            to_add_B0[name] = combine_every_two_rows(data)
            to_add_B0_names.append(name)
        elif name[:4] in wanted_FA:
            to_add_FA[name] = data
            to_add_FA_names.append(name)

    FA_df = pd.DataFrame(to_add_FA)
    B0_df = pd.DataFrame(to_add_B0)

    FA_df = FA_df[to_add_FA_names]
    B0_df = B0_df[to_add_B0_names]

    return FA_df, B0_df

def read_config(file_path):
    """
    Read the config file and generate the information from that
    :param file_path: the path where the yaml config file locates
    :return: a dictionary containing the information in the yaml file
    """
    with open(file_path, "r", encoding='utf-8') as y_file:
        config_file = yaml.load(y_file, Loader=yaml.FullLoader)
    return config_file

# if __name__ == "__main__":
#     path = "R:\\Electronics Project\PSE\\PSE_System_Test\\Personal Folder\\Wang Xinran\\EDR_ACC_Data_Convert_Tool\\sc004_Deployment_AS22_R300.xml"
#     cases = parse_test_cases(open_xml(path))
#     c = cases[37]
#     name = get_name(c)
#     status = check_status(c)
#     testcase_class = TestCase(c, name, status)
#     print(testcase_class.name, testcase_class.status)
#     testcase_class.update_name_and_data()
#     print(testcase_class.name_l)
#     print(testcase_class.data_l)
#     print(c)



