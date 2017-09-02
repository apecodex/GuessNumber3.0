import pymysql

class MySQL():

	def __init__(self):
		self.username = "root"
		self.password = "crazyrookie"
		self.host = "127.0.0.1"
		self.port = 3306

	def sava(self,username,password,email):
		self.connect_sql = pymysql.connect(user=self.username,password=self.password,host=self.host,port=self.port)
		self.connect_cursor = self.connect_sql.cursor()
		sql = """
			CREATE DATABASE IF NOT EXISTS guessnumber DEFAULT CHARACTER SET utf8;
			USE guessnumber;

			CREATE TABLE IF NOT EXISTS user(
				username VARCHAR(50),
				password VARCHAR(88),
				email VARCHAR(88)
			);
			"""
		self.connect_cursor.execute(sql)
		self.connect_sql.commit()

		sql = "INSERT INTO user (username,password,email) VALUES ('{}','{}','{}')".format(username,password,email)
		self.connect_cursor.execute(sql)
		self.connect_sql.commit()


if __name__ == "__main__":
	MySQL().sava("a","A","adasd")