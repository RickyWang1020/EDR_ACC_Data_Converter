"""
Function: pre-processing of .xml file and creating pandas dataframe for each test cases' data
Author: Xinran Wang
Date: 08/03/2020
"""

from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import yaml

# xml file pre-processing
def open_xml(path):
    """
    Open and preprocess the original .xml file
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

def generate_single_testcase_dic(result_code):
    """
    For each test case's raw data, split the data into data type name and data results
    :param result_code: a list containing several strings representing the raw results
    :return: a dictionary, the keys are the name of data type, the values are the lists of data results
    """
    dic = {}

    for c in result_code:
        lst = c.split(', ')
        key = "".join([x[2:] for x in lst[1:3]])
        val = lst[3:]
        if key not in dic:
            dic[key] = []
        if val not in dic[key]:
            dic[key].append(val)
    return dic

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


def generate_dataframe(dictionary, wanted_FA = ["FA13", "FA14", "FA15"], wanted_B0 = ["B032", "B033", "B034", "B035", "B036", "B037", "B042", "B043", "B052", "B053"]):
    """
    From the all-data dictionary of one test case, pick out the data we want and put them in dataframes
    :param dictionary: a dictionary (the output of generate_single_testcase_dic)
    :param wanted_FA: the EDR data type name we want (has default values, subject to changes)
    :param wanted_B0: the ACC data type name we want (has default values, subject to changes)
    :return: a tuple of two dataframes, one is EDR dataframe and another is ACC dataframe
    """
    to_add_FA = {}
    to_add_B0 = {}

    for k in dictionary.keys():
        if k in wanted_FA:
            length_val = len(dictionary[k])
            if length_val > 1:
                for iterator in range(length_val):
                    name = k + "_" + str(iterator + 1)
                    to_add_FA[name] = dictionary[k][iterator]
            else:
                to_add_FA[k] = dictionary[k][0]

        elif k in wanted_B0:
            length_val = len(dictionary[k])
            if length_val > 1:
                for iterator in range(length_val):
                    name = k + "_" + str(iterator + 1)
                    combined_list = combine_every_two_rows(dictionary[k][iterator])
                    to_add_B0[name] = combined_list
                    # to_add_B0[name + "_converted"] = calculate_combined(combined_list, k)
            else:
                combined_list = combine_every_two_rows(dictionary[k][0])
                to_add_B0[k] = combined_list
                # to_add_B0[k + "_converted"] = calculate_combined(combined_list, k)

    FA_df = pd.DataFrame(to_add_FA)
    B0_df = pd.DataFrame(to_add_B0)

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

def update_pbar(progress_bar, progress):
    """
    Updating the progressbar object
    :param progress_bar: the prograssbar object
    :param progress: a number representing the current progress
    :return: None
    """
    progress_bar.update(progress)
    time.sleep(0.01)
