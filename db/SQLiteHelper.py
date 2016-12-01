# coding:utf-8
from config import DB_CONFIG
from db.SqlHelper import SqlHelper
import time
import MySQLdb

__author__ = 'QC'
import sqlite3


class SqliteHelper(SqlHelper):
    tableName = 'sina_items'

    def __init__(self):
        '''
        建立数据库的链接
        :return:
        '''
        self.database = MySQLdb.connect("172.18.1.25", "root", "root",
                                        "test")  # sqlite3.connect(DB_CONFIG['dbPath'],check_same_thread=False)
        self.database.set_character_set('utf8')
        self.cursor = self.database.cursor()
        # 创建表结构
        # self.createTable()

    def compress(self):
        '''
        数据库进行压缩
        :return:
        '''
        self.database.execute('VACUUM')

    # def createTable(self):
    #     self.cursor.execute("create TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY ,title VARCHAR(100) NOT NULL,"
    #            "url VARCHAR (500) NOT NULL,updatetime TimeStamp NOT NULL DEFAULT (datetime('now','localtime')) )"% self.tableName)
    #
    #     self.database.commit()

    def select(self, tableName, condition, count):
        '''

        :param tableName: 表名
        :param condition: 条件包含占位符
        :param value:  占位符所对应的值(主要是为了防注入)
        :return:
        '''
        command = 'SELECT DISTINCT title,url FROM %s WHERE %s ORDER BY title ASC %s ' % (tableName, condition, count)

        self.cursor.execute(command)
        self.cursor.set_character_set('utf8')
        result = self.cursor.fetchall()
        return result

    def selectAll(self):
        self.cursor.execute('SELECT DISTINCT title,url FROM %s ORDER BY title ASC ' % self.tableName)
        result = self.cursor.fetchall()
        return result

    def selectCount(self):
        self.cursor.execute('SELECT COUNT( DISTINCT title) FROM %s' % self.tableName)
        count = self.cursor.fetchone()
        return count

    def selectOne(self, tableName, condition, value):
        '''

        :param tableName: 表名
        :param condition: 条件包含占位符
        :param value:  占位符所对应的值(主要是为了防注入)
        :return:
        '''
        self.cursor.execute('SELECT DISTINCT title,url FROM %s WHERE %s ORDER BY title ASC' % (tableName, condition),
                            value)
        result = self.cursor.fetchone()
        return result

    def update(self, tableName, condition, value):
        self.cursor.execute('UPDATE %s %s' % (tableName, condition), value)
        self.database.commit()

    def delete(self, tableName, condition):
        '''

        :param tableName: 表名
        :param condition: 条件
        :return:
        '''
        deleCommand = 'DELETE FROM %s WHERE %s' % (tableName, condition)
        # print deleCommand
        self.cursor.execute(deleCommand)

        self.commit()

    def commit(self):
        self.database.commit()

    def insert(self, tableName, value):

        #sina = [value[0], value[1]]
        # print sina
        # self.database.set_character_set('utf8')
        # self.cursor.execute('SET NAMES utf8;')
        # self.cursor.execute('SET CHARACTER SET utf8;')
        # self.cursor.execute('SET character_set_connection=utf8;')
        #self.cursor.execute("INSERT INTO %s (title,url,content,pub_date) VALUES('%s','%s','%s','2016-12-01')" % (tableName,'abc','cde','efg'))
        #time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        self.cursor.execute("INSERT INTO %s (title,url,content,pub_date) VALUES('%s','%s','%s','%s')" % (
        tableName, value[0], value[1], value[0],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))

    def batch_insert(self, tableName, values):

        for value in values:
            if value != None:
                self.insert(self.tableName, value)
        self.database.commit()

    def close(self):
        self.cursor.close()
        self.database.close()


if __name__ == "__main__":
    s = SqliteHelper()
    print s.selectCount()[0]
    # print s.selectAll()
