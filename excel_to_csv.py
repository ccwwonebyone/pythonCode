# -*- coding: utf-8 -*-
import os
import pandas as pd

class ExcelToCsv:

    path = ''
    csv_path = ''
    xls = [ '.xls', '.xlsx' ]

    def __init__(self, path):
        self.path = path
        self.csv_path = self.path + '/../csv'
        if os.path.exists(self.csv_path) is not True:
            os.makedirs(self.csv_path)

    def walk(self):
        for root,dirs,files in os.walk(self.path):
            path_root = root.replace(self.path, self.csv_path)
            if os.path.exists(path_root) is not True:
                os.makedirs(path_root)

            for file in files:
                file_name,suffix = os.path.splitext(file)
                if suffix in self.xls:
                    self.to_csv(root + '/' +file, path_root, file_name)

    def to_csv(self, file_path, save_path, file_name):
        data_xls = pd.read_excel(file_path)
        data_xls.to_csv(save_path + '/' + file_name + '.csv')

if __name__ == '__main__':
    excel_to_csv = ExcelToCsv('/Users/zhangzhirong/Desktop/gongju/excels')
    excel_to_csv.walk()
