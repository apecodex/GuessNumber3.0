from tkinter import *
from tkinter import messagebox
import hashlib
import sql
import os
import re

class Login():

    def __init__(self):
        self.windows = Tk()

    def hash(self,username,password):
        md5 = hashlib.md5()
        md5.update((str(username)+str(password)+"guess*number").encode())
        return md5.hexdigest()

    def check_input_is_ok(self):
        # print(self.var_username.get().strip() == "")
        if self.var_username.get().strip() == "":
            messagebox.showinfo(title="提示:", message="抱歉,请输入用户名~")
        elif self.var_password.get().strip() == "":
            messagebox.showinfo(title="提示:", message="抱歉,请输入密码~")
        elif self.var_againpassword.get().strip() == "":
            messagebox.showinfo(title="提示:",message="抱歉,请确认密码~")
        elif self.var_password.get() != self.var_againpassword.get():
            messagebox.showinfo(title="提示:",message="抱歉,两次密码不统一,请检查~")
        elif self.var_email.get().strip() == "" or self.var_email.get() == "example@email.com":
            messagebox.showinfo(title="提示:", message="抱歉,请输入邮箱地址~")
        elif self.var_username.get()[0].isspace() == True or self.var_username.get()[-1].isspace() or len(self.var_username.get().split()) != 1 or self.var_username.get()[0].isdigit() == True:
            messagebox.showinfo(title="提示:", message="抱歉用户名格式不对,请检查~(合法格式例如:hello_123 or hello123 and @hello123)")
        elif len(self.var_password.get()) <= 6 or  [i for i in self.var_password.get() if i.isalpha()] == []:
            messagebox.showinfo(title="提示:",message="抱歉,密码太弱,请输入6位数以上且带有一个字母~")
        elif re.findall(r'[^a-z0-9]+',self.var_email.get().split("@")[0]) != [] or self.var_email.get().split("@")[-1] not in ["qq.com","gmail.com","163.com"]:
            messagebox.showinfo(title="提示:",message="抱歉,邮箱地址不正确,请检查~")
        else:
            messagebox.showinfo(title="提示:",message="用户名'{}',创建成功！快去登录试试吧~~".format(self.var_username.get()))
            passmd5 = self.hash(self.var_username.get(),self.var_password.get())
            sql.sava(self.var_username.get(),passmd5,self.var_email.get())

    def user_login(self):
        if self.var_name_input.get() == "Crazy":    # 检查用户名是否在数据库
            if not self.var_pass_input.get():
                messagebox.showinfo(title="提示:", message="Sorry,password not null~")
            elif self.var_pass_input.get() != "123":
                messagebox.showinfo(title="提示:", message="Sorry,password error~please try again")
            else:
                messagebox.showinfo(title="提示:", message="Welcome,How are you~ "+self.var_name_input.get())
                self.windows.destroy()
                Gamemain().main(self.var_name_input.get())
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
        self.sgin_up_windows.maxsize("600","300")
        self.sgin_up_windows.minsize("600","300")
        self.sgin_up_windows.title("Sgin Up")
        self.sgin_up_windows.config(bg="#222")
        username = Label(self.sgin_up_windows,text="New Username:",font=("宋体",20),bg="#222").place(x=25,y=20)
        password = Label(self.sgin_up_windows,text="Password:",font=("宋体",20),bg="#222").place(x=95,y=70)
        passagain = Label(self.sgin_up_windows,text="Again Password:",font=("宋体",20),bg="#222").place(x=17,y=120)
        email = Label(self.sgin_up_windows,text="Email:",font=("宋体",20),bg="#222").place(x=147,y=170)
        self.var_username = StringVar()
        self.var_password = StringVar()
        self.var_againpassword = StringVar()
        self.var_email = StringVar()
        self.var_email.set("example@email.com")
        inname = Entry(self.sgin_up_windows,font=("宋体",20,),bg="#333",relief="solid",textvariable=self.var_username)
        inname.place(x=240,y=20)
        inpass = Entry(self.sgin_up_windows,font=("宋体",20),bg="#333",relief="solid",textvariable=self.var_password)
        inpass.place(x=240,y=70)
        againpass = Entry(self.sgin_up_windows,font=("宋体",20),bg="#333",relief="solid",textvariable=self.var_againpassword)
        againpass.place(x=240,y=120)
        inemail = Entry(self.sgin_up_windows,font=("宋体",20),bg="#333",relief="solid",textvariable=self.var_email)
        inemail.place(x=240,y=170)
        btn = Button(self.sgin_up_windows,text=" Sgin ",font=("宋体",20),bg="#222",relief="solid",command=self.check_input_is_ok).place(x=430,y=230)

    def main(self):
        ws = self.windows.winfo_screenwidth()
        hs = self.windows.winfo_screenheight()
        w = 800
        h = 500
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.windows.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.windows.maxsize("800","500")
        self.windows.minsize("800","500")
        self.windows.title("Python Guess Number Game (V3.0)")
        self.windows.config(bg="#222")
        if os.name == "posix":
            pass
        else:
            self.windows.overrideredirect(True)
            exit_btn = Button(self.windows, text="Exit", command=self.windows.quit, relief="g", fg="#FFFFFF").place(
                x=750, y=0)
        image = PhotoImage(file="Welcome.png")
        img = Label(self.windows,image=image,width=600,bg="#222").place(x=130,y=-30)
        usename = Label(self.windows,text="username",font=("宋体",30),fg="#888",bg="#222").place(x=80,y=200)
        password = Label(self.windows,text="password",font=("宋体",30),fg="#888",bg="#222").place(x=80,y=300)
        self.var_name_input = StringVar()
        self.var_name_input.set("example@email.com")
        inname = Entry(self.windows,textvariable=self.var_name_input,font=("宋体",30),relief="solid",bg="#222")
        inname.place(x=300,y=200)
        self.var_pass_input = StringVar()
        inpass = Entry(show="❤",textvariable=self.var_pass_input,font=("宋体",30),relief="solid",bg="#222")
        inpass.place(x=300,y=300)
        btn = Button(self.windows,text="Login",command=self.user_login,font=("宋体",20),relief="g",bg="#222").place(x=300,y=400)
        btn = Button(self.windows, text="Sign up", command=self.user_sign_up, font=("宋体", 20),relief="g",bg="#222").place(x=500, y=400)
        version = Label()
        self.windows.mainloop()


class Gamemain():

    def __init__(self):
        self.gamewindows = Tk()
        self.usename = ""
        self.password = ""

    def main(self,username):
        ws = self.gamewindows.winfo_screenwidth()
        hs = self.gamewindows.winfo_screenheight()
        w = 900
        h = 600
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.gamewindows.geometry("%dx%d+%d+%d" % (w,h,x,y))
        self.gamewindows.title("Python Guess Number Game (V3.0)")
        self.gamewindows.config(bg="#222")
        Label(self.gamewindows,text=username).pack()
        self.gamewindows.mainloop()


if "__main__" == __name__:
    L = Login()
    L.main()
