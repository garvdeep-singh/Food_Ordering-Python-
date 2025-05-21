from tkinter import *
from tkinter import ttk
import sqlite3
from PIL import ImageTk,Image
from tkinter import messagebox
import pyttsx3




root=Tk()
root.title("ORDER ONLINE")
root.geometry("600x600")
root.configure(bg="white")

def message():
     engine=pyttsx3.init()
     engine.say("your mesaage has been placed")
     engine.runAndWait()
     messagebox.showinfo("Title", "Thanks for choosing us!")


def calc_cost():
    global cost
    cost=40
    for order in orders:
        cost+=order[3]

def remove(rmv):
    global cost
    
    orders.pop(int(rmv)-1)
    show_cart_btn.configure(text="Show Cart("+str(len(orders))+")")

    top.destroy()
    show_cart(2)

def show_cart(h):
    global top

    top=Toplevel()
    center_window(top, window_width, window_height)

    top.geometry("400x400")
    top.title("CART")
    # Call the function to center the window
    n=0
    i=1
    top.grab_set()

    for order in orders:
        my_label1=Label(top,text=str(i)+". "+order[1]).grid(row=n,column=0,sticky="w",columnspan=4,pady=1)
        my_label2=Label(top,text="\t\tRs."+str(order[3])+"\n").grid(row=n,column=2,sticky="w")
        n+=1
        i+=1
    deliv=Label(top,text="Delivery: Rs.40")
    deliv.grid(row=n+1,column=2,sticky="e")
    calc_cost()
    total=Label(top,text="TOTAL: Rs."+str(cost),font=10)
    total.grid(row=n+2,column=2,sticky="e")

    remove_btn=Button(top,text="Remove Item",command=lambda:remove(remove_entry.get()))
    remove_btn.grid(row=n+3,column=0,sticky="w",columnspan=1)

    global remove_entry
    remove_entry=Entry(top,width=5,borderwidth=5,relief="sunken")
    remove_entry.grid(row=n+3,column=1,sticky="w")

    back1_btn=Button(top,text="Back",command=lambda:top.destroy())
    back1_btn.grid(row=n+4,column=0,sticky="w",pady=10)

    place_order=Button(top,text="Place Order",command=lambda:message())
    place_order.grid(row=n+4,column=1,padx=10,sticky="w")

def cart(id):
    # CALIING DATABASE
    # create a database or connect to one
    conn=sqlite3.connect('database_new.db')
    # create cursor
    c=conn.cursor()

    c.execute("SELECT *,rowid FROM "+city+" WHERE rowid="+str(id))
    selected=c.fetchall()
    print(selected)
    # commit change
    conn.commit()
    # close connection
    conn.close()
    print(selected[0])
    orders.append(selected[0]) 

    if(len(orders)): 
        show_cart_btn["state"]=NORMAL
    show_cart_btn.configure(text="Show Cart("+str(len(orders))+")")



def rstrnt(z,x):
    print(type(z))
    for widget in root.winfo_children():
        widget.grid_forget()
    sel_rstrnt=''

    for item in items:
        y=str(item[6])
        if(z==y):
            sel_rstrnt=item[0]
            print(sel_rstrnt)

    # CALIING DATABASE
    # create a database or connect to one
    conn=sqlite3.connect('database_new.db')
    # create cursor
    c=conn.cursor()
    # Query the database
    c.execute("SELECT *,rowid FROM "+city+" WHERE r_name="+f"'{sel_rstrnt}'")
    menu=c.fetchall()
    print(menu)
    # commit change
    conn.commit()
    # close connection
    conn.close()

    my_label=Label(root,text=sel_rstrnt,font=(50))
    my_label.grid(row=0,column=1,sticky="e",pady=5,padx=5,columnspan=4)
    
    khana=StringVar()
    n=1
    for food in menu:
        k=50-len(food[1])
        Radiobutton(root,text=food[1],value=food[6],variable=khana).grid(row=n,column=0,pady=2,sticky="w")
        label=Label(root,text="Rs."+str(food[3]))
        label.grid(row=n,column=5,sticky="w")
        n+=1
    khana.set(z)
    add_cart=Button(root,text="Add Item",command=lambda:cart(khana.get()))
    add_cart.grid(row=2*n+2,column=3,sticky="e")

    back_btn=Button(root,text="Back",command=lambda:dish_category(x))
    back_btn.grid(row=2*n+2,column=0,sticky="w",pady=10)



    global show_cart_btn
    show_cart_btn=Button(root,text="Show Cart(0)",command=lambda:show_cart(1))
    show_cart_btn.grid(row=2*n+2,column=4)
    
    if(len(orders)==0):
        show_cart_btn["state"]=DISABLED


def open():
    for widget in root.winfo_children():
            widget.grid_forget()
    root.configure(bg="white")

    # Call the function to center the window

    center_window(root, window_width, window_height)
    
    # top=Toplevel(root)
    root.geometry("200x150")
    def get_city():
        global city
        city=clicked.get()
        # top.destroy()
        main_window()



    
    myLabel=Label(root,text="Please!! Select your city")
    myLabel.grid(row=0,column=2)


    option=[
        "Jalandhar",
        "Chandigarh",
        "Patiala",
        "Bathinda",
        
        
    ]
    clicked=StringVar()
    clicked.set(option[0])

    drop=OptionMenu(root,clicked,*option)
    drop.grid(row=2,column=2,padx=50)

    my_button=Button(root,text="OK",command=lambda:get_city())
    my_button.grid(row=4,column=2)


def dish_category(x):
    root.geometry("600x600")
    root.configure(bg="#5e3e5a")
    orders.clear()
    cost=0
    print(city)
    
    for widget in root.winfo_children():
        widget.grid_forget()

    # CALIING DATABASE
    # create a database or connect to one
    conn=sqlite3.connect('database_new.db')
    # create cursor
    c=conn.cursor()
    # Query the database
    c.execute("SELECT *,rowid FROM "+city+" WHERE d_category="+f"'{x}'")
    global items
    items=c.fetchall()
    print(items)
    # commit change
    conn.commit()
    # close connection
    conn.close()

    dish=StringVar()
    n=0
    for item in items:
        Radiobutton(root,text=item[1],value=item[6],variable=dish).grid(column=0,sticky="w",pady=3)
        label1=Label(root,text="....."+item[0])
        label1.grid(row=n,column=3,sticky="e")
        label2=Label(root,text="Rs."+str(item[3])).grid(row=n,column=6,sticky="w")
        n+=1
    
    dish.set(items[0][6])
    
    open_rstrnt=Button(root,text="Open Restaurant",command=lambda:rstrnt(dish.get(),x))
    open_rstrnt.grid(row=2*n+2,column=5,sticky="e")

    back_btn=Button(root,text="Back",command=lambda:back_m(),width=10)
    back_btn.grid(row=2*n+2,column=0,sticky="w",pady=5)
    
def back_m():
        for widget in root.winfo_children():
            widget.grid_forget()
        main_window()

def main_window():
    for widget in root.winfo_children():
            widget.grid_forget()

    root.configure(bg="white")
    
    root.geometry("500x520")


    my_pic=Image.open("images/pizza.jpg")
    resized=my_pic.resize((120,120))
    global new_pic
    new_pic=ImageTk.PhotoImage(resized)


    my_pic1=Image.open("images/burger.jpg")
    resized1=my_pic1.resize((120,120))
    global new_pic1
    new_pic1=ImageTk.PhotoImage(resized1)

    my_pic2=Image.open("images/noodles.jpg")
    resized2=my_pic2.resize((120,120))
    global new_pic2
    new_pic2=ImageTk.PhotoImage(resized2)

    my_pic3=Image.open("images/pasta.jpg")
    resized3=my_pic3.resize((120,120))
    global new_pic3
    new_pic3=ImageTk.PhotoImage(resized3)

    my_pic4=Image.open("images/sandwich.jpg" )
    resized4=my_pic4.resize((120,120))
    global new_pic4
    new_pic4=ImageTk.PhotoImage(resized4)

    my_pic5=Image.open("images/thali.jpg")
    resized5=my_pic5.resize((120,120))
    global new_pic5
    new_pic5=ImageTk.PhotoImage(resized5)

    my_pic6=Image.open("images/soup.jpg")
    resized6=my_pic6.resize((120,120))
    global new_pic6
    new_pic6=ImageTk.PhotoImage(resized6)

    my_pic7=Image.open("images/beverages.jpg")
    resized7=my_pic7.resize((120,120))
    global new_pic7
    new_pic7=ImageTk.PhotoImage(resized7)


    #CREATE BUTTONS
    pizza_btn=Button(root,image=new_pic,command=lambda: dish_category("pizza"),borderwidth=0)
    pizza_btn.grid(row=1,column=0,pady=20)
    burger_btn=Button(root,command=lambda: dish_category("burger"),image=new_pic1,borderwidth=0)
    burger_btn.grid(row=1,column=1,padx=20)
    NOODLES_btn=Button(root,command=lambda: dish_category("noodles"),image=new_pic2,borderwidth=0)
    NOODLES_btn.grid(row=1,column=2,padx=20)
    pasta_btn=Button(root,command=lambda: dish_category("pasta"),image=new_pic3,borderwidth=0)
    pasta_btn.grid(row=2,column=0,pady=20,padx=20)
    sandwich_btn=Button(root,command=lambda: dish_category("sandwich"),image=new_pic4,borderwidth=0)
    sandwich_btn.grid(row=2,column=1,padx=20)
    thali_btn=Button(root,command=lambda: dish_category("thali"),image=new_pic5,borderwidth=0)
    thali_btn.grid(row=2,column=2,padx=20)
    soup_btn=Button(root,command=lambda: dish_category("soup"),image=new_pic6,borderwidth=0)
    soup_btn.grid(row=3,column=0,pady=20,padx=20)
    beverages_btn=Button(root,command=lambda: dish_category("beverages"),image=new_pic7,borderwidth=0)
    beverages_btn.grid(row=3,column=1,padx=20)

    sel_city_btn=Button(root,text="Select city again",command=lambda:open())
    sel_city_btn.grid(row=4,column=0)

def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates for the Tkinter window to be centered
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    # Set the geometry of the window to the specified width, height, and calculated x, y position
    window.geometry(f"{width}x{height}+{x}+{y}")



# Define the size of the window
window_width = 600
window_height = 600



open()


global orders
orders=[]
global cost
cost=0












root.mainloop()

