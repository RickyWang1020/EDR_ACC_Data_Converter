"""
Function: the tkinter functions for window display
Author: Xinran Wang
Date: 08/05/2020
"""

import os
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename

# the location of .xml file
def select_file_path(tk_file_loc_var, initial_directory=os.getcwd()):
    """
    Let the user select the path of .xml file
    :param tk_file_loc_var: the variable that records the path selected
    :param initial_directory: the initial directory that will be shown on the selection window
    :return: None
    """
    selected_path = askopenfilename(initialdir=initial_directory, filetypes=[('XML Files', '*.xml'),('All files', '*')])
    tk_file_loc_var.set(selected_path)

# # the location of .xlsx template
# def select_temp_path(tk_file_loc_var, initial_directory=os.getcwd()):
#     """
#     Let the user select the path of .xlsx template file
#     :param tk_file_loc_var: the variable that records the path selected
#     :param initial_directory: the initial directory that will be shown on the selection window
#     :return: None
#     """
#     selected_path = askopenfilename(initialdir=initial_directory, filetypes=[('Excel Files', '*.xlsx'), ('All files', '*')])
#     tk_file_loc_var.set(selected_path)

# the target directory
def select_dir(tk_temp_dir_var, initial_directory=os.getcwd()):
    """
    Let the user select the path of target directory
    :param tk_temp_dir_var: the variable that records the path selected
    :param initial_directory: the initial directory that will be shown on the selection window
    :return: None
    """
    selected_dir = askdirectory(initialdir=initial_directory)
    tk_temp_dir_var.set(selected_dir)


def get_paths():
    """
    Show the path selection window and store the selected paths in variables
    :return: a tuple containing strings of data file location and target folder location
    """
    root = Tk()

    tk_file_loc = StringVar()
    # tk_temp_loc = StringVar()
    tk_target_dir = StringVar()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width - 450) / 2)
    y = int((screen_height - 250) / 2)

    root.title("Source Data Location, Template Location and Target Directory")
    root.geometry("%sx%s+%s+%s" % (450, 250, x, y))

    Label(root, text="Please select the data file you want to process (.xml): ").grid(row=0, padx=10, pady=5, sticky=W)
    Entry(root, textvariable=tk_file_loc).grid(row=1, column=0, padx=10, sticky=W+E)
    Button(root, text="Browse Computer", command=lambda: select_file_path(tk_file_loc)).grid(row=1, column=1, padx=10, pady=10, sticky=E)

    # Label(root, text="Please select the Template Excel location (.xlsx): ").grid(row=2, padx=10, pady=5, sticky=W)
    # Entry(root, textvariable=tk_temp_loc).grid(row=3, column=0, padx=10, sticky=W+E)
    # Button(root, text="Browse Computer", command=lambda: select_temp_path(tk_temp_loc)).grid(row=3, column=1, padx=10, pady=10, sticky=E)

    Label(root, text="Please assign the directory to put the processed data: ").grid(row=2, padx=10, pady=0, sticky=W)
    Label(root, fg="red", text="The Default Directory is the Current Project Folder!").grid(row=3, padx=10, pady=5, sticky=W)
    Entry(root, textvariable=tk_target_dir).grid(row=4, column=0, padx=10, sticky=W+E)
    Button(root, text="Browse Computer", command=lambda: select_dir(tk_target_dir)).grid(row=4, column=1, padx=10, pady=10)
    Button(root, text="Confirm and Start", command=root.quit).grid(row=6, columnspan=5, padx=10, pady=10, sticky=W+E)
    root.mainloop()

    file_loc_str = tk_file_loc.get()
    file_loc_str = file_loc_str.replace("/", "\\")

    # temp_loc_str = tk_temp_loc.get()
    # temp_loc_str = temp_loc_str.replace("/", "\\")

    target_dir_str = tk_target_dir.get()
    target_dir_str = target_dir_str.replace("/", "\\")

    try:
        opened = bool(root.winfo_viewable())
        root.destroy()
    except:
        return None

    return file_loc_str, target_dir_str
