import pymongo

class mongo():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 27017
        self.client = pymongo.MongoClient(self.host,self.port)
    def select(self,db_name):
        self.conn = self.client[db_name]
    def getAll(self):
        print(self.conn.collection_names())


# s =mongo()
# s.select('10')
# print(list(s.conn['47656'].find({'start': '14:00'})))
# import pymysql
#
# # 打开数据库连接
# db = pymysql.connect("localhost", "root",'wangming','test')
#
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
#
# # 使用 fetchone() 方法获取单条数据.
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
#
# # 使用预处理语句创建表
# sql = """CREATE TABLE EMPLOYEE (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,
#          SEX CHAR(1),
#          INCOME FLOAT )"""
#
# cursor.execute(sql)
# # SQL 插入语句
# sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
#          LAST_NAME, AGE, SEX, INCOME)
#          VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
# try:
#     # 执行sql语句
#     cursor.execute(sql)
#     # 提交到数据库执行
#     db.commit()
# except:
#     # 如果发生错误则回滚
#     db.rollback()
#
# # try:
# #    # 执行sql语句
# #    cursor.execute(sql)
# #    # 提交到数据库执行
# #    db.commit()
# # except:
# #    # 如果发生错误则回滚
# #    db.rollback()
# # 关闭数据库连接
# db.close()