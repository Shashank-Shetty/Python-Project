import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import *

conn = sqlite3.connect("canteen.db")
curr = conn.cursor()
curr.execute('''create table if not exists Institution(stud_id text primary key, stud_name text)''')


class Institution(Toplevel):
    def __init__(self, username):
        Toplevel.__init__(self)
        self.title("CanMagS")
        self.geometry("1200x700+0+0")
        self.resizable(False, False)
        self.config(bg='mediumseagreen')
        self.count = 0
        tk.Label(self, text="CanMagS", fg="blue", bg='mediumseagreen', font=('Goudy Old Style', 80)).place(x=400, y=5)
        tk.Label(self, text="Student ID", fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=200)
        Label(self, text="Student Name", fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=230)
        Label(self, text="Search", fg="blue", bg='mediumseagreen', font=('Arial', 16)).place(x=30, y=260)
        

        self.stud_id = StringVar()
        self.e1 = Entry(self, textvariable=self.stud_id)
        self.e1.place(x=180, y=205)
        self.stud_name = StringVar()
        self.e2 = Entry(self, textvariable=self.stud_name)
        self.e2.place(x=180, y=235)
        self.search = StringVar()
        self.e3 = Entry(self, textvariable=self.search)
        self.e3.place(x=180, y=265)
       

        Button(self, text="Add", command=self.Add,
               height=3, width=13).place(x=30, y=350)
        Button(self, text="View information", command=self.view,
               height=3, width=13).place(x=140, y=350)
        Button(self, text="Update", command=self.update,
               height=3, width=13).place(x=250, y=350)
        Button(self, text="Delete", command=self.delete,
               height=3, width=13).place(x=370, y=350)
        Button(self, text="Search", command=self.searchName,
               height=3, width=13).place(x=490, y=350)
        Button(self, text="Breakfast", command=self.token,
               height=3, width=13).place(x=30, y=500)
        Button(self, text="Lunch", command=self.token,
               height=3, width=13).place(x=140, y=500)
        Button(self, text="Snacks", command=self.token,
               height=3, width=13).place(x=250, y=500)
        

        cols = ('Student ID', 'Student Name')
        self.listBox = ttk.Treeview(self, columns=cols, show='headings')

        for col in cols:
            self.listBox.heading(col, text=col)
            self.listBox.column(col, anchor=CENTER)
            self.listBox.grid(row=1, column=0, columnspan=2)
            self.listBox.place(x=700, y=200)

        self.listBox.bind('<Double-Button-1>', self.GetValue)
        self.show()

    def GetValue(self, event):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        
        row_id = self.listBox.selection()[0]
        select = self.listBox.set(row_id)
        self.e1.insert(0, select['stud_id'])
        self.e2.insert(0, select['stud_name'])
        

    def Add(self):
        stud_id = self.e1.get()
        stud_name = self.e2.get()
        try:
            curr.execute('insert into Institution values(?,?)',
                         (stud_id, stud_name))
            rowcount = curr.lastrowid
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
            
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
            self.stud_id.set(temp[0])
            self.e1.config(state='disabled')
            self.stud_name.set(temp[1])
            # self.no_of_studs_s.set(temp[2])
            # self.m.set(temp[3])

        except Exception as e:

            print(e)

    def update(self):
        try:
            curr.execute('update Institution set stud_id = ?, stud_name = ? where stud_id = ?',
                         (self.e1.get(), self.e2.get(), self.e1.get()))
            self.e1.config(state='normal')
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
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
            curr.execute('DELETE FROM Institution WHERE stud_id=?', (temp[0],))
            self.e1.delete(0, END)
            self.e2.delete(0, END)
            self.e3.delete(0, END)
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
        curr.execute("SELECT * from Institution")
        records = curr.fetchall()
        for record in records:
            self.listBox.insert(parent='', index='end', iid=count, text='', values=(
                record[0], record[1]))
            count += 1
            
    def searchName(self):
        # for i in self.listBox.get_children():
        #     self.listBox.delete(i)
        # count = 1
        # si = self.e1.get()
        si = self.e3.get()
        curr.execute("SELECT stud_id,stud_name from Institution where stud_id = ?", (si,))
        # # records = curr.fetchall()
        rows = curr.fetchall()
        for i in self.listBox.get_children():
            self.listBox.delete(i)
        count = 1
        for record in rows:
            self.listBox.insert(parent='', index='end', iid=count, text='', values=(
                record[0], record[1]))
            count += 1
        
    
    def token(self):
        messagebox.showinfo(
            "Success", "Token Generated", parent=self)

    
