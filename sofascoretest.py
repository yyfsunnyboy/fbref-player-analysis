# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 22:42:40 2025

@author: 葉陽甫
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 22:10:14 2025

@author: yehiv
"""


# 匯入需要的套件
import pandas
# from bs4 import BeautifulSoup
# import urllib.request 
# soup = BeautifulSoup(html, "html5lib")
sfilename = 'test.xlsx'

sheet_name = "Ruben-Dias"

dfs = pandas.read_html("http://fotmob.com/players/1288450/rico-lewis")
# df = dfs[2].iloc[:,0:41]

# for i in range(0,15,2):
#     print("fs[" +  str(i) + "]")
#     print(dfs[i].iloc[:,0:10])
#     print("========================================")    
    
print("fs[" +  str(1) + "]")
print(dfs[1].iloc[:,0:10])
print("========================================")    

import xlwings as xw
workbook = xw.Book(sfilename)
sheet = workbook.sheets[sheet_name]
#sheet.cells(1,1).value = df
