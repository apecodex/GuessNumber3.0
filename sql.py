import pymysql
import sqlite3
import hashlib

class Mysql():
    def __init__(self):
        try:
            self.connect_sql = pymysql.connect(user="root", password="crazyrookie", host="127.0.0.1", port=3306)
            self.connect_cursor = self.connect_sql.cursor()
            self.connect_cursor.execute("CREATE DATABASE IF NOT EXISTS guessnumber DEFAULT CHARACTER SET utf8;")
            self.connect_sql.commit()
            self.connect_cursor.execute("USE guessnumber;")
        except pymysql.err.OperationalError:
            pass

    def sava(self,username,password,email):
        # sql1 = """
        #     CREATE DATABASE IF NOT EXISTS guessnumber DEFAULT CHARACTER SET utf8;
        #     USE guessnumber;
        #     CREATE TABLE IF NOT EXISTS user(
        #         username VARCHAR(88),
        #         password VARCHAR(88),
        #         email VARCHAR(88)
        #     );
        #     """
        # self.connect_cursor.execute(sql1)
        # self.connect_sql.commit()

        sql = "INSERT INTO user (username,password,email) VALUES ('{}','{}','{}')".format(username,password,email)
        self.connect_cursor.execute(sql)
        self.connect_sql.commit()

    # 检查用户名是否正确~
    def check_username(self,username):
        sql = "SELECT username FROM user WHERE username='{}'".format(username)
        try:
            self.connect_cursor.execute(sql)
            fetchall = self.connect_cursor.fetchall()
            for i in fetchall:
                return i[0]
        except pymysql.err.ProgrammingError:
            sql1 = """
        	    CREATE DATABASE IF NOT EXISTS guessnumber DEFAULT CHARACTER SET utf8;
        	    USE guessnumber;
        	    CREATE TABLE IF NOT EXISTS user(
        	        username VARCHAR(88),
        	        password VARCHAR(88),
        	        email VARCHAR(88)
        	    );
        	    """
            self.connect_cursor.execute(sql1)
            self.connect_sql.commit()
        finally:
            self.connect_cursor.execute(sql)
            fetchall = self.connect_cursor.fetchall()
            for i in fetchall:
                return i[0]

    # 检查密码是否正确~
    def check_password(self,username,password):
        md5 = hashlib.md5()
        md5.update((str(username) + str(password) + "guess*number").encode())
        sql = "SELECT password FROM user WHERE password='{}'".format(md5.hexdigest())
        self.connect_cursor.execute(sql)
        fetchall = self.connect_cursor.fetchall()
        for i in fetchall:
            return i[0]

    # 通过email查找用户名和密码,有就返回元组,没有则返回None~
    def check_email_password(self,email):
        if self.check_email(email) != None:
            sql = "SELECT username,password FROM user WHERE email='{}'".format(email)
            self.connect_cursor.execute(sql)
            fetchall = self.connect_cursor.fetchall()
            for i in fetchall:
                return i
        else:
            pass

    # 查找email,没有则返回None~
    def check_email(self,email):
        sql = "SELECT email FROM user WHERE email='{}'".format(email)
        self.connect_cursor.execute(sql)
        fetchall = self.connect_cursor.fetchall()
        for i in fetchall:
            return i[0]

    # 通过email查询用户名,如果没有则返回None~
    def get_username(self,email):
        sql = "SELECT username FROM user WHERE email='{}'".format(email)
        self.connect_cursor.execute(sql)
        fetchall = self.connect_cursor.fetchall()
        for i in fetchall:
            return i[0]

    # 忘记密码时,利用用户名和邮箱来判断是否可以修改密码~
    def check_forget_pass(self,username,email):
        sql = "SELECT * FROM user WHERE username='{}' and email='{}'".format(username,email)
        self.connect_cursor.execute(sql)
        fetchall = self.connect_cursor.fetchall()
        for i in fetchall:
            return i

    def change_pass(self,new_pass,username,email):
        sql = "UPDATE user SET password='{}' WHERE username='{}' and email='{}'".format(new_pass,username,email)
        self.connect_cursor.execute(sql)
        self.connect_sql.commit()

class Sqlite():

    def __init__(self):
        self.connect_sql = sqlite3.connect("guessnumber.db")
        self.connect_cursor = self.connect_sql.cursor()

    def sava(self,username,password,email):
        # sql1 = """
        #     CREATE TABLE IF NOT EXISTS user(
        #         username VARCHAR(88),
        #         password VARCHAR(88),
        #         email VARCHAR(88)
        #     );
		#
        #     INSERT INTO user (username,password,email) VALUES ('ceshi','ceshi','ceshi@16.com')
        #     """
        # self.connect_cursor.executescript(sql1)
        # self.connect_sql.commit()

        sql = "INSERT INTO user (username,password,email) VALUES ('{}','{}','{}')".format(username,password,email)
        self.connect_cursor.execute(sql)
        self.connect_sql.commit()

    def ceshi(self):
        self.connect_cursor.execute("SELECT * FROM user")
        for i in self.connect_cursor.fetchall():
            print(i)

    # 检查用户名是否正确~
    def check_username(self,username):
        sql = "SELECT username FROM user WHERE username='{}'".format(username)
        try:
            for i in self.connect_cursor.execute(sql):
                return i[0]
        except sqlite3.OperationalError:
            connect_sql = sqlite3.connect("guessnumber.db")
            connect_cursor = connect_sql.cursor()
            sql1 = """
        	    CREATE TABLE IF NOT EXISTS user(
        	        username VARCHAR(88),
        	        password VARCHAR(88),
        	        email VARCHAR(88)
        	    );

        	    INSERT INTO user (username,password,email) VALUES ('ceshi','ceshi','ceshi@16.com')
        	    """
            connect_cursor.executescript(sql1)
            connect_sql.commit()
        finally:
            for i in self.connect_cursor.execute(sql):
                return i[0]


    # 检查密码是否正确~
    def check_password(self,username,password):
        md5 = hashlib.md5()
        md5.update((str(username) + str(password) + "guess*number").encode())
        sql = "SELECT password FROM user WHERE password='{}'".format(md5.hexdigest())
        for i in self.connect_cursor.execute(sql):
            return i[0]

    # 通过email查找用户名和密码,有就返回元组,没有则返回None~
    def check_email_password(self,email):
        if self.check_email(email) != None:
            sql = "SELECT username,password FROM user WHERE email='{}'".format(email)
            for i in self.connect_cursor.execute(sql):
                return i
        else:
            pass

    # 查找email,没有则返回None~
    def check_email(self,email):
        sql = "SELECT email FROM user WHERE email='{}'".format(email)
        for i in self.connect_cursor.execute(sql):
            return i[0]

    # 通过email查询用户名,如果没有则返回None~
    def get_username(self,email):
        sql = "SELECT username FROM user WHERE email='{}'".format(email)
        for i in self.connect_cursor.execute(sql):
            return i[0]

    # 忘记密码时,利用用户名和邮箱来判断是否可以修改密码~
    def check_forget_pass(self,username,email):
        sql = "SELECT * FROM user WHERE username='{}' and email='{}'".format(username,email)
        for i in self.connect_cursor.execute(sql):
            return i

    def change_pass(self,new_pass,username,email):
        sql = "UPDATE user SET password='{}' WHERE username='{}' and email='{}'".format(new_pass,username,email)
        self.connect_cursor.execute(sql)
        self.connect_sql.commit()
#
s = Sqlite()
# m = Mysql()
# s.ceshi()
# print(s.check_email("159753@qq.com"))
# print(check_password("1473018671@qq.com","123456s"))
# md5 = hashlib.md5()
# md5.update((str(check_email_password("123456@qq.com")[0]) + str("123456s") + "guess*number").encode())
# print(check_email_password("123456@qq.com")[1] == md5.hexdigest())
# print(get_username("1473018671@qq.com"))
# print(m.check_forget_pass("Crazy","1473018671@qq.com"))
# print(check_email("1473018671@163.com"))
