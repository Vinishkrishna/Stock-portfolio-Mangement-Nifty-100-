from tkinter import *
import mysql.connector
from tkinter import ttk
from yahoo_fin import stock_info as si
import decimal
import matplotlib.pyplot as plt
from tkinter import messagebox
import sys

username=sys.argv[1]

mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="stock_portfolio"
)

conn = mydb.cursor()

root = Tk()

def price():
    if(var.get() in symbols):
        a=var.get()  
        try:
            b=round(decimal.Decimal(si.get_live_price(f"{a}.NS")),2)
        except Exception as e:
            print(e)
        price_label = Label(root, text=f"Price {b}",width=20,height=2)
        price_label.place(x=200,y=440)
        return b
    else:
        pass

def place_order(symbol, order_type, quantity, price,i,username):
    conn.execute(f"SELECT*FROM amount_{username}")
    for ro in conn:
        total=round(price*decimal.Decimal(quantity),2)
        if(order_type=="BUY"):
            if(ro[0]>=total):
                data="Placing order for " + symbol + " shares of " + quantity + " at Rs:" + str(price) + " per share. |  Order type: " + order_type +  " |"  +" TOTAL:Rs "+ str(total)
                listbox.insert(i,data)
                conn.execute(f"INSERT INTO orders_{username} (ORDERS) VALUES ('{data}')")
                conn.execute(f"SELECT*FROM portfolio_{username}")
                current=[]
                for ro in conn:
                    current.append(ro[0])
                if symbol not in current:
                    conn.execute(f"INSERT INTO portfolio_{username} (STOCKS,QUANTITY) VALUES ('{symbol}',{quantity})")
                else:
                    conn.execute(f"UPDATE portfolio_{username} SET QUANTITY=QUANTITY+{quantity} WHERE STOCKS='{symbol}'")
                conn.execute(f"UPDATE amount_{username} SET AMOUNT=AMOUNT-{total}")
            else:
                messagebox.showerror("Not Enough funds","Please add some amount")
        else:
            conn.execute(f"SELECT*FROM portfolio_{username} WHERE STOCKS='{symbol}'")
            for ro in conn:
                stock_quantity=ro[1]
                break
            else:
                stock_quantity=0
            if(stock_quantity>=int(quantity)):
                data="Placing order for " + symbol + " shares of " + quantity + " at Rs:" + str(price) + " per share. |  Order type: " + order_type +  " |"  +" TOTAL:Rs "+ str(total)
                listbox.insert(i,data)
                conn.execute(f"INSERT INTO orders_{username} (ORDERS) VALUES ('{data}')")
                conn.execute(f"SELECT*FROM portfolio_{username}")
                current=[]
                for ro in conn:
                    current.append(ro[0])
                if symbol not in current:
                    conn.execute(f"INSERT INTO portfolio_{username} (STOCKS,QUANTITY) VALUES ('{symbol}',{quantity})")
                else:
                    conn.execute(f"UPDATE portfolio_{username} SET QUANTITY=QUANTITY-{quantity} WHERE STOCKS='{symbol}'")
                conn.execute(f"UPDATE amount_{username} SET AMOUNT=AMOUNT+{total}")
            else:
                messagebox.showerror("Not Enough Stock quantity",f"Your {symbol} stock quantity is only {stock_quantity}")
    mydb.commit()

def portfolio():
    conn.execute(f"SELECT*FROM portfolio_{username}")
    x=[]
    y=[]
    for ro in conn:
        x.append(ro[0])
        y.append(ro[1])
    
    if len(x)!=0 and len(y)!=0:
        plt.title("Portfolio")
        plt.pie(y,labels=x,explode=(0.1,)*len(y),autopct="%1.2f%%")
        plt.axis("equal")
        plt.show()
    else:
        messagebox.showerror("Portfolio has no Stocks","Please buy some stocks to view portfolio")

def display_order(username):
    conn.execute(f"SELECT*FROM orders_{username}")
    for ro in conn:
        listbox.insert(0,ro[0])
    
i=0
listbox = Listbox(root, height = 43,width = 100,bg = "grey",activestyle = 'dotbox',font = ("Helvetica",15),fg = "yellow")

# Create a label for the orders title
title_label = Label(root, text="Orders", font=("Arial", 16))
title_label.place(x=1000,y=15)
listbox.place(x=500,y=50)
display_order(username)
root.title("View Orders")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("%dx%d+%d+%d" %(screen_width,screen_height,0,0))
root.configure(background="#EFBB96")
root.resizable(width=False, height=False)
title_label = Label(root, text="Place Order", font=("Arial", 20),width=15)
title_label.place(x=200,y=55)

symbol_label = Label(root, text="Stock Symbol:",width=14,height=2)
symbol_label.place(x=60,y=120)

conn.execute("SELECT * FROM COMPANY")
symbols=[]
for ro in conn:
    symbols.append(ro[0])


var=StringVar()
combo=ttk.Combobox(root,values=symbols,textvariable=var)
combo.place(x=200,y=120,width=272,height=38)
# Create an entry box for the order type
type_label = Label(root, text="Order Type:",width=14,height=2)
type_label.place(x=60,y=230)
options=["BUY","SELL"]
car=StringVar()
combo=ttk.Combobox(root,values=options,textvariable=car)
combo.place(x=200,y=230,width=272,height=38)
    # Create an entry box for the order quantity
quantity_label = Label(root, text="Quantity:",width=14,height=2)
quantity_label.place(x=60,y=340)
quantity_entry = Entry(root,width=18,font=(('calibre',20,'normal')))
quantity_entry.place(x=200,y=340)

place_order_button = Button(root, text="Place Order",font=20, command=lambda: place_order(var.get(), car.get(), quantity_entry.get(),price(),i,username))
place_order_button.place(x=180,y=540,width=200,height=30)

portfolio_button=Button(root,text="Portfolio",font=20,command=portfolio)
portfolio_button.place(x=240,y=590)
root.mainloop()
