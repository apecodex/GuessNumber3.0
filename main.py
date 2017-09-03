from tkinter import *
from tkinter import messagebox
import hashlib
import sql

class Login():

	def __init__(self):
		self.windows = Tk()

	def hash(self,username,password):
		md5 = hashlib.md5()
		md5.update((str(username)+str(password)+"guess*number").encode())
		return md5.hexdigest()

	def check_input_is_ok(self):
		if self.var_username.get().isspace():
			# messagebox.showinfo(title="提示:", message="Sorry,username not null~~")
			tishi = Label(self.sgin_up_windows,text="No",font=("宋体",20)).place(x=300,y=300)
		elif self.var_password.get().isspace():
			# messagebox.showinfo(title="提示:", message="Sorry,password not null~~")
			pass
		elif self.var_email.get().isspace() or self.var_email.get() == "example@email.com":
			# messagebox.showinfo(title="提示:", message="Sorry,email not null~~")
			pass

			passmd5 = self.hash(self.var_username.get(),self.var_password.get())
		# sql.sava(self.var_username.get(),passmd5,self.var_email.get())

	def user_login(self):
		if self.var_name_input.get() == "Crazy":    # 检查用户名是否在数据库
			if not self.var_pass_input.get():
				messagebox.showinfo(title="提示:", message="Sorry,password not null~")
			elif self.var_pass_input.get() != "123":
				messagebox.showinfo(title="提示:", message="Sorry,password error~please try again")
			else:
				messagebox.showinfo(title="提示:", message="Welcome,How are you~ "+self.var_name_input.get())
				self.windows.destroy()
				Gamemain(self.var_name_input.get())
		else:
			tf = messagebox.askyesno(title="提示:", message="Sorry,username not exists~Sgin Up?")
			if tf == True:
				self.user_sign_up()

	def user_sign_up(self):
		self.sgin_up_windows = Toplevel(self.windows)
		ws = self.windows.winfo_screenwidth()
		hs = self.windows.winfo_screenheight()
		w = 600
		h = 300
		x = (ws / 2) - (w / 2)
		y = (hs / 2) - (h / 2)
		self.sgin_up_windows.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.sgin_up_windows.title("Sgin Up")
		username = Label(self.sgin_up_windows,text="New Username:",font=("宋体",20)).place(x=47,y=20)
		password = Label(self.sgin_up_windows,text="Password:",font=("宋体",20)).place(x=103,y=70)
		passagain = Label(self.sgin_up_windows,text="Again Password:",font=("宋体",20)).place(x=20,y=120)
		email = Label(self.sgin_up_windows,text="Email:",font=("宋体",20)).place(x=146,y=170)
		self.var_username = StringVar()
		self.var_password = StringVar()
		self.var_againpassword = StringVar()
		self.var_email = StringVar()
		self.var_email.set("example@email.com")
		inname = Entry(self.sgin_up_windows,font=("宋体",20),textvariable=self.var_username)
		inname.place(x=250,y=20)
		inpass = Entry(self.sgin_up_windows,font=("宋体",20),textvariable=self.var_password)
		inpass.place(x=250,y=70)
		againpass = Entry(self.sgin_up_windows,font=("宋体",20),textvariable=self.var_againpassword)
		againpass.place(x=250,y=120)
		inemail = Entry(self.sgin_up_windows,font=("宋体",20),textvariable=self.var_email)
		inemail.place(x=250,y=170)
		btn = Button(self.sgin_up_windows,text=" Sgin ",font=("宋体",20),relief="solid",command=self.check_input_is_ok).place(x=430,y=230)

	def main(self):
		ws = self.windows.winfo_screenwidth()
		hs = self.windows.winfo_screenheight()
		w = 900
		h = 600
		x = (ws / 2) - (w / 2)
		y = (hs / 2) - (h / 2)
		self.windows.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.windows.title("Python Guess Number Game (V3.0)")
		self.windows.overrideredirect(True)
		image = PhotoImage(file="Welcome.png")
		img = Label(self.windows,image=image).place(x=170,y=0)
		usename = Label(self.windows,text="username",font=("宋体",30),fg="#682").place(x=150,y=300)
		password = Label(self.windows,text="password",font=("宋体",30),fg="#682").place(x=150,y=400)
		self.var_name_input = StringVar()
		self.var_name_input.set("example@email.com")
		inname = Entry(self.windows,textvariable=self.var_name_input,font=("宋体",30),relief="solid")
		inname.place(x=350,y=300)
		self.var_pass_input = StringVar()
		inpass = Entry(show="❤",textvariable=self.var_pass_input,font=("宋体",30),relief="solid")
		inpass.place(x=350,y=400)
		btn = Button(self.windows,text="Login",command=self.user_login,font=("宋体",20),relief="g").place(x=300,y=500)
		btn = Button(self.windows, text="Sign up", command=self.user_sign_up, font=("宋体", 20),relief="g").place(x=500, y=500)
		exit_btn = Button(self.windows,text="Exit",command=self.windows.quit,relief="g",fg="#FFFFFF").place(x=860,y=10)
		version = Label()
		self.windows.mainloop()


class Gamemain():

	def	__init__(self,username):
		self.windows1 = Tk()
		self.windows1.geometry("900x600")
		self.windows1.maxsize("1000","900")
		self.windows1.minsize("1000","900")
		Label(self.windows1,text=username).pack()
		self.windows1.mainloop()


if "__main__" == __name__:
	L = Login()
	L.main()
