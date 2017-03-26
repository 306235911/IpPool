# -*- coding:utf-8 -*-

import MySQLdb

class Mysql:
    
    # 连接数据库
    def __init__(self):
        try:
            # 连接中加上的 charset="utf8" 可省略下面的 self.db.set_character_set('utf8')
            self.db = MySQLdb.Connect('localhost' , 'root' , '306235911' , 'ippool', charset="utf8")
            self.cur = self.db.cursor()
            # sql = "DELETE FROM ippool WHERE identity >= 0"
            # self.cur.execute(sql)
            # self.db.commit()
            #
            # self.clearn()
        except MySQLdb.Error , e:
            print u"连接数据库错误，原因 %d : %s" % (e.args[0] ,e.args[1])
            
    def clearnIp(self):
        sql = "DELETE FROM ip WHERE id >= 0"
        self.cur.execute(sql)
        self.db.commit()
        
    def clearnUsefulIp(self):
        sql = "DELETE FROM usefulIp WHERE id >= 0"
        self.cur.execute(sql)
        self.db.commit()
            
    def insertData(self, identity, ip, port):
        # sql = "INSERT INTO book VALUES (%d,%s,%s,%s,%s)" % (identity , name , info , score , num)
        sql = "INSERT INTO ip VALUES " + "(%s,%s,%s)"
        try:
            self.db.set_character_set('utf8')
            # result = self.cur.execute(sql)
            
            # 比起 "INSERT INTO table VALUES(%s,%s,%s)" % (a,b,c) 的用法，更常用的为下面的表达
            result = self.cur.execute(sql,(identity, ip, port))
            # insert_id = self.db.insert_id()
            self.db.commit()
            if result:
                return True
            else:
                return False
        except MySQLdb.Error , e:
            self.db.rollback()
            if "'key'PRIMARY" in e.args[1]:
                print u"数据已存在，未插入数据"
            else:
                print u"插入数据失败，原因 %d : %s" % (e.args[0] ,e.args[1])
     
    def selectData(self):
        sql = "SELECT * FROM usefulIp"
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            return result
            # self.db.commit()
            # if result:
            #     return True
            # else:
            #     return False
        except MySQLdb.Error ,e :
        # except:
            self.db.rollback()
            print u"读取数据失败，原因 %d : %s" % (e.args[0] ,e.args[1])
            
    def usefulIp(self, identity, proxy):
        sql = "INSERT INTO usefulIp VALUES " + "(%s,%s)"
        try:
            self.db.set_character_set('utf8')
            # result = self.cur.execute(sql)
            
            # 比起 "INSERT INTO table VALUES(%s,%s,%s)" % (a,b,c) 的用法，更常用的为下面的表达
            result = self.cur.execute(sql,(identity, proxy))
            # insert_id = self.db.insert_id()
            self.db.commit()
            if result:
                return True
            else:
                return False
        except MySQLdb.Error , e:
            self.db.rollback()
            if "'key'PRIMARY" in e.args[1]:
                print u"数据已存在，未插入数据"
            else:
                print u"插入数据失败，原因 %d : %s" % (e.args[0] ,e.args[1])
            
            