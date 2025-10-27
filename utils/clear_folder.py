import os, shutil

def clear_folder(path):
    folder_path = path
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)