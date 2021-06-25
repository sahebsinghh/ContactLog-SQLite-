#import library
import tkinter
from tkinter import *
import tkinter.ttk as ttk
import sqlite3

#initialize window
root = Tk()
root.title("CONTACT LOG")
root.geometry("1100x600")
root.minsize(height=300,width=500)
root.config(bg = 'royal blue')
root.resizable(0,0)

#Frames

#TOP Frame
Top = Frame(root, bd=2, relief=SOLID)
Top.pack(side=TOP)

#frame for entry label and entry box
add_frame = Frame(root,bd=2,relief=SOLID)
add_frame.pack(pady=40,anchor=tkinter.NW)

#frame for table
TableMargin = Frame(root,width=700,height=700,bd=2,bg="light green",relief=SOLID)
TableMargin.pack(side = LEFT,anchor=W)
TableMargin.pack_propagate(0)

#label for top frame
lbl_title = Label(Top, text="CONTACT LOG ", font=('TIMES NEW ROMAN BOLD', 20), width=500)
lbl_title.pack(fill=X)

#inserting image
photo = PhotoImage(file="phoneicon.png")
image_label = Label(root,image=photo,bg="royal blue",height=400,width=600)
image_label.pack(side=BOTTOM,anchor=tkinter.SE)

#creating label for entering data into table
name_label = Label(add_frame,text="FIRST NAME", font=('TIMES NEW ROMAN BOLD', 12))
name_label.grid(row=0,column=0)
surname_label=Label(add_frame,text="LAST NAME", font=('TIMES NEW ROMAN BOLD', 12))
surname_label.grid(row=0,column=1)
countrycode_label=Label(add_frame,text="COUNTRY CODE", font=('TIMES NEW ROMAN BOLD',12))
countrycode_label.grid(row=0,column=2)
number_label=Label(add_frame,text="CONTACT NO", font=('TIMES NEW ROMAN BOLD', 12))
number_label.grid(row=0,column=3)

#entry boxes
name_box = Entry(add_frame,font=('TIMES NEW ROMAN', 12))
name_box.grid(row=1,column=0)
surname_box = Entry(add_frame, font=('TIMES NEW ROMAN ', 12))
surname_box.grid(row=1,column=1)
countrycode_box = Entry(add_frame, font=('TIMES NEW ROMAN ', 12))
countrycode_box.grid(row=1,column=2 )
number_box = Entry(add_frame, font=('TIMES NEW ROMAN', 12))
number_box.grid(row=1,column=3)

#Declaring list and variables
NAME = StringVar()
SURNAME = StringVar()
COUNTRYCODE = StringVar()
NUMBER = StringVar()
contactlist=[]

#Defining Functions

#Creating a database
def Database():
    conn = sqlite3.connect("contactlog.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER  PRIMARY KEY AUTOINCREMENT,name TEXT, surname TEXT, countrycode TEXT, number TEXT)")
    cursor.execute("SELECT * FROM `member` ORDER BY `name` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

# To Add a new contact
def ADD():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("contactlog.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `member` (name, surname, countrycode,number) VALUES( ?, ?, ?, ?)",(str(name_box.get()),str(surname_box.get()), str(countrycode_box.get()), str(number_box.get())))
    conn.commit()
    cursor.execute("SELECT * FROM `member` ORDER BY `name` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    NAME.set("")
    SURNAME.set("")
    COUNTRYCODE.set("")
    NUMBER.set("")

    #clearing the entry boxes
    name_box.delete(0, END)
    surname_box.delete(0, END)
    countrycode_box.delete(0, END)
    number_box.delete(0, END)

# To Delete selected contact
def DELETE():
    curItem = tree.focus()
    contents = (tree.item(curItem))
    selecteditem = contents['values']
    tree.delete(curItem)
    conn = sqlite3.connect("contactlog.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
    conn.commit()
    cursor.close()
    conn.close()

# To view selected contact
def VIEW():
    selected = tree.focus()
    values = tree.item(selected,'values')
    name_box.insert(0, values[1])
    surname_box.insert(0, values[2])
    countrycode_box.insert(0 ,values[3])
    number_box.insert(0, values[4])

# To view selected contact(first select then click on view button)
def UPDATE():
    global mem_id
    curItem = tree.focus()
    contents = (tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("contactlog.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE `member` SET `name` = ?, `surname` = ?, `countrycode` =?, `number` = ?  WHERE  `mem_id` = ?",(str(name_box.get()), str(surname_box.get()), str(countrycode_box.get()), str(number_box.get()),int(mem_id)))
    conn.commit()
    cursor.execute("SELECT * FROM `member` ORDER BY `name` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    NAME.set("")
    SURNAME.set("")
    COUNTRYCODE.set("")
    NUMBER.set("")

    #clearing the entry boxes
    name_box.delete(0, END)
    surname_box.delete(0, END)
    countrycode_box.delete(0, END)
    number_box.delete(0, END)

#Reseting entry boxes
def RESET():
    name_box.delete(0, END)
    surname_box.delete(0, END)
    countrycode_box.delete(0, END)
    number_box.delete(0, END)

#Exit output window
def EXIT():
    root.destroy()

#scrollbar  for table
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID","NAME", "SURNAME","COUNTRYCODE" ,"NUMBER"),height=30, selectmode="extended", yscrollcommand=scrollbary.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT,fill=Y)

#Declaring columns in table
tree.heading('MemberID', text="MemberID",anchor=W)
tree.heading('NAME', text="FIRST NAME", anchor=W)
tree.heading('SURNAME', text="LAST NAME",anchor=W)
tree.heading('COUNTRYCODE', text="COUNTRY CODE",  anchor=W)
tree.heading('NUMBER',text="CONTACT NO", anchor=W)
tree.column('#0', stretch=NO,minwidth=0,width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=100)
tree.column('#3', stretch=NO, minwidth=0, width=90)
tree.column('#4', stretch=NO, minwidth=0, width=100)
tree.column('#5', stretch=NO, minwidth=0, width=100)
tree.pack()

#Creating a Button
Button(root, text="ADD",height=1,width=7,bd=6,font='arial 12 bold', bg='SlateGray4', command=ADD).place(x=720, y=80)
Button(root, text="DELETE",height=1,width=7,bd=6,font='arial 12 bold', bg='SlateGray4', command=DELETE).place(x=840, y=80)
Button(root, text="UPDATE", height=1,width=7,bd=6,font='arial 12 bold', bg='SlateGray4', command=UPDATE).place(x=720, y=140)
Button(root, text="VIEW", height=1,width=7,bd=6,font='arial 12 bold', bg='SlateGray4', command=VIEW).place(x=840, y=140)
Button(root,text="RESET", height=1,width=7,bd=6,font='arial 12 bold',bg='SlateGray4', command = RESET).place(x= 960, y=80)
Button(root, text="EXIT",height=1,width=7 ,bd=6,font='arial 12 bold', bg='red', command=EXIT).place(x=960, y=140)

#Initialization
if __name__ == '__main__':
    Database()

root.mainloop()