import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import *

conn = sqlite3.connect("canteen.db")
curr = conn.cursor()
curr.execute(
    'create table if not exists Grocery(item_name text, quantity integer, price real, date text, total_price real)')


class Grocery(Toplevel):
    def __init__(self,username):
        Toplevel.__init__(self)
        self.title("CanMagS")
        self.geometry("1200x700+0+0")
        self.resizable(False, False)
        self.config(bg='mediumseagreen')
        self.count = 0
        tk.Label(self, text="CanMagS", fg="blue", bg='mediumseagreen',
                 font=('Goudy Old Style', 80)).place(x=400, y=5)

        tk.Label(self, text="Item name",
                 fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=200)
        Label(self, text="Quantity",
              fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=230)
        Label(self, text="Price",
              fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=260)
        Label(self, text="Date", 
              fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=290)
        self.itn = StringVar()
        self.e1 = Entry(self, textvariable=self.itn)
        self.e1.place(x=160, y=205)
        self.q = StringVar()
        self.e2 = Entry(self, textvariable=self.q)
        self.e2.place(x=160, y=235)
        self.p = StringVar()
        self.e3 = Entry(self, textvariable=self.p)
        self.e3.place(x=160, y=265)
        self.d = StringVar()
        self.e4 = Entry(self, textvariable=self.d)
        self.e4.place(x=160, y=295)

        Button(self, text="Add", command=self.Add,
               height=3, width=13).place(x=600, y=250)
        Button(self, text="View information", command=self.view,
               height=3, width=13).place(x=710, y=250)
        Button(self, text="Update", command=self.update,
               height=3, width=13).place(x=820, y=250)
        Button(self, text="Delete", command=self.delete,
               height=3, width=13).place(x=930, y=250)
       

        cols = ('Item Name', 'Quantity', 'Price', 'Date', 'Total Price')
        self.listBox = ttk.Treeview(self, columns=cols, show='headings')

        for col in cols:
            self.listBox.heading(col, text=col)
            self.listBox.column(col, anchor=CENTER)
            self.listBox.grid(row=1, column=0, columnspan=2)
            self.listBox.place(x=30, y=350)

        self.listBox.bind('<Double-Button-1>', self.GetValue)
        self.show()

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

    
    def Add(self):
        item_name = self.e1.get()
        quantity = self.e2.get()
        price = self.e3.get()
        date = self.e4.get()
        self.tp = float(price) * float(quantity)
        try:
            curr.execute('insert into Grocery values(?,?,?,?,?)',
                         (item_name, quantity, price, date, self.tp))
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
            self.e4.delete(0, END)
            self.e1.focus_set()
            self.show()
            conn.commit()

        except Exception as e:
            print(e)

    def view(self):
        try:
            selected = self.listBox.focus()
            temp = self.listBox.item(selected, 'values')
            temp = list(temp)
            self.itn.set(temp[0])
            self.e1.config(state='disabled')
            self.q.set(temp[1])
            self.p.set(temp[2])
            self.d.set(temp[3])

        except Exception as e:

            print(e)

    def update(self):
        try:
            self.tp = float(self.e2.get()) * float(self.e3.get())
            curr.execute('update Grocery set quantity = ?, price = ?, date = ?, total_price = ? where item_name = ?',
                         (self.e2.get(), self.e3.get(), self.e4.get(), self.tp, self.e1.get()))
            self.e1.config(state='normal')
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
            self.e4.delete(0, END)
            self.e1.focus_set()
            self.show()
            conn.commit()

        except Exception as e:

            print(e)

    def delete(self):
        try:
            selected = self.listBox.focus()
            temp = self.listBox.item(selected, 'values')
            temp = list(temp)
            curr.execute('DELETE FROM Grocery WHERE item_name=?', (temp[0],))
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
            self.e4.delete(0, END)
            self.e1.focus_set()
            conn.commit()
            for record in selected:
                self.listBox.delete(record)
            self.show()

        except Exception as e:
            print(e)

    def show(self):
        for i in self.listBox.get_children():
            self.listBox.delete(i)
        count = 1
        curr.execute("SELECT * from Grocery")
        records = curr.fetchall()
        for record in records:
            self.listBox.insert(parent='', index='end', iid=count, text='', values=(
                record[0], record[1], record[2], record[3], record[4]))
            count += 1

    