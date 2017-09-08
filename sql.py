import pymysql
import hashlib

connect_sql = pymysql.connect(user="root", password="crazyrookie", host="127.0.0.1", port=3306)
connect_cursor = connect_sql.cursor()
connect_cursor.execute("USE guessnumber;")

def sava(username,password,email):
    sql1 = """
        CREATE DATABASE IF NOT EXISTS guessnumber DEFAULT CHARACTER SET utf8;
        USE guessnumber;

        CREATE TABLE IF NOT EXISTS user(
            username VARCHAR(88),
            password VARCHAR(88),
            email VARCHAR(88)
        );
        """
    connect_cursor.execute(sql1)
    connect_sql.commit()

    sql = "INSERT INTO user (username,password,email) VALUES ('{}','{}','{}')".format(username,password,email)
    connect_cursor.execute(sql)
    connect_sql.commit()

# 检查用户名是否正确~
def check_username(username):
    sql = "SELECT username FROM user WHERE username='{}'".format(username)
    connect_cursor.execute(sql)
    fetchall = connect_cursor.fetchall()
    for i in fetchall:
        return i[0]

# 检查密码是否正确~
def check_password(username,password):
    md5 = hashlib.md5()
    md5.update((str(username) + str(password) + "guess*number").encode())
    sql = "SELECT password FROM user WHERE password='{}'".format(md5.hexdigest())
    connect_cursor.execute(sql)
    fetchall = connect_cursor.fetchall()
    for i in fetchall:
        return i[0]

# 通过email查找用户名和密码,有就返回元组,没有则返回None~
def check_email_password(email):
    if check_email(email) != None:
        sql = "SELECT username,password FROM user WHERE email='{}'".format(email)
        connect_cursor.execute(sql)
        fetchall = connect_cursor.fetchall()
        for i in fetchall:
            return i
    else:
        pass

# 查找email,没有则返回None~
def check_email(email):
    sql = "SELECT email FROM user WHERE email='{}'".format(email)
    connect_cursor.execute(sql)
    fetchall = connect_cursor.fetchall()
    for i in fetchall:
        return i[0]

# 通过email查询用户名,如果没有则返回None~
def get_username(email):
    sql = "SELECT username FROM user WHERE email='{}'".format(email)
    connect_cursor.execute(sql)
    fetchall = connect_cursor.fetchall()
    for i in fetchall:
        return i[0]

# 忘记密码时,利用用户名和邮箱来判断是否可以修改密码~
def check_forget_pass(username,email):
    sql = "SELECT * FROM user WHERE username='{}' and email='{}'".format(username,email)
    connect_cursor.execute(sql)
    fetchall = connect_cursor.fetchall()
    for i in fetchall:
        return i

def change_pass(new_pass,username,email):
    sql = "UPDATE user SET password='{}' WHERE username='{}' and email='{}'".format(new_pass,username,email)
    connect_cursor.execute(sql)
    connect_sql.commit()


# print(check_password("1473018671@qq.com","123456s"))
# md5 = hashlib.md5()
# md5.update((str(check_email_password("123456@qq.com")[0]) + str("123456s") + "guess*number").encode())
# print(check_email_password("123456@qq.com")[1] == md5.hexdigest())
# print(get_username("1473018671@qq.com"))
# print(check_forget_pass("Crazy","1473018671@qq.com"))
