import json
import pymysql


class JsonToMysql:
    def __init__(self,host,user,passwd,db,charset='utf8',port=3306):
        self.db = pymysql.connect(host=host,
                                  user=user,
                                  passwd=passwd,
                                  db=db,
                                  charset=charset,
                                  port=port
                                )
        self.cursor = self.db.cursor()

    def loadfile(self, file):
        fb = open(file, 'r')
        data = json.load(fb)
        return data

    def creat_mysql(self, data, table):
        ddl = '''
            CREATE TABLE `{}` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            '''.format(table)
        for field, word in data.items():
            if word.isdigit():
                ddl = ddl + ' `' + field + '` int(11) DEFAULT NULL,\r\n'
            else:
                if len(word) > 50:
                    ddl = ddl + ' `' + field + '` TEXT ,\r\n'
                elif len(word) > 10:
                    ddl = ddl + ' `' + field + '` varchar('+ str(len(word)+500)  +') DEFAULT NULL,\r\n'
                else:        
                    ddl = ddl + ' `' + field + '` varchar('+ str(len(word)+50)  +') DEFAULT NULL,\r\n'
        ddl = ddl + '''
            PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
            '''
        try:
            self.cursor.execute(ddl)
            self.db.commit
            return True
        except:
            self.db.rollback()
            return False

    def insert(self,table, data):
        sql = 'insert into '+table
        fields = []
        info = []
        for x in data:
            fields.append(x)
            info.append("'"+str(data[x]).replace("'", "\\\'")+"'")
        values = ','.join(fields)
        values = '('+ values +')'
        datas  = ','.join(info)
        sql = sql + values + 'VALUES ('+datas+')'
        try:
           # 执行sql语句
           self.cursor.execute(sql)
           self.db.commit()
           return True,sql

        except:
           # 如果发生错误则回滚
           self.db.rollback()
           return False,sql
        

if __name__ == "__main__":

    file_path = 'data/idiom.json'
    table = 'chengyu'
    json_to_mysql = JsonToMysql('localhost', 'root', '123456', 'poetry')
    info = json_to_mysql.loadfile(file_path)
    is_creat_table = False
    fb = open('error.sql', 'w')
    for data in info:
        if is_creat_table == False:
            if json_to_mysql.creat_mysql(data, table) is not True:
                print('新建数据表失败')
                break
            is_creat_table = True
        res, sql = json_to_mysql.insert(table, data)
        if res == False:
            fb.write(sql + ";\r\n")
    fb.close()
