import pathlib

def get_notebook_path():
    return str(pathlib.Path().resolve())