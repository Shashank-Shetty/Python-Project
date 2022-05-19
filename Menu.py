import tkinter as tk
from tkinter import ttk, messagebox as mb
import sqlite3
from tkinter import *
from grocery import Grocery
from Employee import Employee
from Bill import Bill
from Institution import Institution
from Wastemanagement import Wastemanagement
from PIL import Image, ImageTk

class Menu(Toplevel):
    def __init__(self, username):
       Toplevel.__init__(self)
       self.title("CanMagS")
       self.geometry("1200x700+0+0")
       self.resizable(False, False)
       self.config(bg='mediumseagreen')
       self.username = username
       #Frame_login=Frame(self,bg="")
       #Frame_login.place(x=0,y=0,height=700,width=1366)
       #self.img=ImageTk.PhotoImage(file="C:\\Users\\Shashank Shetty\\Downloads\\234171.jpg")
       #img=Label(Frame_login,image=self.img).place(x=0,y=0,width=1366,height=700)
       tk.Label(self, text="CanMagS", fg="blue", bg='mediumseagreen',font=('Goudy Old Style', 80)).place(x=400, y=5)
       Button(self,command=self.grocery, text="Grocery", fg="black", bg='azure3',
              height=6, width=20).place(x=30, y=300)
       Button(self,command=self.bill, text="Bill", fg="black", bg='azure3',
             height=6, width=20).place(x=360, y=300)
       Button(self,command=self.institution, text="Institution", fg="black", bg='azure3',
              height=6, width=20).place(x=690, y=300)
       Button(self,command=self.employee, text="Employee", fg="black", bg='azure3',
              height=6, width=20).place(x=1020, y=300)
       
       
    def grocery(self):
       g = Grocery(self.username)

    def Wastemanagement(self):
       w = Wastemanagement(self.username)
    
    def bill(self):
       b = Bill(self.username)
    
    def employee(self):
       e = Employee(self.username)
       
    def institution(self):
       i = Institution(self.username)


