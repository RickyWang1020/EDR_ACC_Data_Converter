from select_file import *
from progressbar import *
from excel import *
from copy_acc_edr import *
import frozen_dir

SETUP_DIR = frozen_dir.app_path()
sys.path.append(SETUP_DIR)

# progress bar operation
total_len = 1000000000
widgets = ['Progress: ', Percentage(), ' ', Bar('>'), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
pbar = ProgressBar(widgets=widgets, maxval=total_len, redirect_stdout=True)

# read the config file
#conf = read_config(os.path.join(SETUP_DIR, "config", "var_conf.yaml"))
conf = read_config("var_conf.yaml")

coeff_dic = conf["coefficient"]
name_to_description = conf["name_to_description"]

#temp_path = os.path.join(SETUP_DIR, "template", "Template.xlsx")
temp_path = "Template.xlsx"


while True:
    try:
        file_path, output_path, to_convert, tc_names, parsed = get_paths()
        #print(file_path, output_path, to_convert, tc_names, parsed)

        results = get_all_results(parsed)

        unit = total_len / len(tc_names)
        need_index = 0

        pbar.start()
        update_pbar(pbar, 0)

        data_name = file_path.split("\\")[-1].replace(".xml", "")
        folder_path = create_folder(output_path, data_name)

        for i in range(len(results)):
            if to_convert[i]:
                result = results[i]
                print("Processing:", tc_names[need_index])
                n, d = generate_single_testcase(result)
                fa_dataframe, b0_dataframe = generate_dataframe(n, d)
                file_name = create_excel(folder_path, tc_names[need_index])
                fa_col = list(fa_dataframe.columns)
                b0_col = list(b0_dataframe.columns)
                if fa_col:
                    process_edr_data(temp_path, folder_path, file_name, fa_col, pbar, unit * need_index, unit / 3)
                    update_pbar(pbar, unit * need_index + unit / 3)
                if b0_col:
                    process_acc_data(temp_path, folder_path, file_name, b0_col, coeff_dic, name_to_description, pbar, unit * need_index + unit / 3, unit / 3)
                    update_pbar(pbar, unit * need_index + unit * 2 / 3)
                fill_excel_for_one_testcase(folder_path, fa_dataframe, b0_dataframe, file_name)
                update_pbar(pbar, unit * (need_index + 1))
                need_index += 1
        pbar.finish()

        print("Finished!\nGenerated", need_index, "test case files in", folder_path)
        input("Press Enter to exit...")

    except UnicodeDecodeError:
        print("[Error] Wrong file format. Check Again!")
    except FileNotFoundError:
        print("[Error] Directories cannot be empty. Check Again!")
    except ZeroDivisionError:
        print("[Error] You selected 0 test case! Check Again!")
    except TypeError:
        break
    else:
        break

