import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import *
import random

conn = sqlite3.connect("canteen.db")
curr = conn.cursor()
curr.execute(
    'create table if not exists Bill(item_name text, quantity integer, price real, date text, total_price real)')


class Bill(Toplevel):
    def __init__(self, username):
        Toplevel.__init__(self)
        self.title("CanMagS")
        self.geometry("1200x700+0+0")
        self.resizable(False, False)
        self.config(bg='mediumseagreen')
        self.count = 0
        tk.Label(self, text="CanMagS", fg="blue", bg='mediumseagreen',
                 font=('Goudy Old Style', 80)).place(x=400, y=5)

        tk.Label(self, text="Item name",
                 fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=90, y=310)
        Label(self, text="Quantity",
              fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=90, y=340)
        Label(self, text="Price", 
              fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=90, y=370)
        Label(self, text="Date", fg="blue", bg='mediumseagreen',
              font=('Arial', 16)).place(x=90, y=400)
        self.itn = StringVar()
        self.e1 = Entry(self, textvariable=self.itn)
        self.e1.place(x=210, y=315)
        self.q = StringVar()
        self.e2 = Entry(self, textvariable=self.q)
        self.e2.place(x=210, y=345)
        self.p = StringVar()
        self.e3 = Entry(self, textvariable=self.p)
        self.e3.place(x=210, y=375)
        self.d = StringVar()
        self.e4 = Entry(self, textvariable=self.d)
        self.e4.place(x=210, y=405)

        
    
        Button(self, text="Generate Bill", command=self.gBill,
               height=3, width=13).place(x=100, y=490)
              
        

    def store(self):
        item_name = self.e1.get()
        quantity = self.e2.get()
        price = self.e3.get()
        date = self.e4.get()
        try:
            curr.execute('insert into Bill values(?,?,?,?,?)',
                         (item_name, quantity, price, date, self.tp))
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
            self.e4.delete(0, END)
            self.e1.focus_set()
            conn.commit()
        

        except Exception as e:
            print(e)
    
        # Billing area
    def gBill(self):
        try:
            quantity = self.e2.get()
            price = self.e3.get()
            self.tp = float(price) * float(quantity)
            bill_no = StringVar()
            x=random.randint(1000,9999)
            bill_no.set(str(x))
            F = Frame(self,relief = GROOVE)
            F.place(x=550, y=150, width=600, height=450)
            bill_title = Label(F, text='Bill', font=('Arial', 16), relief=GROOVE).pack(fill=X)
            scroll_y = Scrollbar(F, orient=VERTICAL)
            text_area = Text(F, yscrollcommand=scroll_y)
            scroll_y.pack(side=RIGHT, fill=Y)
            scroll_y.config(command=text_area.yview)
            text_area.pack()
            text_area.delete(1.0, END)
            text_area.insert(END, "\t\t\t CanMagS")
            text_area.insert(END, f'\n\n Bill Number:\t{bill_no.get()}')
            text_area.insert(END, f'\n Date:\t{self.d.get()}')
            text_area.insert(END, f'\n===========================================')
            text_area.insert(END, '\n Item Name\t\t  Quantity\t\t         Price\t')
            text_area.insert(END, f'\n {self.e1.get()}\t\t  {self.e2.get()}\t\t         {self.e3.get()}\t')
            text_area.insert(END, f'\n===========================================\n\n')
            text_area.insert(END, f'\n Total Price:\t {self.tp}')
            text_area.configure(font=('Arial', 14))
            self.store()
        
        except Exception as e:
            print(e)
        

    def GetValue(self, event):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        row_id = self.listBox.selection()[0]
        select = self.listBox.set(row_id)
        self.e1.insert(0, select['item_name'])
        self.e2.insert(0, select['quantity'])
        self.e3.insert(0, select['price'])
        self.e4.insert(0, select['date'])

    # def update(self):
    #     try:
    #         self.tp = float(self.e2.get()) * float(self.e3.get())
    #         curr.execute('update Bill set quantity = ?, price = ?, date = ?, total_price = ? where item_name = ?',
    #                      (self.e2.get(), self.e3.get(), self.e4.get(), self.tp, self.e1.get()))
    #         self.e1.config(state='normal')
    #         self.e1.delete(0, END)
    #         self.e2.delete(0, END)
    #         self.e3.delete(0, END)
    #         self.e4.delete(0, END)
    #         self.e1.focus_set()
    #         self.show()
    #         conn.commit()

    #     except Exception as e:

    #         print(e)

# root = tk()
# b = Bill(root)
# root.mainloop()

   

   