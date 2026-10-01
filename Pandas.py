# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 22:10:14 2025

@author: yehiv
"""


# 匯入需要的套件
import pandas
sfilename = 'test.xlsx'

sheet_name = "Thomas-Muller"

dfs = pandas.read_html("https://fbref.com/en/players/3c6089ab/Thomas-Muller")
df = dfs[4].iloc[:,0:41]

for i in range(10):
    print("fs[" +  str(i) + "]")
    print(dfs[i].iloc[:,0:10])
    print("========================================")    

import xlwings as xw
workbook = xw.Book(sfilename)
sheet = workbook.sheets[sheet_name]
sheet.cells(1,1).value = df