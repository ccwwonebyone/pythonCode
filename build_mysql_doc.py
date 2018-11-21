# -*- coding: utf-8 -*-

import pymysql,os

class BuildMysqlDoc:
    def __init__(self,host,user,passwd,db,charset='utf8',port=3306):
        self.db = pymysql.connect(host=host,
                                  user=user,
                                  passwd=passwd,
                                  db=db,
                                  charset=charset,
                                  port=port
                                )
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
            tables.append({'name':table[0],'engine':table[1],'collection':table[14],'comment':table[17]})
        return tables

    def get_cloumns(self,table):
        sql = 'show full columns from '+table
        self.cursor.execute(sql)
        columns = []
        for column in self.cursor.fetchall():
            columns.append({
                'name':str(column[0]),
                'comment':str(column[8]),
                'type':str(column[1]),
                'isnull':str(column[3]),
                'default':str(column[5]),
                'collection':str(column[2]),
            })
        return columns
if __name__ == '__main__':
    host    = input('ip地址(localhost):')
    user    = input('用户名(root):')
    passwd  = input('密码:')
    db      = input('数据库:')
    charset = input('字符集(utf8):')
    port    = input('端口(3306):')
    if not db or not passwd:
        print('请输入正确的信息:密码,数据库')
        exit
    host    = host    if host    else 'localhost'
    user    = user    if user    else 'root'
    charset = charset if charset else 'utf8'
    port    = port    if port    else 3306

    build_mysql_doc = BuildMysqlDoc(host,user,passwd,db,charset,port)
    # print(build_mysql_doc.get_tables())
    fields = {
        'name':'字段',
        'comment':'注释',
        'type':'类型',
        'isnull':'能否为null',
        'default':'默认值',
        'collectio':'字符集',
    }
    field_str = ' | '.join(list(fields.values()))
    table_str = '---|'*len(fields)
    table_str = table_str[:-1]
    handler = open(db+'.md','w')
    content = '[TOC]'
    content += "\r\n"
    content += '# '+db
    for table in build_mysql_doc.get_tables():
        content += """
---
## *"""+table['name']+'-'+table['comment']+"""*
```
注释："""+table['comment']+"""
engine："""+table['engine']+"""
字符集："""+table['collection']+"""
```
"""+field_str+"""
"""+table_str+"""
"""
        for column in build_mysql_doc.get_cloumns(table['name']):
            content += ' | '.join(list(column.values()))
            content += "\r\n"
    handler.write(content)
    handler.close()
