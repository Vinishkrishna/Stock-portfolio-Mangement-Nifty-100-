from tkinter import *
from PIL import ImageTk, Image
from subprocess import call
from yahoo_fin import stock_info as si
import sys
import mysql.connector

root= Tk()
root.title('GrowUp Stock Management Website')
root.iconbitmap(r'C:\Users\R VINISH KRISHNA\Desktop\Login\stock-market.ico')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("%dx%d+%d+%d" %(screen_width,screen_height,0,0))
root.configure(background="#EFBB96")
root.resizable(width=False, height=False)
flag=0
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="stock_portfolio"
)
conn=mydb.cursor()

flag=0
try:
    top_gainers = si.get_day_gainers()[1:9][["Symbol","Price (Intraday)","% Change"]]
except:
    flag=1
    conn.execute(f"SELECT*FROM TOP_STOCKS")
    labela = Label(root,text="TOP STOCKS",font=("Ariel",14,"bold"),bd=4,bg='#A269F8',fg="white",relief="raised",width=17,height=3)
    labela.place(x=1180, y=80)
    ycor=180
    for ro in conn:
        label3 = Label(root,text=f"{ro[0]}",font=("Ariel",15,"bold"),bd=4,bg='#74db44',fg="white",relief="raised",width=30,height=2)
        label3.place(x=1100, y=ycor)
        ycor=ycor+80
    ycor=180
    

username=sys.argv[1]

conn.execute(f"CREATE TABLE IF NOT EXISTS amount_{username} (AMOUNT FLOAT)")
conn.execute(f"CREATE TABLE IF NOT EXISTS orders_{username} (ORDERS VARCHAR(255))")
conn.execute(f"CREATE TABLE IF NOT EXISTS portfolio_{username} (STOCKS VARCHAR(255),QUANTITY FLOAT)")
conn.execute(f"CREATE TABLE IF NOT EXISTS watchlist_{username} (SYMBOL VARCHAR(255),VOLUME INT,GOAL VARCHAR(255))")
count=conn.execute(f"SELECT COUNT(AMOUNT) FROM amount_{username}")
for ro in conn:
    if(int(ro[0])==0):
        conn.execute(f"INSERT INTO amount_{username} (AMOUNT) VALUES (0.0)")
        mydb.commit()

def stock_details():
    if flag!=1:
        labela = Label(root,text="TOP GAINERS",font=("Ariel",14,"bold"),bd=4,bg='#A269F8',fg="white",relief="raised",width=17,height=3)
        labela.place(x=1180, y=80)
        ycor=180
        for index,gainer in top_gainers.iterrows():
            label3 = Label(root,text=f"{index}. {gainer['Symbol']} - {gainer['Price (Intraday)']} ({gainer['% Change']})",font=("Ariel",15,"bold"),bd=4,bg='#74db44',fg="white",relief="raised",width=30,height=2)
            label3.place(x=1100, y=ycor)
            ycor=ycor+80
        ycor=180
        

def place_details():
    if flag==0:
        stock_details()
    

def watchlist():
    call(["python","watchlist_stock.py",sys.argv[1]])

def orders():
    call(["python","view_order.py",sys.argv[1]])
    

def view_funds():
    call(["python","view_funds.py",sys.argv[1]])



submit_button=Button(root,text="Watchlist",bg="#48dcfa",bd=4,command=watchlist)
submit_button.place(x=2,y=3,width=500,height=70)

submit_button=Button(root,text="Order",bg="#48dcfa",bd=4,command=orders)
submit_button.place(x=510,y=2,width=500,height=70)

submit_button=Button(root,text="Funds",bg="#48dcfa",bd=4,command=view_funds)
submit_button.place(x=1017,y=3,width=500,height=70)

img = ImageTk.PhotoImage(Image.open("wall2.jpg"))
label1 = Label(root, image = img,width=1000,height=762)
label1.place(x=10, y=75)

root.mainloop()