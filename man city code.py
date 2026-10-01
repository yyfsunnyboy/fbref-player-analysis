# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 22:01:12 2025

@author: 葉陽甫
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 22:10:14 2025

@author: yehiv
"""


# 匯入需要的套件
import pandas
import time
sfilename = 'man city player.xlsx'
sheetname = "name to web"
import xlwings as xw
workbook = xw.Book(sfilename)
sheet = workbook.sheets[sheetname]
    # name=input(str())
for i in range(1,13):
    print("num=")
    print(i)
    stmp=sheet.cells(i,1).value
    print("stemp=",stmp)
    num=i
    fnum5game=int(sheet.cells(i,3).value)
    # fnumcarran=int(sheet.cells(i,4).value)
    sheet_name = sheet.cells(num,1).value  
    # sheet_name_carrer=sheet.cells(num,1).value  ' career'
    print(sheet_name)
    dfs = pandas.read_html(sheet.cells(num,2).value)
    time.sleep(3)
    print(int(fnum5game))
    df5game = dfs[fnum5game].iloc[:,0:41]
    # print(int(fnumcarran))
    # dfcarran = dfs[fnumcarran].iloc[0:20, 28:36]
    
    for i in range(10):
        print("fs[" +  str(i) + "]")
        print(dfs[i].iloc[:,0:10])
        print("========================================")    
    
    import xlwings as xw
    workbook = xw.Book(sfilename)
    sheet = workbook.sheets[sheet_name]
    sheet.cells(1,1).value = df5game
    # sheet.cells(10,1).value = dfcarran

