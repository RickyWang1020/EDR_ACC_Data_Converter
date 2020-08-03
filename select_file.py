from tkinter import *
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory, askopenfilename
import threading
import time

# the location of .xml file
def select_path(tk_file_loc_var):
    selected_path = askopenfilename(initialdir="C:\\Users\\", filetypes=[('XML Files', '*.xml'),('All files', '*')])
    tk_file_loc_var.set(selected_path)

# the directory of .xlsx template
def select_dir(tk_temp_dir_var):
    selected_dir = askdirectory(initialdir="C:\\Users\\")
    tk_temp_dir_var.set(selected_dir)


def get_paths():
    root = Tk()

    tk_file_loc = StringVar()
    tk_temp_dir = StringVar()

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    x = int((screenWidth - 700) / 2)
    y = int((screenHeight - 200) / 2)

    root.title("Source Data Location and Template's Directory")
    root.geometry("%sx%s+%s+%s" % (700, 200, x, y))

    Label(root, text="Please select the data file you want to process (.xml): ").grid(row=0, padx=10, pady=5, sticky=W)
    Entry(root, textvariable=tk_file_loc).grid(row=1, column=0, padx=10, sticky=W+E)
    Button(root, text="Browse Computer", command=lambda: select_path(tk_file_loc)).grid(row=1, column=1, padx=10, pady=10)

    Label(root, text="Please assign the directory to put the processed data (must include a Template.xlsx file):").grid(row=2, padx=10, pady=5, sticky=W)
    Entry(root, textvariable=tk_temp_dir).grid(row=3, column=0, padx=10, sticky=W+E)
    Button(root, text="Browse Computer", command=lambda: select_dir(tk_temp_dir)).grid(row=3, column=1, padx=10, pady=10)
    Button(root, text="Confirm and Start", command=root.quit).grid(row=5, columnspan=2, padx=10, pady=10, sticky=W+E)
    root.mainloop()

    file_loc_str = tk_file_loc.get()
    file_loc_str = file_loc_str.replace("/", "\\")

    temp_dir_str = tk_temp_dir.get()
    temp_dir_str = temp_dir_str.replace("/", "\\")
    try:
        root.destroy()
    except:
        pass

    return file_loc_str, temp_dir_str
