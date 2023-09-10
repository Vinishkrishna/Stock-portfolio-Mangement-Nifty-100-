from tkinter import*
from tkinter import messagebox
from subprocess import call
import ast

root=Tk()
root.title('Login')
root.iconbitmap(r'C:\Users\R VINISH KRISHNA\Desktop\Login\stock-market.ico')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

def sign_in(username):
    username=user.get()
    password=code.get()
    file=open('datasheet.txt','r')
    d=file.read()
    r=ast.literal_eval(d)
    file.close()

    if username in r.keys() and password==r[username]:
        call(['python','ui_labels.py',username])
        root.destroy()
    else:
        messagebox.showerror('Invalid','invalid username or password')


def signup_command():
    window=Toplevel(root)
    window.title("SignUp")
    window.iconbitmap(r'C:\Users\R VINISH KRISHNA\Desktop\Stock Management\SignUp\stock-market.ico')
    window.geometry("925x500+300+200")
    window.configure(bg='#fff')
    window.resizable(False,False)

    def signup():
        username=user.get()
        password=code.get()
        confirm_password=confirm_code.get()
    
        if(len(username)>=6 and len(password)>=6):
            if password==confirm_password:
                    file=open("datasheet.txt","r+")
                    d=file.read()
                    r=ast.literal_eval(d)
                    if (username.lower() not in r.keys()):
                        dict2={username:password}
                        r.update(dict2)
                        file.truncate(0)
                        file.close()
                        file=open("datasheet.txt","w")
                        file.write(str(r))

                        messagebox.showinfo("Signup","Sucessfully sign up")
                        window.destroy()
                    else:
                        messagebox.showinfo("Signup","Username already present-Please try another one")
                        window.destroy()    
            else:
                messagebox.showerror("Invalid","Both Password should match")
        else:
            messagebox.showerror("Invalid","Please enter characters of atleast 6 ")

    def sign():
        window.destroy()

    img = PhotoImage(file="signup.png")
    Label(window,image=img,border=0,bg='white').place(x=50,y=90)

    frame=Frame(window,width=350,height=390,bg='#fff')
    frame.place(x=480,y=50)

    heading=Label(frame,text='Sign up',fg="#57a1f8",bg='white',font=("Microsoft Yahei UI Light",23,"bold"))
    heading.place(x=100,y=5)

##########
    def on_enter(e):
        user.delete(0,'end')

    def on_leave(e):
        if user.get()=="":
           user.insert(0,"Username")

    user = Entry(frame,width=25, fg="black",border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    user.place(x=30, y=80)
    user.insert(0,'Username')
    user.bind("<FocusIn>",on_enter)
    user.bind("<FocusOut>", on_leave)

    Frame(frame,width=295, height=2, bg="black").place(x=25,y=107)

##########
    def on_enter(e):
        code.delete(0,'end')

    def on_leave(e):
        if code.get()=="":
           code.insert(0,"Password")

    code= Entry(frame,width=25, fg="black",border=0,bg='white',font=('Microsoft Yahei UI Light',11),show='*')
    code.place(x=30,y=150)
    code.insert(0,'Password')
    code.bind("<FocusIn>",on_enter)
    code.bind("<FocusOut>", on_leave)

    Frame(frame,width=295, height=2, bg="black").place(x=25,y=177)
########
    def on_enter(e):
        confirm_code.delete(0,'end')

    def on_leave(e):
        if confirm_code.get()=="":
           confirm_code.insert(0,"Confirm Password")

    confirm_code= Entry(frame,width=25, fg="black",border=0,bg='white',font=('Microsoft Yahei UI Light',11),show='*')
    confirm_code.place(x=30,y=220)
    confirm_code.insert(0,'Confirm Password')
    confirm_code.bind("<FocusIn>",on_enter)
    confirm_code.bind("<FocusOut>", on_leave)

    Frame(frame,width=295, height=2, bg="black").place(x=25,y=247)
#######----
    Button(frame,width=39, pady=7,text="Sign up",bg="#57a1f8",fg="white",border=0,command=signup).place(x=35,y=280)
    label=Label(frame,text="I have an account",fg='black',bg="white",font=("Microsoft YaHei UI Light",9))
    label.place(x=90, y=340)

    signin=Button(frame,width=6,text="Sign in",border=0,bg="white",cursor="hand2",fg="#57a1f8",command=sign)
    signin.place(x=200, y=340)
    window.mainloop()
######@@@@@@@@@@@

img = PhotoImage(file='login.png')
Label(root, image=img, bg="white").place(x=50,y=50)
frame=Frame(root,width=350, height=350,bg="white")
frame.place(x=480,y=70)
heading=Label(frame, text= 'Sign in',fg='#57a1f8' ,bg='white',font=( 'Microsoft YaHei UI Light',23, 'bold'))
heading.place(x=100,y=5)
############------------------
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    name=user.get()
    if name=="":
        user.insert(0,'Username')

user = Entry(frame,width=25, fg= "black" ,border=0, bg= "white" ,font=( 'Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0 , 'Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)
Frame(frame,width=295,height=2,bg="black").place(x=25,y=107)
############------------------
def on_enter(e):
    code.delete(0,'end')
def on_leave(e):
    name=code.get()
    if name=="":
        code.insert(0,'Password')

code = Entry(frame,width=25, fg= "black" ,border=0, bg= "white" ,font=( 'Microsoft YaHei UI Light',11),show='*')
code.place(x=30,y=150)
code.insert(0 , 'Password')
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)
Frame(frame,width=295,height=2,bg="black").place(x=25,y=177)
#############################
username = ""
Button(frame, width=39, pady=7, text= 'Sign in' ,bg= '#57a1f8' ,fg= 'white' ,border=0,command=lambda: sign_in(username)).place(x=35,y=204)
label=Label(frame,text="Don't have an account?" ,fg= 'black' ,bg= 'white',font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=270)

sign_up= Button(frame,width=6, text= 'Sign up',border=0, bg= 'white' ,cursor='hand2',fg='#57a1f8',command=signup_command)
sign_up.place(x=215,y=270)

root.mainloop()