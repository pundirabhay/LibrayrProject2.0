import string
from tkinter import *
import sqlite3
from datetime import datetime
from tkinter import messagebox
import random
from tkinter.ttk import  Style, Treeview
import gmail
import smtplib
import re



current_date  = datetime.now()

win = Tk()
win.state("zoomed")   #it will set the window on full screen
win.resizable(width = False, height = False)
win.configure(bg="#F9F5F6")

try:
    con = sqlite3.connect(database="library.sqlite")
    cur = con.cursor()
    cur.execute("create table users(first_name text, last_name text, email text, contact_no text, password text,joindate text)")
    cur.execute("create table dashboard(Book_ID text, subject text, Author text, Num_of_Copies integer)")
    cur.execute("create table BookIssued(Name text, department text, subject text, author text, Num_of_Copies integer)")
    con.commit()

except Exception as e:
    print("error", e)
con.close()

def main_screen():
    frm = Frame(win)
    frm.configure(bg = "#F8E8EE")
    frm.place(x=0,y=0, relwidth=1.0, relheight=1.0)

    def acn_create():
        frm.destroy()
        acn_create_frm()

    def open_acn():
        frm.destroy()
        open_acn_screen()



    lbl_title = Label(frm, text="RAM library Management System",fg="black", bg="#F8E8EE",font=("Cambria", 40, "bold", "underline"))
    lbl_title.pack()

    lbl_stf = Label(frm, text="Staff Login or Signup page", fg="black", bg="#F8E8EE",font=("Monaco", 25, "bold",))
    lbl_stf.pack()
    lbl_stf.place(relx=.02, rely=.2)

    create_acn_btn = Button(frm,text="Create An Account",bg="powder blue",fg="black",command=acn_create, font=("Chalkboard", 20, 'bold'))
    create_acn_btn.pack()
    create_acn_btn.place(relx=.03, rely=.3)

    create_login_btn = Button(frm, text="Login", bg="powder blue", fg="black",command=open_acn, font=("Chalkboard", 20, 'bold'))
    create_login_btn.pack()
    create_login_btn.place(relx=.22, rely=.3)

def acn_create_frm():
        frm = Frame(win)
        frm.configure(bg="#F9F5F6")
        frm.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        def back_btn():
            frm.destroy()
            main_screen()

        def valid_password(password):
            pattern = r"[a-zA-Z0-9]"
            if re.match(pattern, password):
                return True
            else:
                return False

        def validate_gmail_address(email):
            pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
            if re.match(pattern, email):
                return True
            else:
                return False

        def open_account():
            name_f = first_name_entry.get()
            name_l = last_name_entry.get()
            email = email_entry.get()
            contact_num = no_entry.get()
            pwd = pwd_entry.get()
            open_date = current_date.strftime("%d/%m/%Y")

            if not valid_password(pwd):
                messagebox.showerror("Password", "Password is invalid. It must contain upper and lower case letters.")
                return

            if not validate_gmail_address(email):
                messagebox.showerror("Email", "Email is invalid.")
                return

            if len(contact_num) <= 9:
                messagebox.showerror("Contact Number", "Contact number should have at least 10 digits.")
                return

            if name_f == "" or name_l == "" or email == "" or contact_num == "" or pwd == "":
                messagebox.showwarning("Empty Fields", "Entries should not be empty.")
            else:
                con = sqlite3.connect(database="library.sqlite")
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO users (first_name, last_name, email, contact_no, password, joindate) VALUES (?,?,?,?,?,?)",
                    (name_f, name_l, email, contact_num, pwd, open_date))
                con.commit()
                con.close()
                messagebox.showinfo("Account Created", "Account created successfully.")

                first_name_entry.delete(0, "end")
                last_name_entry.delete(0, "end")
                email_entry.delete(0, "end")
                no_entry.delete(0, "end")
                pwd_entry.delete(0, "end")
                first_name_entry.focus()

        def reset():
            first_name_entry.delete(0, "end")
            last_name_entry.delete(0, "end")
            email_entry.delete(0, "end")
            no_entry.delete(0, "end")
            pwd_entry.delete(0, "end")
            first_name_entry.focus()

        back_button = Button(frm, text="⬅️", bg="powder blue", fg="black", command=back_btn,borderwidth=0,font=("Monaco", 20, 'bold'))
        back_button.pack()
        back_button.place(relx=0, rely=.01)

        new_lbl = Label(frm, text="STAFF SIGNUP", fg="black", bg="#F9F5F6", font=("Monaco", 35, "bold",))
        new_lbl.pack()
        new_lbl.place(relx=.4, rely=.01)

        new_lbl_1 = Label(frm, text="PLEASE ENTER YOUR DETAILS", fg="black", bg="#F9F5F6", font=("Monaco", 30, "bold",))
        new_lbl_1.pack()
        new_lbl_1.place(relx=.33, rely=.09)

        first_name_lbl = Label(frm, text="First Name :-", fg="black", bg="#F9F5F6", font=("Batang", 25, "bold",))
        first_name_lbl.pack()
        first_name_lbl.place(relx=.2, rely=.2)
        first_name_entry = Entry(frm,fg="black",font=("Cambria",20,"bold"),width=45, bg="white")
        first_name_entry.place(relx=.31,rely=.2)
        first_name_entry.focus()

        last_name_lbl = Label(frm, text="Last Name :-", fg="black", bg="#F9F5F6", font=("Batang", 25, "bold",))
        last_name_lbl.pack()
        last_name_lbl.place(relx=.2, rely=.3)
        last_name_entry = Entry(frm,fg="black", font=("Cambria", 20, "bold"), width=45, bg="white")
        last_name_entry.place(relx=.31, rely=.3)

        email_lbl = Label(frm, text="Email Add :-", fg="black", bg="#F9F5F6", font=("Batang", 25, "bold",))
        email_lbl.pack()
        email_lbl.place(relx=.2, rely=.4)
        email_entry = Entry(frm,bg="white",width=45,fg="black", font=("ariel",20,"bold"))
        email_entry.place(relx=.31, rely=.4)

        contact_nbrm = Label(frm, text="contact No :-", fg="black", bg="#F9F5F6", font=("Batang", 25, "bold",))
        contact_nbrm.pack()
        contact_nbrm.place(relx=.2, rely=.5)
        no_entry = Entry(frm, bg="white", width=45, fg="black", font=("ariel", 20, "bold"))
        no_entry.place(relx=.31, rely=.5)

        pwd_lbl = Label(frm, text="Password :-", fg="black", bg="#F9F5F6", font=("Batang", 25, "bold",))
        pwd_lbl.pack()
        pwd_lbl.place(relx=.2, rely=.6)
        pwd_entry = Entry(frm, bg="white", width=45, fg="black", font=("ariel", 20, "bold"))
        pwd_entry.place(relx=.31, rely=.6)

        create_btn = Button(frm, text="Create", bg="powder blue", fg="black",command=open_account,font=("Monaco", 20, 'bold'))
        create_btn.pack()
        create_btn.place(relx=.4, rely=.7)

        btn_reset = Button(frm, text="Reset", bg="powder blue", fg="black",command=reset, font=("Monaco", 20, 'bold'))
        btn_reset.pack()
        btn_reset.place(relx=.6, rely=.7)


def open_acn_screen():
        frm = Frame(win)
        frm.configure(bg="#F9F5F6")
        frm.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        def back_btn():
            frm.destroy()
            main_screen()

        def login_screen():
            email = email_entry_log.get()
            pwd = pwd_entry_log.get()
            if(email == "" or pwd == ""):
                messagebox.showerror("Login","Entries Can't Be Empty")
                return
            else:
                con = sqlite3.connect(database="library.sqlite")
                cur = con.cursor()
                cur.execute("select email,password from users where email=? and password=?",(email,pwd))
                row = cur.fetchone()
                if(row == None):
                    messagebox.showerror("login","user id password is wrong")
                else:
                    frm.destroy()
                    screen_login()

        def forgot_pwd_screen():
            forgot_screen()


        back_button = Button(frm, text="⬅️", bg="powder blue", fg="black", command=back_btn,borderwidth=0,font=("Monaco", 20, 'bold'))
        back_button.pack()
        back_button.place(relx=0, rely=.01)

        lbl_1 = Label(frm, text="Kindle Please Enter the details ", fg="black", bg="#F9F5F6", font=("Batang", 25, "bold",))
        lbl_1.pack()
        lbl_1.place(relx=.4, rely=.01)

        email_lbl = Label(frm, text="Email Add :-", fg="black", bg="#F9F5F6", font=("Batang", 25, "bold",))
        email_lbl.pack()
        email_lbl.place(relx=.2, rely=.2)
        email_entry_log = Entry(frm, bg="white", width=45, fg="black", font=("ariel", 20, "bold"))
        email_entry_log.place(relx=.3, rely=.2)
        email_entry_log.focus()

        pwd_lbl = Label(frm, text="Password :-", fg="black", bg="#F9F5F6", font=("Batang", 25, "bold",))
        pwd_lbl.pack()
        pwd_lbl.place(relx=.2, rely=.3)
        pwd_entry_log = Entry(frm, bg="white", width=45, fg="black",show="*", font=("ariel", 20, "bold"))
        pwd_entry_log.place(relx=.3, rely=.3)

        login_btn = Button(frm, text="Login", bg="powder blue", fg="black",command=login_screen, font=("Monaco", 20, 'bold'))
        login_btn.pack()
        login_btn.place(relx=.4, rely=.4)

        login_reset_btn = Button(frm, text="Forgot Password", bg="powder blue", fg="black",command=forgot_pwd_screen,font=("Monaco", 20, 'bold'))
        login_reset_btn.pack()
        login_reset_btn.place(relx=.5, rely=.4)

def screen_login():
    frm = Frame(win)
    frm.configure(bg="#F9F5F6")
    frm.place(x=0, y=0, relwidth=1.0, relheight=1.0)

    lib_lbl = Label(win, text='RAM Library', width=12, bg='#FCE9F1', fg='black', font=('Andale Mono', 40, 'italic'))
    lib_lbl.place(x=0, y=100)

    lbl_om = Label(win,text="🕉",bg="#F9F5F6", font=('Andale Mono', 80, 'italic'))
    lbl_om.place(relx=.0,rely=.0)

    lbl_ram = Label(win, text="RAM Library Management System", bg="#F9F5F6", fg="black", font=('Chalkboard', 70, 'italic', "underline"))
    lbl_ram.place(relx=.13, rely=.0)

    lbl_om = Label(win, text="🕉", bg="#F9F5F6", font=('Andale Mono', 80, 'italic'))
    lbl_om.place(relx=.94, rely=.0)

    def  d_board_btn_clicked():
        frm = Frame(win)
        frm.configure(bg="#F8E8EE")
        frm.place(relx=.22, rely=.13, relwidth=.78, relheight=.62)

        tv = Treeview(frm, style='Custom.Treeview')
        tv.place(x=0, y=0, relwidth=0.992, relheight=0.99)
        tv.tag_configure('ariel', background='#F8E8EE')

        style = Style()
        style.theme_use("default")
        style.configure("Custom.Treeview", background="white")

        tv['columns'] = ('col1','col2','col3','col4')

        tv.column('col1',width=100,anchor='c')
        tv.column('col2', width=150, anchor='c')
        tv.column('col3', width=150, anchor='c')
        tv.column('col4', width=150, anchor='c')

        tv.heading('col1',text='Book Id')
        tv.heading('col2', text='Subject')
        tv.heading('col3', text='Author Name')
        tv.heading('col4', text='Left Copies')

        tv['show'] = 'headings'

        con = sqlite3.connect(database="library.sqlite")
        cur = con.cursor()
        cur.execute('select * from dashboard')

        for row in cur:
            tv.insert("",'end', values=(row[0],row[1],row[2],row[3]),tags=('ariel'))


    def book_add():
        frm = Frame(win)
        frm.configure(bg="#F8E8EE")
        frm.place(relx=.22, rely=.13, relwidth=.78, relheight=.62)

        def add_book():
            subject = subject_entry.get()
            writer = author_entry.get()
            copy_number = copy_entry.get()

            if subject == "" or writer == "" or copy_number == "":
                messagebox.showwarning("entry","Entries never be empty")
            else:
                con = sqlite3.connect(database="library.sqlite")
                cur = con.cursor()
                for _ in range(1):
                    random_number = random.randint(100, 999)
                    random_alphabet = random.choice(string.ascii_letters)

                    combined = str(random_number) + random_alphabet

                cur.execute("insert into dashboard(book_id,subject,author,Num_of_copies) values (?,?,?,?)", (combined,subject, writer,copy_number))
                con.commit()
                con.close()
                messagebox.showinfo("Add Book", "book add successfully")

                subject_entry.delete(0,END)
                author_entry.delete(0,END)
                copy_entry.delete(0,END)
                subject_entry.focus()

        lbl_subject = Label(win,text="Subject :-", fg="black", bg="#F8E8EE", font=("Andale Mono",25,))
        lbl_subject.place(relx=.4, rely=.28)
        subject_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        subject_entry.place(relx=.51, rely=.28)

        author_lbl = Label(win,text="Author Name :-", fg="black", bg="#F8E8EE", font=("Andale Mono",25,))
        author_lbl.place(relx=.4, rely=.36)
        author_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        author_entry.place(relx=.55, rely=.36)

        copy_lbl = Label(win, text="Number Of Copies :-", fg="black", bg="#F8E8EE", font=("Andale Mono", 25,))
        copy_lbl.place(relx=.4, rely=.45)
        copy_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        copy_entry.place(relx=.6, rely=.45)

        add_btn = Button(frm, text="Add", bg="powder blue", fg="black",command=add_book,font=("Monaco", 20, 'bold'))
        add_btn.pack()
        add_btn.place(relx=.53, rely=.63)


    def book_withdraw():
        frm = Frame(win)
        frm.configure(bg="#F8E8EE")
        frm.place(relx=.22, rely=.13, relwidth=.78, relheight=.62)

        def essued_book():
            student_name = std_entry.get()
            student_dept = std_dept_entry.get()
            book_name = book_name_entry.get()
            author_name = author_name_entry.get()
            no_of_copies = std_num_entry.get()

            if(student_name == "", student_dept == "", book_name == "", author_name == "",no_of_copies == ""):
                messagebox.showwarning("Entry","Entries Never Be Empty")
            else:
                con = sqlite3.connect(database="library.sqlite")
                cur = con.cursor()
                cur.execute("insert into BookIssued (name,department,subject,author,Num_of_Copies) values (?,?,?,?,?)",(student_name,student_dept,book_name,author_name,no_of_copies))
                con.commit()
                con.close()
                messagebox.showinfo("essued","Book Issued Successfully 🥳")

                std_entry.delete(0,END)
                std_dept_entry.delete(0,END)
                book_name_entry.delete(0,END)
                book_name_entry.delete(0,END)
                author_name_entry.delete(0,END)
                std_num_entry.delete(0,END)
                std_entry.focus()

        std_name = Label(win, text="Name :-", bg="#F8E8EE", fg="black",font=('Chalkboard', 30, 'italic'))
        std_name.place(relx=.3, rely=.2)
        std_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        std_entry.place(relx=.38, rely=.21)

        std_dept = Label(win, text="Department :-", bg="#F8E8EE", fg="black", font=('Chalkboard', 30, 'italic'))
        std_dept.place(relx=.3, rely=.3)
        std_dept_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        std_dept_entry.place(relx=.44, rely=.31)

        book_name_lbl = Label(win, text="Subject :-", bg="#F8E8EE", fg="black", font=('Chalkboard', 30, 'italic'))
        book_name_lbl.place(relx=.3, rely=.4)
        book_name_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        book_name_entry.place(relx=.42, rely=.41)

        author_lbl = Label(win, text="Author Name :-", bg="#F8E8EE", fg="black", font=('Chalkboard', 30, 'italic'))
        author_lbl.place(relx=.3, rely=.5)
        author_name_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        author_name_entry.place(relx=.46, rely=.51)

        std_num = Label(win, text="No Of Copies:-", bg="#F8E8EE", fg="black", font=('Chalkboard', 30, 'italic'))
        std_num.place(relx=.3, rely=.6)
        std_num_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        std_num_entry.place(relx=.45, rely=.61)

        issue_btn = Button(frm, text="Issue", bg="powder blue", fg="black",command=essued_book, font=("Monaco", 20, 'bold'))
        issue_btn.pack()
        issue_btn.place(relx=.37, rely=.88)


    def  book_see():
        frm = Frame(win)
        frm.configure(bg="#F8E8EE")
        frm.place(relx=.22, rely=.13, relwidth=.78, relheight=.62)

        tv = Treeview(frm, style='Custom.Treeview')
        tv.place(x=0, y=0, relwidth=0.992, relheight=0.99)
        tv.tag_configure('ariel', background='#F8E8EE')

        style = Style()
        style.theme_use("default")
        style.configure("Custom.Treeview", background="#F8E8EE")


        tv['columns'] = ('col1','col2','col3','col4','col5')

        tv.column('col1',width=100,anchor='c')
        tv.column('col2', width=150, anchor='c')
        tv.column('col3', width=150, anchor='c')
        tv.column('col4', width=150, anchor='c')
        tv.column('col5', width=150, anchor='c')

        tv.heading('col1',text='Name')
        tv.heading('col2', text='Department')
        tv.heading('col3', text='Subject')
        tv.heading('col4', text='Author Name')
        tv.heading('col5', text='Num Of Copies')

        tv['show'] = 'headings'

        con = sqlite3.connect(database="library.sqlite")
        cur = con.cursor()
        cur.execute('select * from BookIssued ')
        for row in cur:
            tv.insert("",'end', values=(row[0],row[1],row[2],row[3],row[4]),tags=('ariel'))


    def view_std():
        frm = Frame(win)
        frm.configure(bg="#F8E8EE")
        frm.place(relx=.22, rely=.13, relwidth=.78, relheight=.62)

        tv = Treeview(frm, style='Custom.Treeview')
        tv.place(x=0, y=0, relwidth=0.992, relheight=0.99)
        tv.tag_configure('ariel', background='#F8E8EE')

        style = Style()
        style.theme_use("default")
        style.configure("Custom.Treeview", background="#F8E8EE")

        tv['columns'] = ('col1', 'col2', 'col3', 'col4','col5')

        tv.column('col1', width=100, anchor='c')
        tv.column('col2', width=150, anchor='c')
        tv.column('col3', width=150, anchor='c')
        tv.column('col4', width=150, anchor='c')
        tv.column('col5', width=150, anchor='c')

        tv.heading('col1', text='first Name')
        tv.heading('col2', text='Last Name')
        tv.heading('col3', text='Email')
        tv.heading('col4', text='Contact Number')
        tv.heading('col5', text='Join Date')

        tv['show'] = 'headings'

        con = sqlite3.connect(database="library.sqlite")
        cur = con.cursor()
        cur.execute('select * from users')
        for row in cur:
            tv.insert("", 'end', values=(row[0], row[1], row[2], row[3], row[5]), tags=('ariel'))

    def back_book():
        frm = Frame(win)
        frm.configure(bg="#F8E8EE")
        frm.place(relx=.22, rely=.13, relwidth=.78, relheight=.62)

        rtn_book_lbl = Label(win,text="Book ID :-",bg="#F8E8EE",fg="black", font=("Chalkboard", 20, 'bold'))
        rtn_book_lbl.place(relx=.38, rely=.21)
        rtn_book_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        rtn_book_entry.place(relx=.47, rely=.21)

        rtn_author_lbl = Label(win, text="Author Name :-", bg="#F8E8EE", fg="black", font=('Chalkboard', 20, 'bold'))
        rtn_author_lbl.place(relx=.38, rely=.31)
        rtn_author_name_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        rtn_author_name_entry.place(relx=.5, rely=.31)

        student_name_lbl = Label(win, text="Student Name :-", bg="#F8E8EE", fg="black", font=('Chalkboard', 20, 'bold'))
        student_name_lbl.place(relx=.38, rely=.41)
        student_name_lbl_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        student_name_lbl_entry.place(relx=.5, rely=.41)

        student_dept_lbl = Label(win, text="Student Department :-", bg="#F8E8EE", fg="black", font=('Chalkboard', 20, 'bold'))
        student_dept_lbl.place(relx=.38, rely=.51)
        student_dept_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        student_dept_entry.place(relx=.55, rely=.51)

        rtn_btn = Button(frm, text="Return", bg="powder blue", fg="black", font=("Monaco", 20, 'bold'))
        rtn_btn.pack()
        rtn_btn.place(relx=.5, rely=.74)

    def report_essue():
        frm = Frame(win)
        frm.configure(bg="#F8E8EE")
        frm.place(relx=.22, rely=.13, relwidth=.78, relheight=.62)

        def send_email():
            # Get the user's message from the message box
            user_message = message_entry.get("1.0", "end-1c")

            # Configure the SMTP server and sender's email
            smtp_server = "smtp.gmail.com"  # Change this for other email providers
            smtp_port = 587
            sender_email = "rg3394722@gmail.com"  # Replace with your email address
            sender_password = "qvwtjthzrxgprviv"  # Replace with your email password

            # Create the SMTP connection
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login('rg3394722@gmail.com', 'qvwtjthzrxgprviv')

                # Compose the email
                subject = "User Message"
                body = user_message
                message = f"Subject: {subject}\n\n{body}"

                # Send the email
                receiver_email = "pundirabhay987@gmail.com"  # Replace with recipient's email
                server.sendmail('rg3394722@gmail.com', 'pundirabhay987@gmail.com', message)
                server.quit()

                # Show a success message
                messagebox.showinfo("Email Sent", "Email sent successfully!")
            except smtplib.SMTPException as e:
                # Show an error message
                messagebox.showerror("Email Error", str(e))

        # Create a label for the message box
        message_label = Label(frm, text="Report an essue:")
        message_label.pack()
        message_label.place(relx=0.1, rely=0.001, relwidth=0.78, relheight=0.05)



        # Create a message box for user input
        message_entry = Text(frm, height=10, width=50)
        message_entry.configure(bg="white",fg='black', font=('Monaco',20,'bold'))
        message_entry.pack()
        message_entry.place(relx=0, rely=0.053, relwidth=0.999, relheight=0.9)

        # Create a button to send the email
        send_button =Button(frm, text="Send Email", command=send_email)
        send_button.place(relx=0.22, rely=0.999)
        send_button.pack(side='bottom')

    def booksearch():
        frm = Frame(win)
        frm.configure(bg="#F8E8EE")
        frm.place(relx=.22, rely=.13, relwidth=.78, relheight=.62)

        def SeacrhBook():
            book_n = book_name_entry.get()
            author_n = author_name_entry.get()
            if(book_n == "" or author_n == ""):
                messagebox.showerror("Entry","Entry can't Be Empty")
            else:
                con = sqlite3.connect(database="library.sqlite")
                cur = con.cursor()
                cur.execute("select subject, author from dashboard where subject =? and author = ?",(book_n,author_n))
                row = cur.fetchone()
                if(row == None):
                    messagebox.showerror("Entry","Book Not Found")
                else:
                    messagebox.showinfo("Book Found", f"Subject: {book_n}\nEmail: {author_n}")
                    book_name_entry.delete()
                    author_name_entry.delete()
                    book_name_entry.focus()


        book_name = Label(win, text="Subject :-", bg="#F8E8EE", fg="black", font=("Chalkboard", 20, 'bold'))
        book_name.place(relx=.38, rely=.21)
        book_name_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        book_name_entry.place(relx=.48, rely=.21)

        author_name = Label(win, text="Author Name :-", bg="#F8E8EE", fg="black", font=("Chalkboard", 20, 'bold'))
        author_name.place(relx=.38, rely=.31)
        author_name_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
        author_name_entry.place(relx=.49, rely=.31)

        search_btn = Button(frm, text="Search", bg="powder blue", fg="black",command=SeacrhBook, font=("Monaco", 20, 'bold'))
        search_btn.pack()
        search_btn.place(relx=.43, rely=.4)

    def logout_frm():
        messagebox.showwarning("logout","You really want to logut")
        frm.destroy()
        main_screen()


    d_board_btn = Label(win, text='👉 Dashboard', width=12, bg='#FCE9F1', fg='black', font=('Andale Mono', 40, 'italic'))
    d_board_btn.bind("<Button-1>", lambda event: d_board_btn_clicked())
    d_board_btn.pack()
    d_board_btn.place(x=0, y=153)

    book_btn = Label(win, text='📕 AddBook', width=12, bg='#FCE9F1', fg='black', font=('Andale Mono', 40, 'italic'))
    book_btn.bind("<Button-1>", lambda event: book_add())
    book_btn.pack()
    book_btn.place(x=0, y=206)

    book_iss = Label(win, text='🖇️ IssueBook', width=12, bg='#FCE9F1', fg='black', font=('Andale Mono', 40, 'italic'))
    book_iss.bind("<Button-1>", lambda event: book_withdraw())
    book_iss.pack()
    book_iss.place(x=0, y=259)

    book_iss = Label(win, text='✅Issued Book', width=12, bg='#FCE9F1', fg='black', font=('Andale Mono', 40, 'italic'))
    book_iss.bind("<Button-1>", lambda event: book_see())
    book_iss.pack()
    book_iss.place(x=0, y=312)

    see_std = Label(win, text='👨‍🎓Students', width=12, bg='#FCE9F1', fg='black', font=('Andale Mono', 40, 'italic'))
    see_std.bind("<Button-1>", lambda event: view_std())
    see_std.pack()
    see_std.place(x=0, y=365)

    rtn_book = Label(win, text='🔁Return Book', width=12, bg='#FCE9F1', fg='black', font=('Andale Mono', 40, 'italic'))
    rtn_book.bind("<Button-1>", lambda event: back_book())
    rtn_book.pack()
    rtn_book.place(x=0, y=418)

    report = Label(win, text='❗️Report', width=12, bg='#FCE9F1', fg='black', font=('Andale Mono', 40, 'italic'))
    report.bind("<Button-1>", lambda event: report_essue())
    report.pack()
    report.place(x=0, y=470)

    report = Label(win, text='SearchBook', width=12, bg='#FCE9F1', fg='black', font=('Andale Mono', 40, 'italic'))
    report.bind("<Button-1>", lambda event: booksearch())
    report.pack()
    report.place(x=0, y=522)

    logout_lbl = Label(win, text='Logout', width=12, bg='#FCE9F1', fg='black', font=('Andale Mono', 40, 'italic'))
    logout_lbl.bind("<Button-1>", lambda event: logout_frm())
    logout_lbl.pack()
    logout_lbl.place(x=700, y=580)

def forgot_screen():
    frm = Frame(win)
    frm.configure(bg="#F8E8EE")
    frm.place(relx=.0, rely=.0, relwidth=.999, relheight=.99)

    def back():
        frm.destroy()
        main_screen()

    def send_otp():
        email = user_email_id_entry.get()
        phone_num = user_phone_number_entry.get()

        con = sqlite3.connect(database="library.sqlite")  # connection for gettting otp from the database
        cur = con.cursor()
        cur.execute("select email,password from users where contact_no = ?",(phone_num,))
        row = cur.fetchone()
        if(row == None):
            messagebox.showerror("Password Recovery","Phone Number is wrong")
        else:
            if(row[0]==email):
                otp_r = random.randint(1000,9999)
                try:
                    con = gmail.GMail("pundirabhay987@gmail.com","ozbeopkdufeirdcd")
                    msg = gmail.Message(to = email,subject='opt verification', text =f'your otp is:- {otp_r}' )
                    con.send(msg)
                    messagebox.showinfo("Password Recovery", 'OTP sent')
                except:
                    messagebox.showerror("Password Recovery","something went wrong")

                lbl_forgot_otp = Label(win, text="OTP :-", bg="#F8E8EE", fg="black", font=("Chalkboard", 20, 'bold'))
                lbl_forgot_otp.place(relx=.37, rely=.5)
                entry_otp = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
                entry_otp.place(relx=.44, rely=.5)
                def otp_get():
                    verify_otp = int(entry_otp.get())
                    if (otp_r == verify_otp):
                        messagebox.showinfo("Password Recovery",f"your password is:-{row[1]} ")

                    else:
                        messagebox.showerror("Password Recovery","OTP is wrong")

                gen_otp_btn = Button(win, text="Get Password", bg="powder blue", fg="black",command=otp_get,font=("Monaco", 20, 'bold'))
                gen_otp_btn.pack()
                gen_otp_btn.place(relx=.49, rely=.6)



            else:
                messagebox.showerror("Password Recovery", "Email is wrong")
        con.close()
    back_button = Button(frm, text="⬅️", bg="powder blue", fg="black", command=back, borderwidth=0, font=("Monaco", 20, 'bold'))
    back_button.pack()
    back_button.place(relx=0, rely=.01)

    lbl_title = Label(win, text="Kindly Please Enter all the details", bg="#F8E8EE", fg="black", font=("Chalkboard", 20, 'bold'))
    lbl_title.place(relx=.39, rely=.01)

    user_email_id = Label(win, text="Email Id :-", bg="#F8E8EE", fg="black", font=("Chalkboard", 20, 'bold'))
    user_email_id.place(relx=.35, rely=.21)
    user_email_id_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
    user_email_id_entry.place(relx=.44, rely=.21)

    user_phone_number = Label(win, text="Phone No.:-", bg="#F8E8EE", fg="black", font=("Chalkboard", 20, 'bold'))
    user_phone_number.place(relx=.35, rely=.31)
    user_phone_number_entry = Entry(win, bg="white", width=20, fg="black", font=("ariel", 20, "bold"))
    user_phone_number_entry.place(relx=.44, rely=.31)

    gen_btn = Button(frm, text="Generate OTP", bg="powder blue", fg="black",command=send_otp, font=("Monaco", 20, 'bold'))
    gen_btn.pack()
    gen_btn.place(relx=.49, rely=.4)


main_screen()
win.mainloop()