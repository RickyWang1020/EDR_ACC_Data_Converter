"""
Function: the tkinter functions for window display
Author: Xinran Wang
Date: 08/11/2020
"""

import os
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename
from function import *

class_root = None
choice = None
choice_name = None
parsed_tc = None

class Test_Case(Frame):
    def __init__(self, root, name, status):
        Frame.__init__(self, root)
        self.root = root
        self.name = name
        self.status = status
        self.selected = [BooleanVar() for k in range(len(self.name))]

        self.sb = Scrollbar(self, orient="vertical")
        self.text = Text(self, width=20, height=10, yscrollcommand=self.sb.set)
        self.sb.config(command=self.text.yview)
        self.sb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)


    def generate_checkbox(self):
        for i in range(len(self.name)):
            if self.status[i]:
                cb = Checkbutton(self, text=self.name[i], variable=self.selected[i], fg="green")
            else:
                cb = Checkbutton(self, text=self.name[i], variable=self.selected[i], fg="red")
            self.text.window_create("end", window=cb)
            self.text.insert("end", "\n")
        self.grid(row=3, padx=10, pady=5, sticky=W)

        Button(self.root, text="Select Failed (" + str(self.get_failed_count()) + ")", command=lambda: self.check_fail()).grid(row=3, column=1, padx=10, pady=10, sticky=N+W)
        Button(self.root, text="Select Passed (" + str(self.get_passed_count()) + ")", command=lambda: self.check_pass()).grid(row=3, column=1, padx=10, pady=52, sticky=N+W)
        Button(self.root, text="Select All", command=lambda: self.check_all()).grid(row=3, column=1, padx=10, pady=52, sticky=S+W)
        Button(self.root, text="Deselect All", command=lambda: self.uncheck_all()).grid(row=3, column=1, padx=10, pady=10, sticky=S+W)

    def get_selected(self):
        lst = [v.get() for v in self.selected]
        selected_names = [self.name[idx] for idx in range(len(self.name)) if lst[idx]]
        return lst, selected_names

    def get_passed_count(self):
        return len([x for x in self.status if x])

    def get_failed_count(self):
        return len([x for x in self.status if (not x)])

    def check_all(self):
        for item in self.selected:
            item.set(True)

    def uncheck_all(self):
        for item in self.selected:
            item.set(False)

    def check_pass(self):
        for item in self.selected:
            item.set(False)
        for idx, item in enumerate(self.status):
            if item:
                self.selected[idx].set(True)

    def check_fail(self):
        for item in self.selected:
            item.set(False)
        for idx, item in enumerate(self.status):
            if not item:
                self.selected[idx].set(True)


# the location of .xml file
def select_file_path(root, tk_file_loc_var, initial_directory=os.getcwd()):
    """
    Let the user select the path of .xml file
    :param tk_file_loc_var: the variable that records the path selected
    :param initial_directory: the initial directory that will be shown on the selection window
    :return: None
    """
    global class_root, parsed_tc
    try:
        selected_path = askopenfilename(initialdir=initial_directory, filetypes=[('XML Files', '*.xml'), ('All files', '*')])
        tk_file_loc_var.set(selected_path)
    except:
        print("[Error] Directories cannot be empty. Try Again!")

    parsed_tc = parse_test_cases(open_xml(selected_path))

    testcases_name = []
    testcases_status = []
    for r in parsed_tc:
        name = get_name(r)
        # True means passed and False means failed
        status = check_status(r)
        testcases_name.append(name)
        testcases_status.append(status)

    class_root = Test_Case(root, testcases_name, testcases_status)
    class_root.generate_checkbox()

# the target directory
def select_dir(tk_temp_dir_var, initial_directory=os.getcwd()):
    """
    Let the user select the path of target directory
    :param tk_temp_dir_var: the variable that records the path selected
    :param initial_directory: the initial directory that will be shown on the selection window
    :return: None
    """
    try:
        selected_dir = askdirectory(initialdir=initial_directory)
        tk_temp_dir_var.set(selected_dir)
    except:
        print("[Error] Directories cannot be empty. Try Again!")

def onclick(root):
    global choice, choice_name
    choice, choice_name = class_root.get_selected()
    root.quit()

def get_paths():
    """
    Show the path selection window and store the selected paths in variables
    :return: a tuple containing strings of data file location and target folder location
    """
    root = Tk()

    tk_file_loc = StringVar()
    tk_target_dir = StringVar()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width - 450) / 2)
    y = int((screen_height - 450) / 2)

    root.title("Source Data and Target Directory")
    root.geometry("%sx%s+%s+%s" % (450, 450, x, y))

    Label(root, text="Please select the data file you want to process (.xml): ").grid(row=0, padx=10, pady=5, sticky=W)
    e = Entry(root, textvariable=tk_file_loc)
    e.grid(row=1, column=0, padx=10, sticky=W+E)
    Button(root, text="Browse Computer", command=lambda: select_file_path(root, tk_file_loc)).grid(row=1, column=1, padx=10, pady=10, sticky=E)

    Label(root, text="Please select the test case you want to convert (Red-Fail; Green-Pass): ").grid(row=2, columnspan=5, padx=10, pady=5, sticky=W)
    Text(root, width=20, height=10).grid(row=3, padx=10, pady=5, sticky=W)

    Label(root, text="Please assign the directory to put the processed data: ").grid(row=4, columnspan=5, padx=10, pady=5, sticky=W)
    Label(root, fg="red", text="The Default Directory is the Current Project Folder!").grid(row=5, columnspan=5, padx=10, sticky=W)
    Entry(root, textvariable=tk_target_dir).grid(row=6, column=0, padx=10, sticky=W+E)
    Button(root, text="Browse Computer", command=lambda: select_dir(tk_target_dir)).grid(row=6, column=1, padx=10, pady=10)
    Button(root, text="Confirm and Start", command=lambda: onclick(root)).grid(row=7, columnspan=5, padx=10, pady=10, sticky=W+E)
    root.mainloop()

    file_loc_str = tk_file_loc.get()
    file_loc_str = file_loc_str.replace("/", "\\")

    target_dir_str = tk_target_dir.get()
    target_dir_str = target_dir_str.replace("/", "\\")

    try:
        opened = bool(root.winfo_viewable())
        root.destroy()
    except:
        return None

    return file_loc_str, target_dir_str, choice, choice_name, parsed_tc

# if __name__ == "__main__":
#     print(get_paths())