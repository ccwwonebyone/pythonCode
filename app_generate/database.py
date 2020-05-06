# -*- coding: utf-8 -*-

import pymysql,os


class DateBase:
    def __init__(self, host, user, passwd, db, charset='utf8', port=3306):
        self.db = pymysql.connect(host=host,
                                  user=user,
                                  passwd=passwd,
                                  db=db,
                                  charset=charset,
                                  port=port)
        self.cursor = self.db.cursor()
    
    def get_dbs(self):
        sql = 'show databases'
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_tables(self):
        sql = 'show table status'
        self.cursor.execute(sql)
        tables = []
        for table in self.cursor.fetchall():
            tables.append({'name': table[0], 'engine': table[1], 'collection': table[14], 'comment': table[17]})
        return tables

    def get_columns(self, table):
        sql = 'show full columns from `'+table+'`'
        self.cursor.execute(sql)
        columns = []
        for column in self.cursor.fetchall():
            column_comment = str(column[8]).replace("\r", "")
            column_comment = column_comment.replace("\n", "")
            column_comment = column_comment.replace("|", " ")
            columns.append({
                'name': str(column[0]),
                'comment': column_comment,
                'type': str(column[1]),
                'isnull': str(column[3]),
                'default': str(column[5]),
                'collection': str(column[2]),
            })
        return columns
    