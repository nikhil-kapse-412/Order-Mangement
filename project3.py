from tkinter import *
from tkinter.messagebox import *
from pymongo import *
from tkinter.scrolledtext import *

def view():
    con = None
    try:
        con = MongoClient("localhost", 27017)
        db = con["project"]
        coll = db["order"]
        view_data.delete(1.0, END)
        data = coll.find()
        for d in data:
            view_data.insert(END, f"Order Number: {d['order_number']}\n")
            view_data.insert(END, f"Order Name: {d['order_name']}\n")
            view_data.insert(END, f"Phone Number Number: {d['phone_number']}\n")
            view_data.insert(END, f"Emaial Id: {d['email_id']}\n")
            view_data.insert(END, f"Address: {d['adres']}\n \n")
                        
    except Exception as e:
        showerror("Issue: ", e)
    finally:
        if con is not None:
            con.close()

def delete_order():
    mobile_number = delete_ent.get()

    if not mobile_number:
        showerror("Error", "Please enter a mobile number to delete.")
        return
    if not mobile_number.isdigit():
        showerror("Error", "Please no enter alphabets.")
        return
    if askokcancel("Confirmation", "Do you want to delete the order with mobile number?"):
        con = None
        try:
            con = MongoClient("localhost", 27017)
            db = con["project"]
            coll = db["order"]

            result = coll.delete_one({"phone_number": mobile_number})
            if result.deleted_count == 1:
                showinfo("Success", "Order Deleted")
            else:
                showerror("Error", "Order not found with that mobile number.")

        except Exception as e:
            showerror("Issue: ", e)
        finally:
            if con is not None:
                con.close()
        delete_ent.delete(0, END)
        delete_ent.focus()


def login(): 
    username = "Nikhil"
    password = "12345"

    user = admin_login_ent.get()
    pas = admin_pin_ent.get()

    if user != username and pas == password:
        showerror("Issue", "Wrong Username")
    elif user == username and pas != password:
        showerror("Issue", "Wrong Password")
    elif user != username and pas != password:
        showerror("Issue", "Wrong Password and username")
    elif user == "" or pas == "":
        showerror("Issue", "Enter the password/Username")
    else:
        showinfo("Success", "Login Successful")
        admin.deiconify()
        admin_page.deiconify()

def f3():
    root.withdraw()
    admin.deiconify()

def f2():
    try:
        con = None
        con = MongoClient("localhost", 27017)
        db = con["project"]
        coll = db["order"]

        order = order_no_ent.get()
        order_text = order_text_ent.get()
        mobile = mobile_number_ent.get()
        email = email_id_ent.get()
        address = addres_ent.get("1.0", "end-1c")
        
        if order == "":
            showerror("Issue", "Order Number should not be empty")
        elif order_text == "":
            showerror("Issue", "Do not keep name & Qty empty")
        elif mobile == "":
            showerror("Issue", "Do not leave the mobile number empty")
        elif email == "":
            showerror("Issue", "Do not leave the email-id empty")
        elif address == "":
            showerror("Issue", "Do not leave the address empty")
        elif any(char in "!@#$%^&*()" for char in order):
            showerror('Issue', 'Do not enter special characters in the Order Name')
        elif any(char in "!@#$%^&()*" for char in order_text):
            showerror('Issue', 'Do not enter special characters in the Order Name')
        elif any(char in "!@#$%^&()*" for char in mobile):
            showerror('Issue', 'Mobile number should not contain special characters and should be numbers only')
        elif not mobile.isdigit():
            showerror('Issue', 'Mobile number should contain only digits and no alphabets')
        elif any(char in "!@#$%^&*()" for char in address):
            showerror('Issue', 'Do not enter special characters in the address')
        elif any(char in "!#$%^&()*" for char in email):
            showerror('Issue', 'Do not enter special characters in the email-id')
        else:
            doc = {"order_number": order, "order_name": order_text, "phone_number": mobile, "email_id": email, "adres": address}
            coll.insert_one(doc)
            showinfo("Success", "Order Placed")

    except Exception as e:
        showerror("Issue", "Order not placed")
    finally:
        if con is not None:
            con.close()


def f1():
    root.withdraw()
    order.deiconify()

root = Tk()
root.title("Order Management")
root.geometry("600x600+20+20")
f = ("Arial", 30, "bold")

lab_title = Label(root, text="Order Management", font=f)
lab_title.pack(pady=5)

place_order_btn = Button(root, text="Place the order", font=f, command=f1)
admin_login_btn = Button(root, text="Admin Login", font=f, command=f3)
place_order_btn.pack(pady=5)
admin_login_btn.pack(pady=5)

order = Tk()
order.title("Order")
order.geometry("900x900+100+100")
order.withdraw()
f = ("Arial", 30, "bold")

menu = StringVar(order)

choices = {'1. tea', '2. coffee', '3. juice', '4. milkshake', '5. Soda'}
menu.set('View Order Options')
order_menu = OptionMenu(order, menu, *choices)
order_menu.config(font=f)
order_menu.place(x=450)

order_no_lab = Label(order, text="Enter order number", font=f)
order_no_ent = Entry(order, font=f)
order_no_lab.place(y=80, x=100)
order_no_ent.place(y=80, x=500)

order_text_lab = Label(order, text="Enter the name & Qty", font=f)
order_text_ent = Entry(order, font=f)
order_text_lab.place(y=160, x=100)
order_text_ent.place(y=160, x=520)

mobile_number = Label(order, text="Enter the mobile no.", font=f)
mobile_number_ent = Entry(order, font=f)
mobile_number.place(y=240, x=100)
mobile_number_ent.place(y=240, x=500)

email_id = Label(order, text="Enter email id", font=f)
email_id_ent = Entry(order, font=f)
email_id.place(y=320, x=100)
email_id_ent.place(y=320, x=500)

addres = Label(order, text="Enter your address", font=f)
addres_ent = ScrolledText(order, font=f)
addres.place(y=400, x=100)
addres_ent.place(y=400, x=500, height=85, width=450)

order_btn = Button(order, text="Order", font=f, command=f2)
order_btn.place(y=500)

def back():
    order.withdraw()
    root.deiconify()

back_btn = Button(order, text="Back", font=f, command=back)
back_btn.place(y=500, x=500)

admin = Tk()
admin.title("Admin Page")
admin.geometry("500x500+50+50")
admin.withdraw()

admin_login = Label(admin, text="Username", font=f)
admin_login_ent = Entry(admin, font=f)
admin_login.place(y=60, x=80)
admin_login_ent.place(y=60, x=300, width=150)
admin_pin = Label(admin, text="Password", font=f)
admin_pin_ent = Entry(admin, font=f, show="*")
admin_pin.place(y=120, x=80)
admin_pin_ent.place(y=120, x=300, width=150)

def bck():
    admin.withdraw()
    root.deiconify()

login_btn = Button(admin, text="Login", font=f, command=login)
login_btn.place(y=180, x=70, height=50)
bck_btn = Button(admin, text="Back", font=f, command=bck)
bck_btn.place(y=180, x=250, height=50)


admin_page = Tk()
admin_page.title("Admin Page")
admin_page.geometry("400x400+50+50")
admin_page.withdraw()

def f9():
    admin_page.withdraw()
    admin.deiconify()


def f4():
    admin_page.withdraw()
    delete_window.deiconify()

def f3():
    admin_page.withdraw()
    view2.deiconify()

delete_btn = Button(admin_page, text="Delete Order", font=f, command=f4)
delete_btn.place(y=60, x=80)

view_btn = Button(admin_page, text="View Order", font=f, command=f3)
view_btn.place(y=145, x=80)

bk_btn = Button(admin_page, text="Back", font=f, command=f9)
bk_btn.place(y=320, x=80)

view2 = Tk()
view2.title("View Order")
view2.geometry("700x700+50+60")
view2.withdraw()

def back5():
    view2.withdraw()
    admin_page.deiconify()

view_data = ScrolledText(view2, font=f)
view_data.place(x=20, y=20, height=400, width=1000)
view_btn = Button(view2, text="View Order", font=f, command=view)
view_btn.place(y=475, x=100)

back_btn1 = Button(view2, text='back', font=f, command=back5)
back_btn1.place(y=475, x=500)


delete_window = Tk()
delete_window.title("View Order")
delete_window.geometry("900x900+50+50")
delete_window.withdraw()

def back8():
    delete_window.withdraw()
    admin_page.deiconify()


delete_order1 = Label(delete_window, text="Enter the Mobile Number", font=f)
delete_order1.place(y=70, x=50)
delete_ent = Entry(delete_window,font=f)
delete_ent.place(y=70, x=550)

delete_btn = Button(delete_window, text="Delete Order", font=f, command=delete_order)
delete_btn.place(y=140, x=50)

back_btn2 = Button(delete_window, text='back', font=f, command=back8)
back_btn2.place(y=140, x=400)


def f9():
    if askokcancel("Quit", "Do u want to exit"):
        root.destroy()
        order.destroy()
        admin.destroy()
        admin_page.destroy()
        view2.destroy()
        delete_window.destroy()

root.protocol("WM_DELETE_WINDOW", f9)
order.protocol("WM_DELETE_WINDOW", f9)
admin.protocol("WM_DELETE_WINDOW", f9)
admin_page.protocol("WM_DELETE_WINDOW", f9)
view2.protocol("WM_DELETE_WINDOW", f9)
delete_window.protocol("WM_DELETE_WINDOW", f9)

root.mainloop()



