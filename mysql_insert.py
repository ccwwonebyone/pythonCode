# -*- coding: utf-8 -*-

import pymysql,datetime,random,time,threading

class Insert_capturerecord (threading.Thread):
    def __init__(self, db, cursor,picList):
        threading.Thread.__init__(self)
        self.db = db
        self.cursor = cursor
        self.picList = picList
    def run(self):
        date = datetime.datetime.now().strftime('%Y%m%d')
        table = 'capturerecord_' + date
        sql = """CREATE TABLE IF NOT EXISTS  `"""+table+"""` (
              `caprecid` int(11) NOT NULL AUTO_INCREMENT,
              `captime` datetime DEFAULT NULL,
              `bodypicurl` varchar(128) DEFAULT NULL,
              `facepicurl` varchar(128) DEFAULT NULL,
              `quality` float DEFAULT NULL,
              `dev_devid` int(11) DEFAULT NULL,
              PRIMARY KEY (`caprecid`)
            ) ENGINE=MyISAM DEFAULT CHARSET=utf8"""
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute(sql)
        while True:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %T')
            pic = picList[random.randrange(0,len(self.picList))]
            quality = str(random.randrange(60,100))
            devid = str(random.randrange(3,7))
            # SQL 插入语句
            insert_capturerecord_sql = """INSERT INTO {}(captime,
                     bodypicurl, facepicurl, quality, dev_devid)
                     VALUES ('{}', '{}', '{}',{}, {})""".format(table,now_time,pic,pic,quality,devid)

            try:
               # 执行sql语句
               cursor.execute(insert_capturerecord_sql)
               # 提交到数据库执行
               db.commit()
               print("插入表：{},插入时间：{},插入设备：{}".format(table,now_time,devid))
            except:
               # 如果发生错误则回滚
               db.rollback()
               print('插入失败')

            sleepTime = random.randrange(1,10)
            time.sleep(sleepTime)

class Insert_alertrecord (threading.Thread):
    def __init__(self, db, cursor,picList,capresultid):
        threading.Thread.__init__(self)
        self.db = db
        self.cursor = cursor
        self.picList = picList
        self.capresultid = capresultid
    def run(self):
        while True:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %T')
            pic = picList[random.randrange(0,len(self.picList))]
            score = str(random.randrange(60,100))
            employee_empid = str(random.randrange(3,7))
            dev_devid = str(random.randrange(3,7))
            serinfo_serid = str(random.randrange(1,10))
            self.capresultid = self.capresultid + 1
            # SQL 插入语句
            insert_capturerecord_sql = """INSERT INTO alertrecord(alerttime,
                     bodypicurl, facepicurl, employee_empid,
                     alertpicurl,score,dev_devid,serinfo_serid,capresultid)
                     VALUES ('{}', '{}', '{}','{}', '{}',{},{},{},{})""".format(now_time,pic,pic,
                        employee_empid,pic,score,dev_devid,serinfo_serid,self.capresultid )

            try:
               # 执行sql语句
               cursor.execute(insert_capturerecord_sql)
               # 提交到数据库执行
               db.commit()
               print("插入表：alertrecord,插入时间：{},插入人员：{},记录ID：{}".format(now_time,employee_empid,self.capresultid ))
            except:
               # 如果发生错误则回滚
               db.rollback()
               print("插入失败")

            sleepTime = random.randrange(1,10)
            time.sleep(sleepTime)

# 打开数据库连接
db = pymysql.connect(host='192.168.0.223',
    port=3306,
    user='root',
    passwd='123456',
    db='face',
    charset='utf8'
 )




# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

picList = ['http://image79.360doc.com/DownloadImg/2014/11/1401/47085930_1.jpg',
            'http://image79.360doc.com/DownloadImg/2014/11/1401/47085930_2.jpg',
            'http://image79.360doc.com/DownloadImg/2014/11/1401/47085930_3.jpg',
            'http://image79.360doc.com/DownloadImg/2014/11/1401/47085930_4.jpg',
            'http://image79.360doc.com/DownloadImg/2014/11/1401/47085930_5.jpg']
capresultid = 1

# 创建新线程
insert_capturerecord_thread = Insert_capturerecord(db, cursor,picList)
insert_alertrecord_thread = Insert_alertrecord(db, cursor,picList,capresultid)

insert_capturerecord_thread.start()
insert_alertrecord_thread.start()

insert_capturerecord_thread.join()
insert_alertrecord_thread.join()

db.close()