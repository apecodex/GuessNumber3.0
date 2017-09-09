from tkinter import *
from tkinter import messagebox
import hashlib
import sql
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random

class Login():

    def __init__(self):
        self.windows = Tk()

    # 加密密码
    def hash(self,username,password):
        md5 = hashlib.md5()
        md5.update((str(username)+str(password)+"guess*number").encode())
        return md5.hexdigest()

    # 匹配email地址
    def check_email_is_ok(self,email):
        pattern = re.compile(r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')
        return pattern.search(email)

    # 发送邮箱验证码
    def send_email(self,email,name):
        self.randomslist = "".join(list(map(str, random.sample(range(1, 10), 5))))
        serder = "2905217710@qq.com"
        receiver = email
        smtp_server = "smtp.qq.com"
        username = "2905217710@qq.com"
        password = "cswqzrqkhzzkdgjg"
        msg = MIMEText("验证码:{}".format(self.randomslist), 'plain', 'utf-8')
        msg['From'] = serder
        msg['To'] = receiver
        msg['Subject'] = Header(u"Hello {}".format(name), "utf-8").encode()
        smtp = smtplib.SMTP_SSL(smtp_server, 465)
        smtp.login(username, password)
        smtp.sendmail(serder, receiver, msg.as_string())
        print(self.randomslist)

    # 发送邮箱验证码
    def sgin_send_email(self):
        if self.var_email.get().strip() == "" or self.var_email.get() == "example@email.com":
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,你还没输入邮箱呐~")
        else:
            if sql.check_email(self.var_email.get()) != None:
                self.information_text.delete(0, END)
                self.information_text.insert(END, "抱歉,此邮箱已被注册~")
            elif self.check_email_is_ok(self.var_email.get()) == None:
                self.information_text.delete(0, END)
                self.information_text.insert(END, "抱歉,邮箱地址错误")
            else:
                self.send_email(self.var_email.get(),self.var_username.get())
                self.information_text.delete(0, END)
                self.information_text.insert(END, "已成功发送,请打开邮箱查看验证码~")
                self.information_text.config(fg="#FFF")

    # 检测输入的是否合法~
    def check_input_is_ok(self):
        # print(self.var_username.get().strip() == "")
        if self.var_username.get().strip() == "":
            self.information_text.delete(0,END)
            self.information_text.insert(END,"抱歉,请输入用户名~")
        elif self.var_password.get().strip() == "":
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,请输入密码~")
        elif self.var_againpassword.get().strip() == "":
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,请确认密码~")
        elif self.var_password.get() != self.var_againpassword.get():
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,两次密码不统一,请检查~")
        elif self.var_email.get().strip() == "" or self.var_email.get() == "example@email.com":
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,请输入邮箱地址~")
        elif self.var_username.get()[0].isspace() == True or self.var_username.get()[-1].isspace() or len(self.var_username.get().split()) != 1 or self.var_username.get()[0].isdigit() == True:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,用户名格式不对,请检查~(合法格式例如:hello_123 or hello123 and @hello123)")
        elif len(self.var_password.get()) <= 6 or  [i for i in self.var_password.get() if i.isalpha()] == []:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,密码太弱,请输入6位数以上且带有一个字母~")
        elif self.check_email_is_ok(self.var_email.get()) == None:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,邮箱地址不正确,请检查~")
        elif sql.check_username(self.var_username.get()) != None:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,用户名已存在~")
        elif sql.check_email(self.var_email.get()) != None:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "抱歉,此邮箱已被注册~")
        elif self.var_verification_code.get().strip() == "":
            self.information_text.delete(0, END)
            self.information_text.insert(END, "请输入验证码~")
        elif self.var_verification_code.get() != self.randomslist:
            self.information_text.delete(0, END)
            self.information_text.insert(END, "验证码错误~")
        else:
            passmd5 = self.hash(self.var_username.get(),self.var_password.get())
            sql.sava(self.var_username.get(),passmd5,self.var_email.get())
            messagebox.showinfo(title="提示:", message="用户名'{}',创建成功！快去登录试试吧~~".format(self.var_username.get()))
    # 登录页面
    def user_login(self):
        if self.var_name_input.get() == sql.check_username(self.var_name_input.get()) or self.var_name_input.get() == sql.check_email(self.var_name_input.get()):    # 检查用户名是否在数据库
            if not self.var_pass_input.get():
                messagebox.showinfo(title="提示:", message="抱歉,请输入密码~")
            else:
                if self.check_email_is_ok(self.var_name_input.get()) != None:
                    if self.hash(sql.check_email_password(self.var_name_input.get())[0],self.var_pass_input.get()) != sql.check_password(sql.check_email_password(self.var_name_input.get())[0],self.var_pass_input.get()):
                        messagebox.showinfo(title="提示:", message="抱歉,密码错误,请重新输入~")
                    else:
                        messagebox.showinfo(title="提示:", message="Welcome,How are you~ " + sql.get_username(self.var_name_input.get()))
                        self.windows.destroy()
                        Gamemain().main(sql.get_username(self.var_name_input.get()))
                else:
                    if sql.check_password(self.var_name_input.get(),self.var_pass_input.get()) == None:
                        messagebox.showinfo(title="提示:", message="抱歉,密码错误,请重新输入~")
                    else:
                        messagebox.showinfo(title="提示:", message="Welcome,How are you~ " + self.var_name_input.get())
                        self.windows.destroy()
                        Gamemain().main(self.var_name_input.get())
        else:
            tf = messagebox.askyesno(title="提示:", message="Sorry,username not exists~Sgin Up?")
            if tf == True:
                self.user_sign_up()
    # 注册页面
    def user_sign_up(self):
        self.sgin_up_windows = Toplevel(self.windows)
        ws = self.windows.winfo_screenwidth()
        hs = self.windows.winfo_screenheight()
        w = 600
        h = 450
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.sgin_up_windows.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.sgin_up_windows.maxsize("600","450")
        self.sgin_up_windows.minsize("600","450")
        self.sgin_up_windows.title("Sgin Up")
        self.sgin_up_windows.config(bg="#222")
        Label(self.sgin_up_windows,text="Sgin Up",font=("楷体",60),bg="#222",fg="#fbd").pack(side="bottom")
        username = Label(self.sgin_up_windows,text="New Username:",font=("宋体",20),bg="#222").place(x=25,y=20)
        password = Label(self.sgin_up_windows,text="Password:",font=("宋体",20),bg="#222").place(x=95,y=70)
        passagain = Label(self.sgin_up_windows,text="Again Password:",font=("宋体",20),bg="#222").place(x=17,y=120)
        email = Label(self.sgin_up_windows,text="Email:",font=("宋体",20),bg="#222").place(x=147,y=170)
        self.varification_code = Label(self.sgin_up_windows,text="Code:",font=("宋体",25),bg="#222").place(x=150,y=240)
        self.var_username = StringVar()
        self.var_password = StringVar()
        self.var_againpassword = StringVar()
        self.var_email = StringVar()
        self.var_verification_code = StringVar()
        self.var_text = StringVar()
        self.var_email.set("example@email.com")
        inname = Entry(self.sgin_up_windows,font=("宋体",20,),bg="#333",relief="solid",textvariable=self.var_username)
        inname.place(x=240,y=20)
        inpass = Entry(self.sgin_up_windows,font=("宋体",20),bg="#333",relief="solid",textvariable=self.var_password,show="*")
        inpass.place(x=240,y=70)
        againpass = Entry(self.sgin_up_windows,font=("宋体",20),bg="#333",relief="solid",textvariable=self.var_againpassword,show="*")
        againpass.place(x=240,y=120)
        inemail = Entry(self.sgin_up_windows,font=("宋体",20),bg="#333",relief="solid",textvariable=self.var_email)
        inemail.place(x=240,y=170)
        inverification_code = Entry(self.sgin_up_windows,font=("宋体",25),insertbackground="#000",width=5,bg="#333",relief="solid",textvariable=self.var_verification_code)
        inverification_code.place(x=240,y=240)
        code_btn = Button(self.sgin_up_windows,font=("宋体",12),text="发送",bg="#222",width=6,relief="solid",command=self.sgin_send_email).place(x=530,y=170)
        btn = Button(self.sgin_up_windows,text=" Sgin ",font=("宋体",20),bg="#222",relief="solid",command=self.check_input_is_ok,activebackground="#222").place(x=430,y=230)
        self.information_text = Listbox(self.sgin_up_windows,bg="#222",fg="red",width=45,height=1,font=("微软雅黑",15))
        self.information_text.place(x=30, y=300)

    # 检查新修改的密码是否ok
    def check_new_pass_is_ok(self):
        if self.new_pass.get().strip() == "":
            # messagebox.showinfo(title="提示", message="抱歉,请输入密码~")
            self.change_pass_text.delete(0, END)
            self.change_pass_text.insert(END, "抱歉,请输入密码~")
        elif self.agagin_pass.get().strip() == "":
            # messagebox.showinfo(title="提示",message="抱歉,请确认密码~please agagin~")
            self.change_pass_text.delete(0, END)
            self.change_pass_text.insert(END, "抱歉,请确认密码~please agagin~")
        elif self.new_pass.get() != self.agagin_pass.get():
            # messagebox.showinfo(title="提示",message="抱歉,两次输入的密码不相同~")
            self.change_pass_text.delete(0, END)
            self.change_pass_text.insert(END, "抱歉,两次输入的密码不相同~")
        elif len(self.new_pass.get()) <= 6 or [i for i in self.new_pass.get() if i.isalpha()] == []:
            # messagebox.showinfo(title="提示:",message="抱歉,密码太弱,请输入6位数以上且带有一个字母~")
            self.change_pass_text.delete(0, END)
            self.change_pass_text.insert(END, "抱歉,密码太弱,请输入6位数以上且带有一个字母~~")
        else:
            sql.change_pass(self.hash(self.forget_name.get(),self.new_pass.get()),self.forget_name.get(),self.forget_email.get())
            # messagebox.showinfo(title="提示",message=" 修改成功!   ")
            self.change_pass_text.delete(0, END)
            self.change_pass_text.config(fg="#FFF")
            self.change_pass_text.insert(END, "修改成功!")

    def forget_send_email(self):
        if sql.check_email(self.forget_email.get()) == None:
            self.find_text.delete(0, END)
            self.find_text.insert(END, "邮箱不存在~")
        else:
            self.send_email(self.forget_email.get(),self.forget_name.get())
            self.find_text.delete(0,END)
            self.find_text.config(fg="#FFF")
            self.find_text.insert(END,"验证码已发送，请查看邮箱~")

    # 更改密码
    def change_password(self):
        if self.var_name_input.get().strip() == "":
            self.find_text.delete(0, END)
            self.find_text.insert(END, "用户名不得为空~")
        elif sql.check_forget_pass(self.forget_name.get(),self.forget_email.get()) == None:
            self.find_text.delete(0,END)
            self.find_text.insert(END,"用户名不存在或邮箱错误~")
        elif self.find_code.get().strip() == "":
            self.find_text.delete(0, END)
            self.find_text.insert(END, "验证码不得为空~")
        elif self.find_code.get() != self.randomslist:
            self.find_text.delete(0, END)
            self.find_text.insert(END, "验证码错误~")
        else:
            self.change_pass_windows = Toplevel(self.windows)
            ws = self.change_pass_windows.winfo_screenwidth()
            hs = self.change_pass_windows.winfo_screenheight()
            w = 450
            h = 300
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)
            self.change_pass_windows.geometry("%dx%d+%d+%d" % (w,h,x,y))
            self.change_pass_windows.config(bg="#222")
            self.change_pass_windows.maxsize("450","300")
            self.change_pass_windows.minsize("450","300")
            self.change_pass_windows.title("Change Password~")
            icon = Label(self.change_pass_windows,text="Change Password",font=("微软雅黑",30),bg="#222",fg="#568").pack()
            new_pass_label = Label(self.change_pass_windows,text="New Password",font=("楷体",15),bg="#222").place(x=30,y=100)
            agagin_pass_label = Label(self.change_pass_windows,text="Again Password",font=("楷体",15),bg="#222").place(x=20,y=150)
            self.new_pass = StringVar()
            self.agagin_pass = StringVar()
            new_pass_btn = Entry(self.change_pass_windows,show="*",font=("楷体",15),relief="solid",bg="#222",textvariable=self.new_pass)
            new_pass_btn.place(x=190,y=100)
            agagin_pass_btn = Entry(self.change_pass_windows,show="*",font=("楷体",15),relief="solid",bg="#222",textvariable=self.agagin_pass)
            agagin_pass_btn.place(x=190,y=150)
            btn = Button(self.change_pass_windows,text="确认",font=("楷体",10),relief="solid",activebackground="#222",bg="#222",command=self.check_new_pass_is_ok).place(x=380,y=250)
            self.change_pass_text = Listbox(self.change_pass_windows,bg="#222",fg="red",width=30,height=1,font=("微软雅黑",15))
            self.change_pass_text.place(x=50,y=200)

    # 忘记密码
    def forget_password(self):
        self.forget_pass_windows = Toplevel(self.windows)
        ws = self.forget_pass_windows.winfo_screenwidth()
        hs = self.forget_pass_windows.winfo_screenheight()
        w = 600
        h = 300
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.forget_pass_windows.geometry("%dx%d+%d+%d" % (w,h,x,y))
        self.forget_pass_windows.maxsize("600","300")
        self.forget_pass_windows.minsize("600","300")
        self.forget_pass_windows.title("Forget Password")
        self.forget_pass_windows.config(bg="#222")
        labelname = Label(self.forget_pass_windows,text="Username",bg="#222",font=("微软雅黑",20)).place(x=50,y=50)
        labelemail = Label(self.forget_pass_windows,text="Email",bg="#222",font=("微软雅黑",20)).place(x=110,y=120)
        self.find_inverification_code = Label(self.forget_pass_windows,text="Code",bg="#222",font=("微软雅黑",20)).place(x=110,y=190)
        self.forget_name = StringVar()
        self.forget_email = StringVar()
        self.find_code = StringVar()
        if self.var_name_input.get() == "example@email.com":
            pass
        elif self.check_email_is_ok(self.var_name_input.get()):
            self.forget_email.set(self.var_name_input.get())
        elif self.var_name_input.get().split("@")[-1] not in ["qq.com", "gmail.com", "163.com"]:
            self.forget_name.set(self.var_name_input.get())
        else:
            pass
        inname = Entry(self.forget_pass_windows,textvariable=self.forget_name,font=("微软雅黑",20),bg="#222",relief="solid")
        inname.place(x=200,y=50)
        inemail = Entry(self.forget_pass_windows,textvariable=self.forget_email,font=("微软雅黑",20),bg="#222",relief="solid")
        inemail.place(x=200,y=120)
        find_inverification_code = Entry(self.forget_pass_windows,textvariable=self.find_code,font=("微软雅黑",20),bg="#222",relief="solid",width=5)
        find_inverification_code.place(x=200,y=190)
        find_btn = Button(self.forget_pass_windows,text="更改密码",font=("微软雅黑",15),relief="solid",activebackground="#222",bg="#222",fg="#FFF",command=self.change_password).place(x=450,y=180)
        find_code_btn = Button(self.forget_pass_windows,text="发送",font=("微软雅黑",10),relief="solid",activebackground="#222",bg="#222",fg="#FFF",command=self.forget_send_email).place(x=300,y=190)
        self.find_text = Listbox(self.forget_pass_windows,bg="#222",fg="red",width=30,height=1,font=("微软雅黑",15))
        self.find_text.place(x=50,y=250)

    def main(self):
        ws = self.windows.winfo_screenwidth()   # 获取显示器显示的宽度
        hs = self.windows.winfo_screenheight()   # 获取显示器显示的高度
        w = 800
        h = 500
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.windows.geometry('%dx%d+%d+%d' % (w, h, x, y))    # 在显示器中心出现
        self.windows.maxsize("800","500")
        self.windows.minsize("800","500")
        self.windows.title("Python Guess Number Game (V3.0)")
        self.windows.config(bg="#222")
        if os.name == "posix":    # 因为在Linux环境中,overrideredirect无法正常使用Entry和Button,还会导致卡死
            pass
        else:
            self.windows.overrideredirect(True)    # 去除边框
            exit_btn = Button(self.windows, text="Exit", command=self.windows.quit, relief="g", fg="#FFFFFF",bg="#222").place(
                x=10, y=0)    # Windows环境下使用了overrideredirect之后就没有边框了,自己弄一个退出按钮~
        image = PhotoImage(file="Welcome.png")    # 设置欢迎界面
        img = Label(self.windows,image=image,width=700,bg="#222").place(x=130,y=-30)
        usename = Label(self.windows,text="username",font=("宋体",30),fg="#888",bg="#222").place(x=80,y=200)
        password = Label(self.windows,text="password",font=("宋体",30),fg="#888",bg="#222").place(x=80,y=300)
        self.var_name_input = StringVar()
        self.var_name_input.set("example@email.com")
        inname = Entry(self.windows,textvariable=self.var_name_input,font=("宋体",30),relief="solid",bg="#222")
        inname.place(x=300,y=200)
        self.var_pass_input = StringVar()
        inpass = Entry(show="❤",textvariable=self.var_pass_input,font=("宋体",30),relief="solid",bg="#222")
        inpass.place(x=300,y=300)
        forget_pass_btn = Button(self.windows,text="forget password?",font=("楷体",10),relief="solid",bg="#222",fg="#FFF",command=self.forget_password,activebackground="#222").place(x=580,y=350)
        btn = Button(self.windows,text="Login",command=self.user_login,font=("宋体",20),relief="g",bg="#222",fg="#fff",activebackground="#222").place(x=300,y=400)
        btn = Button(self.windows, text="Sign up", command=self.user_sign_up, font=("宋体", 20),relief="g",bg="#222",fg="#fff",activebackground="#222").place(x=500, y=400)
        version = Label()
        self.windows.mainloop()

# 游戏界面
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
        Label(self.gamewindows,text="欢迎您~"+username).pack()
        self.gamewindows.mainloop()


if "__main__" == __name__:
    L = Login()
    L.main()
