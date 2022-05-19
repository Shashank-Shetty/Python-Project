import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import *
#import pattern
import re

conn = sqlite3.connect("canteen.db")
curr = conn.cursor()
curr.execute('create table if not exists Employee(name text, role text, gender text, phone_no text, address text, salary real)')


class Employee(Toplevel):
    def __init__(self, username):
        Toplevel.__init__(self)
        self.title("CanMagS")
        self.geometry("1200x700+0+0")
        self.resizable(False, False)
        self.config(bg='mediumseagreen')
        self.count = 0
        tk.Label(self, text="CanMagS", fg="blue", bg = 'mediumseagreen',
                 font=('Goudy Old Style', 80)).place(x=400, y=5)

        tk.Label(self, text="Name",fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=200)
        Label(self, text="Role",fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=230)
        Label(self, text="Gender", fg="blue",
              bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=260)
        Label(self, text="Phone no", fg="blue",
              bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=290)
        Label(self, text="Address", fg="blue",
              bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=320)
        Label(self, text="Salary", fg="blue",
              bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=350)
        self.n = StringVar()
        self.e1 = Entry(self, textvariable=self.n)
        self.e1.place(x=160, y=205)
        self.r = StringVar()
        self.e2 = Entry(self, textvariable=self.r)
        self.e2.place(x=160, y=235)
        self.g = StringVar()
        self.e3 = Entry(self, textvariable=self.g)
        self.e3.place(x=160, y=265)
        self.p = StringVar()
        self.e4 = Entry(self, textvariable=self.p)
        self.e4.place(x=160, y=295)
        self.a = StringVar()
        self.e5 = Entry(self, textvariable=self.a)
        self.e5.place(x=160, y=325)
        self.s = StringVar()
        self.e6 = Entry(self, textvariable=self.s)
        self.e6.place(x=160, y=355)

        Button(self, text="Add", command=self.Add,
               height=3, width=13).place(x=600, y=250)
        Button(self, text="View information", command=self.view,
               height=3, width=13).place(x=710, y=250)
        Button(self, text="Update", command=self.update,
               height=3, width=13).place(x=820, y=250)
        Button(self, text="Delete", command=self.delete,
               height=3, width=13).place(x=930, y=250)
        

        cols = ('Name', 'Role', 'Gender', 'Phone No', 'Address', 'Salary')
        self.listBox = ttk.Treeview(self, columns=cols, show='headings')

        for col in cols:
            self.listBox.heading(col, text=col)
            self.listBox.column(col, anchor=CENTER)
            self.listBox.grid(row=1, column=0, columnspan=2)
            self.listBox.place(x=0, y=400)

        self.listBox.bind('<Double-Button-1>', self.GetValue)
        self.show()

    def GetValue(self, event):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0, END)
        self.e5.delete(0, END)
        self.e6.delete(0, END)
        row_id = self.listBox.selection()[0]
        select = self.listBox.set(row_id)
        self.e1.insert(0, select['name'])
        self.e2.insert(0, select['role'])
        self.e3.insert(0, select['gender'])
        self.e4.insert(0, select['phone_no'])
        self.e5.insert(0, select['adress'])
        self.e6.insert(0, select['salary'])

    def Add(self):
        name = self.e1.get()
        role = self.e2.get()
        gender = self.e3.get()
        phone_no = self.e4.get()
        address = self.e5.get()
        salary = self.e6.get()
        try:
            curr.execute('insert into Employee values(?,?,?,?,?,?)',(name, role, gender, phone_no, address, salary))
            rowcount = curr.lastrowid
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
            self.e4.delete(0, END)
            self.e5.delete(0, END)
            self.e6.delete(0, END)
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
            self.n.set(temp[0])
            self.e1.config(state='disabled')
            self.r.set(temp[1])
            self.g.set(temp[2])
            self.p.set(temp[3])
            self.a.set(temp[4])
            self.s.set(temp[5])

        except Exception as e:

            print(e)

    def update(self):
        try:
            curr.execute('update Employee set role = ?, gender = ?, phone_no = ?, address = ?, salary = ? where name = ?',
                         (self.e2.get(), self.e3.get(), self.e4.get(), self.e5.get(), self.e6.get(), self.e1.get()))
            self.e1.config(state='normal')
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
            self.e4.delete(0, END)
            self.e5.delete(0, END)
            self.e6.delete(0, END)
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
            curr.execute('DELETE FROM Employee WHERE name=?', (temp[0],))
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
            self.e4.delete(0, END)
            self.e5.delete(0, END)
            self.e6.delete(0, END)
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
        curr.execute("SELECT * from Employee")
        records = curr.fetchall()
        for record in records:
            self.listBox.insert(parent='', index='end', iid=count, text='', values=(
                record[0], record[1], record[2], record[3], record[4], record[5]))
            count += 1

    