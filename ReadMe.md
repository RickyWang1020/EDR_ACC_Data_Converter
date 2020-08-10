# EDR ACC Data Converter Documentation

## Workflow (in main.py)
1）初始化设置：
  - 初始化进度条
  
        # progress bar operation
        total_len = 1000000
        widgets = ['Progress: ', Percentage(), ' ', Bar('>'), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
        pbar = ProgressBar(widgets=widgets, maxval=total_len, redirect_stdout=True)
  
  - 阅读config文件和template文件

        # read the config file
        conf = read_config(os.path.join(SETUP_DIR, "config", "var_conf.yaml"))
        coeff_dic = conf["coefficient"]
        name_to_description = conf["name_to_description"]

        temp_path = os.path.join(SETUP_DIR, "template", "Template.xlsx")

2）while True部分（如果出现非法路径输入则会持续循环直到接收到合法输入）
  - 通过tkinter窗口获取原始数据和输出excel的路径
  
        file_path, output_path = get_paths()
        
       - 函数解释：
            - `get_paths()`：显示tkinter窗口，接收用户选择的原始数据和输出excel的路径并且将两条路径存储为string形式输出

  - 处理XML文件数据，过滤出以特定字段开头的数据
  
        results = get_all_results(parse_test_cases(open_xml(file_path)))
        
       - 函数解释：
            - `open_xml(path)`：接收XML文件路径并将其转化为beautifulsoup文档类型，便于之后按标签过滤分析
            - `parse_test_cases(bs_file)`：接收 `open_xml(path)` 输出的文档，按照testcase标签将整个文档分割为多个test cases，输出一个list，list内每个元素为一个test case所对应的beautifulsoup文档
            - `get_all_results(testcases)`：接收 `parse_test_cases(bs_file)` 输出的list，遍历这个list内的每个test case文档，将符合条件的数据摘出（判断方法：commname标签以protocols开头），转为string后放入一个list中。最后将每个test case的list按顺序放入一个大list中输出（注意，此时只是筛选出符合protocols开头的所有数据，尚未按数据名称，如FA13等，筛选出特定需要的数据类型）
                
                输出举例：
                
                `[["[0x62, 0xFA, ...]", "[0x62, 0xFA, ...]", ...], [...], [...], ...]`

  - 遍历 `get_all_results(testcases)` 筛选出的list，每一次循环即处理一个test case，先按指定字头筛选处理数据生成pandas数据表，然后创建excel文件将数据表填入excel中
  
        n, d = generate_single_testcase(result)
        fa_dataframe, b0_dataframe = generate_dataframe(n, d)
        file_name = create_excel(output_path, "Test_Case_" + str(i + 1))
        process_edr_data(temp_path, output_path, file_name, list(fa_dataframe.columns), pbar, unit * i, unit / 3)
        update_pbar(pbar, unit * i + unit / 3)
        process_acc_data(temp_path, output_path, file_name, list(b0_dataframe.columns), coeff_dic, name_to_description, pbar, unit * i + unit / 3, unit / 3)
        update_pbar(pbar, unit * i + unit * 2 / 3)
        fill_excel_for_one_testcase(output_path, fa_dataframe, b0_dataframe, i + 1)
        update_pbar(pbar, unit * (i + 1))
        
       - 函数解释：
            - `generate_single_testcase(result_code)`：接收单个test case经过筛选后的结果数据，将数据切分成数据类型（例如FA13）和数据内容（以list形式存储的一串string，如 `["0xFF", "0xFF", ...]` ），分别存储在name_list和data_list中，返回这两个list（list可以保证存储的数据是按照XML文件中数据的输入顺序放入的，而不会像dictionary一样将数据打乱）
            - `generate_dataframe(name_lst, data_lst, wanted_FA = ["FA13", "FA14", "FA15"], wanted_B0 = ["B032", "B033", "B034", "B035", "B036", "B037", "B042", "B043", "B052", "B053"])`：name_lst和data_lst依次接收`generate_single_testcase(result_code)`输出的两个list，wanted_FA和wanted_B0是excel中需要出现的EDR和ACC数据类型名称（有预设值，也可以根据情况修改）。该函数首先根据wanted_FA和wanted_B0的值，将符合条件的EDR和ACC数据挑出（此时才筛选出特定需要的数据类型名称），然后生成EDR和ACC数据的pandas数据表格形式，返回这两个数据表格
            - `create_excel(directory, file_name)`：接收想要创建excel文件的路径以及excel文件名，在指定路径生成一个 `.xlsx` 文件并返回文件名（带后缀）
            - `process_edr_data(temp_dir, file_dir, data_file_name, edr_column, pbar, progressbar_hist, progressbar_length)`：将template的格式按EDR数据的数量复制多次，并在这个过程中间实时更新进度条
            - `process_acc_data(temp_dir, file_dir, data_file_name, acc_column, coeff_dic, name_to_description, pbar, progressbar_hist, progressbar_length)`：将template的格式按ACC数据的数量复制多次，同时填入相应的数据计算公式，并在这个过程中间实时更新进度条
            - `fill_excel_for_one_testcase(working_dir, FA_dataframe, B0_dataframe, test_case_index)`：将这个test case的所有ACC和EDR数据填入有格式的excel表格的特定位置中
            - `update_pbar(progress_bar, progress)`：更新进度条到一个新的progress value的函数

  - except部分：报错情况的处理
  
        except UnicodeDecodeError:
            print("[Error] Wrong file format. Check Again!")
        except FileNotFoundError:
            print("[Error] Directories cannot be empty. Check Again!")
        except TypeError:
            break
        else:
            break
       
       - 各个情况解释：
            - `UnicodeDecodeError`：在本程序出现的原因是选择数据文件时文件格式错误（不是XML文件），因此重新运行本程序，让用户重新选择
            - `FileNotFoundError`：在本程序出现的原因是选择路径时包含了空路径，因此重新运行本程序，让用户重新选择
            - `TypeError`：在本程序中出现的原因是点击右上角“X”号关闭了弹出的tkinter窗口，因此退出程序
            - `else`：try部分正常运行，没有报错，终止整个while loop并退出程序
            
## Variables Subject to Change
  - `var_conf.yaml`：
  
      - `coefficient`：ACC数据表格中计算函数需要乘的系数，key是数据类型名，value是系数
      - `name_to_description`：ACC数据表格中的description表头，key是数据类型名，value是description
      
  - `copy_acc_edr.py`：
  
      - `acc_convert_function`中，返回的值是写入excel表格中的数据计算公式，由于返回值形式比较复杂（需要将不同的行、列数放入该计算公式中然后返回），建议直接在该函数内修改计算公式
      
## How to Pack this Project into .EXE?

1） 确保Python版本在3.5及以上，这样更适合打包程序运行

2） 下载安装Pyinstaller：https://pypi.org/project/PyInstaller/#files 下载tar.gz压缩包，解压后会得到一个Pyinstaller-3.6.tar的压缩包，再次解压之后可以得到一个Pyinstaller-3.6的文件夹，这就是Pyinstaller的程序包

3） 将本程序的文件夹复制一份到Pyinstaller-3.6文件夹内（也可以跳过这一操作，但是复制之后方便在Pyinstaller-3.6的文件夹内直接进行操作）

4） 打开cmd，把路径切换到Pyinstaller-3.6文件夹内的本程序文件夹下（如果没有做上一步，则直接把路径切换到本程序文件夹下）：

    cd /yourpath/(Pyinstaller-3.6/)EDR_ACC_Data_Converter

5） 首先创建 `.spec` 配置文件，由于本程序的主文件是 `main.py` ，因此我们需要为 `main.py` 创建配置文件，在cmd输入如下指令：

    pyi-makespec -w main.py
    
   然后文件夹内就会出现一个 `main.spec` 配置文件，可以通过修改该文件来指引Pyinstaller按照我们的需求打包出 `.exe` 文件

6） 打开 `main.spec` ，修改以下参数：
  - 在开头 `# -*- mode: python ; coding: utf-8 -*-` 的下一行，加上：

        import sys
        sys.setrecursionlimit(1000000)

    这是因为本程序内有些import的库会自我循环迭代，迭代次数过多就会超出系统默认的递归次数，因此需要将最大递归次数设置得大一点，才能成功创建文件
    
  - 在 `a = Analysis` 后的括号中，在第一个方括号内，加入本程序使用到的所有Python文件路径（也就是程序中import过的Python文件，不是库），例如，将目前的程序用到的几个文件加入方括号中（由于当前路径已经是本程序的文件夹，因此这些文件的路径直接写文件名即可）：
  
        a = Analysis(['main.py', 'copy_acc_edr.py', 'excel.py', 'frozen_dir.py', 'function.py', 'select_file.py'], pathex=...
        
    这样会提示Pyinstaller找到import过的文件
  - 同样在 `a = Analysis` 后的括号中，在 `datas=` 后的方括号内，写入本程序还需要用到的其他类型文件（非.py文件），例如本程序目前应该加入的配置：
  
        datas=[('var_conf.yaml', 'config'), ('Template.xlsx', 'template')]
        
    第一个tuple：`('var_conf.yaml', 'config')`，第一个元素是需要用到的文件的路径，第二个元素是在打包完成的 `.exe` 所在文件夹内创建一个叫 `config` 的文件夹放置一份 `var_config.yaml` 的复制本，便于生成的 `.exe` 在要读取该 `.yaml` 文件时找到文件位置。第二个tuple也是同理
  - 在 `exe = EXE` 后的括号中，找到 `console=False` 这个参数，可见默认值是False，表示生成的 `.exe` 程序默认不会出现cmd窗口。但是本程序需要借助cmd窗口显示当前处理的文件进度，因此需要将这一参数修改为 `console=True`

7） 保存好 `.spec` 文件之后，回到先前的cmd，在命令行输入：

    pyinstaller -D main.spec
        
   意为将本程序的所有文件打包成一个目录，这个目录中包含 `.exe` 文件，以及需要import或需要读的库、程序、文件
   
   此时打开程序文件夹，会发现新生成了两个文件夹：dist和build，build是打包过程中生成的临时文件目录，之后可以删除，dist则是打包完成后的目录，打开后可以找到 `main.exe` 文件。可以将 `main.exe` 拖动到cmd中运行，也可以写一个 `.bat` 脚本来一键运行
   
   - 创建 `.bat` 脚本的方法：
   
        在 `main.exe` 所在文件夹内（如果严格按照上述步骤，`main.exe` 所在文件夹应该是 `/dist/main/` ）新建文本文档，在里面写入以下两行：
        
          cd /d %~dp0
          main.exe
        
        随后将文本文档后缀名改成 `.bat` ，此时双击 `.bat` 文件即可运行 `main.exe` 文件
        
8） 如果在生成了dist和build之后又对 `.spec` 文件做了修改并且想要重新打包，建议先删除之前生成的dist和build文件夹，然后输入打包指令，这样会生成新的dist和build文件夹（如果不删除之前的文件夹而直接再次打包，有可能会在覆盖先前的dist和build文件夹时发生权限错误，因此建议先删除这两个文件夹）

9） 打包完成之后，如果要将程序移植到其他计算机运行，则需要将 `main.exe` 所在的整个文件夹进行迁移，因为 `main.exe` 所在的文件夹内包含该程序需要的运行环境，因此需要一并移动
