

# sourcery skip: assign-if-exp, remove-zero-from-range
import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re


import xlrd


root = tk.Tk()    # 显式创建根窗体
root.withdraw()   # 将根窗体隐藏

file = filedialog.askopenfilename(parent=root, title='打开统计excel文件')

folder = filedialog.askdirectory(parent=root, title='打开需要统计文件夹')

# data1 = pd.read_excel(file, index_col='科室')
data1 = pd.read_excel(file, index_col=0)

file_list = os.listdir(folder)

for i in range(29):
    for filename in file_list:
        if data1.index[i] in filename:
            data = pd.read_excel(folder+'//'+filename)
            for j in range(0, 9):
                for k in range(1, 18):
                    if data1.columns[j] in data.values[k, 1]:
                        temp = data.values[k, 3]
                        temp = re.findall(r"\d+\.?\d*", temp)
                        if len(temp) > 1:
                            temp = float(temp[1])
                        else:
                            temp = 100

                        data1.iloc[i, j] = temp



data1.to_excel(file)