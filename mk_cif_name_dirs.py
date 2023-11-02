import time
from tqdm import tqdm
tqdm.pandas()  # set up for progress_apply method
from os import path
import re
from pathlib import Path
import pandas as pd


def get_subdir_list(p_sub_list):
    """
    To get a sub directory path list, Use thie func().
    
    pram: p_aub_list: specify a directory which sub dirs is gotten from.
    """
    # 引数の直下のディレクトリ・パスの一覧を取得
    sub_dir_list_temp = []
    for p_sub in p_sub_list:
        sub_dir_list_temp.append([p_s_s for p_s_s in p_sub.iterdir()])
    # ２次元リストを１次元リスト化
    return sum(sub_dir_list_temp, [])


p = Path('../cif/')
p_sub_list = [p_s for p_s in p.glob('[0-9]')]

cif_path_list = get_subdir_list(get_subdir_list(get_subdir_list(p_sub_list)))


def cif_filter(cif_file_path):
    pattern = '.*\.cif'
    cif_file_path_str = str(cif_file_path)
    return bool(re.match(pattern, cif_file_path_str))


cif_path_list = [path for path in cif_path_list if cif_filter(path)]


def path2df(cif_path_list):

    dict_ = {"cif_AbsPath": [str(elem) for elem in cif_path_list],
             "FolderPath": [path.split(cif_path)[0] for cif_path in cif_path_list],
             "FileName": [path.split(cif_path)[1] for cif_path in cif_path_list],
             "cif_s_dir": [str(elem).split('/')[2] for elem in cif_path_list],
             "cif_ss_dir": [str(elem).split('/')[3] for elem in cif_path_list],
             "cif_sss_dir": [str(elem).split('/')[4] for elem in cif_path_list],
            }
    
    return pd.DataFrame(dict_)


df = path2df(cif_path_list)


def mk_cif_folder_name(df):
    """
    To create a cif_FolderName column, Use thie func().
    """
    return df['FolderPath'] + '/' + df['FileName'].split(".")[0]


df['cif_FolderName'] = df.apply(mk_cif_folder_name, axis=1)

# monitering how long does thie command take
before = time.time()
# make cif name directorys
df.progress_apply(lambda row: mk_cif_num_folder(row['cif_FolderName']), axis=1)
after = time.time()
print(f"it took {after - before}sec to make all of cif name directories.")