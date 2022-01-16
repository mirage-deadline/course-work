import os

def create_folder() -> None:
    folder_list = ['res_csv', 'result', 'author_poem']
    for folder in folder_list:
        os.makedirs(folder, exist_ok=True)