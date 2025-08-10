import os

image_file=[]
list_ignore=["chat.py","chromedriver.exe","pdfmaker.py","sel.py","trial.py","merged_chats.pdf","__pycache__","deleter.py"]
for name in os.listdir(os.getcwd()):
    if name not in list_ignore:
        os.remove(name)