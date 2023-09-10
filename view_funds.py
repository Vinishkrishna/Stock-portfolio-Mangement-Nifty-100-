from tkinter import *
import mysql.connector
import sys

username=sys.argv[1]

mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="stock_portfolio"
)

conn = mydb.cursor()

def updated_amount(username):
    conn.execute(f"SELECT*FROM amount_{username}")
    for ro in conn:
        amount_label["text"]=f"Amount : {ro[0]}"
    mydb.commit()

def add_funds_submit(username):
    amount=amount_entry.get()
    conn.execute(f"UPDATE amount_{username} SET AMOUNT=AMOUNT+{amount}")
    updated_amount(username)

def withdraw_funds_submit(username):
    amount=amount_entry.get()
    conn.execute(f"UPDATE amount_{username} SET AMOUNT=AMOUNT-{amount}")
    updated_amount(username)

root = Tk()
root.title("View Funds")
root.iconbitmap(r'C:\Users\R VINISH KRISHNA\Desktop\Login\stock-market.ico')
root.geometry("%dx%d+%d+%d" %(300,300,0,0))
root.configure(background="#EFBB96")
root.resizable(width=False, height=False)
title_label = Label(root, text="Add Funds", font=("Arial", 16))
title_label.pack()

cash_radio = Label(root, text="Cash",font=("Arial", 12),width=10,bd=3,relief="solid",background="#A881AF")
cash_radio.place(x=100,y=35)
amount_label = Label(root, text="Amount:", font=("Arial", 12),width=20)
amount_label.place(x=70,y=80)

conn.execute(f"SELECT*FROM amount_{username}")

flag=0
for ro in conn:
    amount_label["text"]=f"Amount : {ro[0]}"
    flag=flag+1
else:
    if not flag:
        data=0
        amount_label["text"]=f"Amount : {data}"
        conn.execute(f"INSERT INTO amount_{username} (AMOUNT) VALUES ({data})")

amount_entry = Entry(root, font=("Arial", 16),width=10)
amount_entry.place(x=80,y=120)

submit_button = Button(root, text="Add Funds", font=("Arial", 12), command=lambda:add_funds_submit(username))
submit_button.place(x=100,y=150)

submit_button = Button(root, text="Withdraw Funds", font=("Arial", 12), command=lambda:withdraw_funds_submit(username))
submit_button.place(x=90,y=200)
root.mainloop()