import tkinter as tk
from tkinter import ttk
from tkinter import *
import mysql.connector
from yahoo_fin import stock_info as si
import sys

username=sys.argv[1]
r= tk.Tk()
tree=ttk.Treeview(r)
i=0
symbols=[]
volume=[]
goal=["BUY","SELL"]
present=[]
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="stock_portfolio"
)
def add_stock(username,i):
    a=var.get()
    b=car.get()
    if (a in symbols) and (b in goal) and (a not in present):
        try:
            c=si.get_live_price(f"{a}.NS")
            tree.insert('', i, text="",values=(f"{a}",c,f"{volume[symbols.index(a)]}",f"{b}"),tags=["t1"])
            conn.execute(f"INSERT INTO watchlist_{username} (SYMBOL,VOLUME,GOAL) VALUES ('{a}',{volume[symbols.index(a)]},'{b}')")      
            present.append(a)
            mydb.commit()
        except:
            print("Exception")

def remove_stock():
    selected_item=tree.selection()[0]
    tree.delete(selected_item)

def taking_price(e):
    try:
        e=si.get_live_price(f"{ro[0]}.NS")
        return e
    except:
        print("Loading.....")
        taking_price(ro[0])

    # return si.get_live_price(f"{e}.NS")


conn = mydb.cursor()

conn.execute("SELECT*FROM COMPANY")

for ro in conn:
    symbols.append(ro[0])
    volume.append(ro[1])

conn.execute(f"SELECT*FROM watchlist_{username}")

for ro in conn:
    present.append(ro[0])
    ret=taking_price(ro[0])
    tree.insert('', i, text="",values=(ro[0],ret,ro[1],ro[2]),tags=["t1"])

r.title('View Watchlist')
r.iconbitmap(r'C:\Users\R VINISH KRISHNA\Desktop\Login\stock-market.ico')
screen_width = r.winfo_screenwidth()
screen_height = r.winfo_screenheight()
r.geometry("%dx%d+%d+%d" %(screen_width,screen_height,0,0))
r.configure(background="#EFBB96")
r.resizable(width=False, height=False)


var=StringVar()
car=StringVar()
combo=ttk.Combobox(r,values=symbols,textvariable=var)
combo.place(x=700,y=40,width=160,height=38)
combo=ttk.Combobox(r,values=goal,textvariable=car)
combo.place(x=880,y=40,width=160,height=38)
add_button=Button(r,text="Add Stock",bg="#48dcfa",command=lambda:add_stock(username,i))
add_button.place(x=580,y=38,width=100,height=40)
remove_button=Button(r,text="Delete",bg="#48dcfa",command=remove_stock)
remove_button.place(x=450,y=38,width=100,height=40)
label = Label(r,text="UPDATE WATCHLIST",font=("Ariel",14,"bold"),bd=4,bg='#A269F8',fg="white",relief="raised",width=17,height=1)
label.place(x=620, y=3)


tree['show'] ="headings"

s= ttk.Style(r)
s.theme_use("clam")

s.configure(".",font=('Helvetica',11))
s.configure("Treeview.Heading",foreground="red",font=("Helvetica",11,"bold"))
#Define number of columns
tree["columns"]=("SYMBOL","PRICE","VOLUME","GOAL")

#Assign the width,minwidth and anchor to the respective columns

tree.column("SYMBOL", width=50, minwidth=50, anchor=tk.CENTER)
tree.column("PRICE", width=100, minwidth=100,anchor=tk.CENTER)
tree.column("VOLUME", width=150, minwidth=150,anchor=tk.CENTER)
tree.column("GOAL", width=150, minwidth=150,anchor=tk.CENTER)

#Assign the heading names to the respective columns
tree.heading("SYMBOL", text="SYMBOL",anchor=tk.CENTER)
tree.heading("PRICE", text="PRICE", anchor=tk.CENTER)
tree.heading("VOLUME", text="VOLUME", anchor=tk.CENTER)
tree.heading("GOAL", text="GOAL", anchor=tk.CENTER)

#setting orientation and placing tree in a particular location.
hsb = ttk.Scrollbar(r,orient="horizontal")
hsb.configure(command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
tree.tag_configure("t1",background="#F264AB",foreground="green")
hsb.pack(fill=X,side=BOTTOM)
tree.place(x=0,y=120,width=screen_width-40,height=screen_height-200)
r.mainloop()
