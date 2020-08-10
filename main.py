from function import *
from select_file import *
from progressbar import *
from excel import *
from copy_acc_edr import *
import frozen_dir

SETUP_DIR = frozen_dir.app_path()
sys.path.append(SETUP_DIR)

# progress bar operation
total_len = 1000000
widgets = ['Progress: ', Percentage(), ' ', Bar('>'), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
pbar = ProgressBar(widgets=widgets, maxval=total_len, redirect_stdout=True)

# read the config file
conf = read_config(os.path.join(SETUP_DIR, "config", "var_conf.yaml"))
coeff_dic = conf["coefficient"]
name_to_description = conf["name_to_description"]

temp_path = os.path.join(SETUP_DIR, "template", "Template.xlsx")

while True:
    try:
        file_path, output_path = get_paths()
        results = get_all_results(parse_test_cases(open_xml(file_path)))

        pbar.start()
        update_pbar(pbar, 0)

        unit = total_len / len(results)

        for i, result in enumerate(results):
            print("Processing: Test Case", i + 1)
            n, d = generate_single_testcase(result)
            fa_dataframe, b0_dataframe = generate_dataframe(n, d)
            file_name = create_excel(output_path, "Test_Case_" + str(i + 1))
            process_edr_data(temp_path, output_path, file_name, list(fa_dataframe.columns), pbar, unit * i, unit / 3)
            update_pbar(pbar, unit * i + unit / 3)
            process_acc_data(temp_path, output_path, file_name, list(b0_dataframe.columns), coeff_dic, name_to_description, pbar, unit * i + unit / 3, unit / 3)
            update_pbar(pbar, unit * i + unit * 2 / 3)
            fill_excel_for_one_testcase(output_path, fa_dataframe, b0_dataframe, i + 1)
            update_pbar(pbar, unit * (i + 1))
        pbar.finish()

        print("Finished!\nGenerated", i + 1, "test case files in", output_path)
        input("Press Enter to exit...")

    except UnicodeDecodeError:
        print("[Error] Wrong file format. Check Again!")
    except FileNotFoundError:
        print("[Error] Directories cannot be empty. Check Again!")
    except TypeError:
        break
    else:
        break
