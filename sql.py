import pymysql

def sava(username,password,email):
	connect_sql = pymysql.connect(user="root",password="crazyrookie",host="127.0.0.1",port=3306)
	connect_cursor = connect_sql.cursor()
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

