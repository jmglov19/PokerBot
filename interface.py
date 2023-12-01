import tkinter
import random
from tkinter import ttk
import sqlite3
import secrets

def load_frame():
    frame_choice = selector_combobox.get()

    if frame_choice == "New Instrument":
        instrument_frame()
    if frame_choice == "New Customer":
        new_customer_frame()
    if frame_choice == "Show Records":
        show_records()
    if frame_choice == "Add Ticket":
        add_ticket_frame()

def add_customers_csv():
    return
def add_instruments_csv():
    return


window = tkinter.Tk()
window.title("Rental Program Database")

frame = tkinter.Frame(window)
frame.pack()


# This frame is the basic frame that opens when the program is run. It stays at the top and changes the frame
# to a fram that is selected
frame_selector = tkinter.LabelFrame(frame, text= "Frame Selector")
frame_selector.grid(row=0, column=0, sticky= "news", padx= 20, pady= 10)

# List of possisible choices
frames = ["New Instrument", "New Customer", "Show Records", "Add Ticket"]

selector_combobox = ttk.Combobox(frame_selector, values= frames )
selector_combobox.grid(row= 0, column= 0, padx= 20, pady= 10)

selector_button = tkinter.Button(frame_selector, text= "Load Frame", command= load_frame)
selector_button.grid(row=0, column=1, padx= 20, pady= 10)

add_customers_csv_button = tkinter.Button(frame_selector, text= "Custmers CSV", command= add_customers_csv)
add_instruments_csv_button = tkinter.Button(frame_selector, text= "Instruments CSV", command= add_instruments_csv)

add_customers_csv_button.grid(row= 0, column= 2, padx= 20, pady= 10)
add_instruments_csv_button.grid(row= 0, column= 3, padx= 20, pady= 10)



# This frame is used for adding one instrument at a time to the data base. This can be useful for when only a new 
# instruments need to be added it can be quickly done this way.

def instrument_frame():
    def enter_instrument_data():
       

        serial_num = serial_num_entry.get()
        instrument_type = instrument_combobox.get()
        brand = brand_entry.get()

        if (instrument_type == "Alto Saxophone"):
            cost = 169.00
        else:
            cost = 139.00
        status = status_combobox.get()


        conn = sqlite3.connect('test.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Instrument (                        
                                    serial_num Varchar(10),
                                    instrument Varchar(15),
                                    brand Varchar(10),
                                    cost double precision,
                                    status Varchar(8),
                                    PRIMARY KEY (serial_num)
                                );'''
        conn.execute(table_create_query)
        
        # Insert Data
        insert_data_query = '''Insert INTO Instrument (serial_num, instrument, brand, cost, status) VALUES
                            ( ?, ?, ?, ?, ?)'''
        
        data_tuple = (serial_num, instrument_type, brand, cost, status)
        
        cursor = conn.cursor()
        cursor.execute(insert_data_query, data_tuple)
        conn.commit()
        conn.close()



        #print(serial_num, instrument_type, brand, cost, status)
    # Add an Instrument
    instrument_addition_frame = tkinter.LabelFrame(frame, text= "Add an Instrument")
    instrument_addition_frame.grid(row= 1, column= 0, sticky= "news", padx= 20, pady= 10)

    instrument_types = ["Flute", "Clarinet", "Alto Saxophone", "Trumpet", "Percussion Kit"]

    instrument_label = tkinter.Label(instrument_addition_frame, text= "Instrument")
    brand_label = tkinter.Label(instrument_addition_frame, text= "Brand")
    serial_num_lablel = tkinter.Label(instrument_addition_frame, text= "Serial Number")
    status_label = tkinter.Label(instrument_addition_frame, text= "Status")

    instrument_label.grid(row= 0, column= 0)
    brand_label.grid(row= 0, column= 1)
    serial_num_lablel.grid(row=0, column= 2)
    status_label.grid(row= 0, column= 3)

    instrument_combobox = ttk.Combobox(instrument_addition_frame, values= instrument_types)
    brand_entry = tkinter.Entry(instrument_addition_frame)
    serial_num_entry = tkinter.Entry(instrument_addition_frame)
    status_combobox = ttk.Combobox(instrument_addition_frame, values=["Ready", "Out", "Repair"])

    instrument_combobox.grid(row= 1, column= 0)
    brand_entry.grid(row= 1, column= 1)
    serial_num_entry.grid(row= 1, column= 2)
    status_combobox.grid(row= 1, column= 3)

    for widget in instrument_addition_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    # Button
    button = tkinter.Button(instrument_addition_frame, text="Enter data", command= enter_instrument_data)
    button.grid(row=2, column=0, sticky="news", padx=20, pady=10)


# This frame is used for adding a customer to the data base. They are given a unique ID and their personal info
# is stored here
def new_customer_frame():

    def enter_customer_data():
        customerID = secrets.token_hex(4)

        parent = parent_entry.get()
        student = student_entry.get()
        street = street_entry.get()
        city = city_entry.get()
        zipcode = zipcode_entry.get()
        homephone = homephone_entry.get()
        workphone = workphone_entry.get()
        school = school_entry.get()

        conn = sqlite3.connect('test.db')
        customer_table_create_query = '''CREATE TABLE IF NOT EXISTS Renter (
                                customerID Varchar(8),
                                parent_name Varchar(20),
                                student_name Varchar(20),
                                street Varchar(20),
                                city Varchar(10),
                                zipcode Varchar(5),
                                home_phone Varchar(10),
                                work_phone Varchar(10),
                                school Varchar(15),
                                PRIMARY KEY (customerID)
                                );'''
        conn.execute(customer_table_create_query)
        
        # Insert Data
        insert_data_query = '''Insert INTO Renter (customerID, parent_name, student_name, street, city, zipcode, home_phone,
                                work_phone, school) VALUES
                            (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        data_tuple = (customerID, parent, student, street, city, zipcode, homephone, workphone, school)
        
        cursor = conn.cursor()
        cursor.execute(insert_data_query, data_tuple)
        conn.commit()
        conn.close()



        print(customerID, parent, student, street, city, zipcode, homephone, workphone, school)
    


    # Add Customer
    Customer_add_frame = tkinter.LabelFrame(frame, text= "New Customer")
    Customer_add_frame.grid(row= 1, column= 0, sticky= "news", padx= 20, pady= 10)

    parent_label = tkinter.Label(Customer_add_frame, text= "Guardian's Name")
    student_label = tkinter.Label(Customer_add_frame, text= "Student's Name")
    street_label = tkinter.Label(Customer_add_frame, text= "Street Address")
    city_label = tkinter.Label(Customer_add_frame, text= "City")
    zipcode_label = tkinter.Label(Customer_add_frame, text= "Zipcode")
    homephone_label = tkinter.Label(Customer_add_frame, text= "Home Phone #")
    workphone_label = tkinter.Label(Customer_add_frame, text= "Work Phone # (Optional)")
    school_label = tkinter.Label(Customer_add_frame, text="School")





    parent_entry= tkinter.Entry(Customer_add_frame)
    student_entry= tkinter.Entry(Customer_add_frame)
    street_entry= tkinter.Entry(Customer_add_frame)
    city_entry= tkinter.Entry(Customer_add_frame)
    zipcode_entry= tkinter.Entry(Customer_add_frame)
    homephone_entry= tkinter.Entry(Customer_add_frame)
    workphone_entry= tkinter.Entry(Customer_add_frame)
    school_entry= tkinter.Entry(Customer_add_frame)

    # First Row
    parent_label.grid(row=0, column=0)
    student_label.grid(row=0, column= 1)
    school_label.grid(row=0, column= 2)
    parent_entry.grid(row=1, column=0)
    student_entry.grid(row=1, column=1)
    school_entry.grid(row=1, column=2)

    # Second Row (Address)
    street_label.grid(row=2, column=0)
    city_label.grid(row=2, column=1)
    zipcode_label.grid(row=2, column=2)
    street_entry.grid(row=3, column=0)
    city_entry.grid(row=3, column=1)
    zipcode_entry.grid(row=3, column=2)

    # Third Row (Phone #)
    homephone_label.grid(row=4, column=0)
    workphone_label.grid(row=4, column= 1)
    homephone_entry.grid(row=5, column=0)
    workphone_entry.grid(row=5, column=1)


    for widget in Customer_add_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    # Button
    customer_button = tkinter.Button(Customer_add_frame, text="Enter data", command= enter_customer_data)
    customer_button.grid(row=6, column=0, sticky="news", padx=20, pady=10)


# This frame is used to search up information in that data base. Things such as what is the status of certian instruments,
# How many instruments are available, and who has what instruments
def show_records():
    
    def query_format(query):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()  
        c.execute(query)
        customers = c.fetchall()

        print_customers = ''
        for customer in customers:
            print_customers += str(customer) + "\n"
        
        
        itemsA = print_customers.split("\n")
        #for i in itemsA:

        #print(itemsA)
        query_label["text"] = print_customers
        item_combobox["values"] = itemsA

        conn.commit()
        conn.close()
    
    def edit_fromat(edit):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()  
        c.execute(edit)
        conn.commit()
        conn.close()

    

    def show_customers():
        
        entry = customer_entry.get()
        search = customers_combobox.get()
        option = customer_info_combobox.get()

        if option == "Information":   
            customer_info_query = """ SELECT *   
                            FROM Renter
                            WHERE """ + search + """ LIKE '"""  + entry + """%'    
                    """
            query_format(customer_info_query)
            item_actions["values"] = ["Remove"]
            
        
        elif option == "Tickets":
            customer_ticket_query = """ select Renter.parent_name, Renter.student_name, t.instrument, t.serial_num, t.status, t.paid, t.RentID
                                from (select RT.rentID, Instrument.instrument, customerID, RT.status, instrument.serial_num, RT.paid
                                        from Instrument
                                        inner join Rented_Ticket RT on Instrument.serial_num = RT.serial_num) as t
                                inner join Renter on t.customerID = Renter.customerID
                                WHERE """ + search + """ LIKE '"""  + entry + """%'    
                        """
            query_format(customer_ticket_query)
            item_actions["values"] = ["Returned", "Out", "Remove", "Paid", "Not Paid"]


    def show_instruments():  
        instrument = instrument_entry.get()
        instrument_entry.delete(0, 20)
        insrument_query = """ SELECT *
                            FROM Instrument
                            Where instrument LIKE '""" + instrument + """%' 
                            Limit 10      
        """
        query_format(insrument_query)

    def show_open_instruments():
        open_instruments_query = """ select instrument, count() from Instrument
                                    where status = 'Ready'
                                    group by instrument"""
        query_format(open_instruments_query)

    def execute_command():
        edit = ""
        customer_option = customer_info_combobox.get()
        if customer_option == "Information":
            id = item_combobox.get()
            id = id.split("'", 2)[1]
            #print(id)
           
            command = item_actions.get()
            if command == "Remove":
                edit = "DELETE FROM Renter WHERE customerID = '" + id + "';"
                edit_fromat(edit)
                edit = "DELETE FROM Rented_Ticket WHERE customerID = '" + id + "';"
                edit_fromat(edit)
            
            show_customers()


        elif customer_option == "Tickets":
            id = item_combobox.get()
            id = id[-10:-2]
            #print(id)
            command = item_actions.get()
            if command == "Returned":
                edit = "UPDATE Rented_Ticket SET status = 'Returned' WHERE rentID = '" + id + "';"
            if command == "Out":
                edit = "UPDATE Rented_Ticket SET status = 'Out' WHERE rentID = '" + id + "';"
            if command == "Paid":
                edit = "UPDATE Rented_Ticket SET paid = 'Paid' WHERE rentID = '" + id + "';"
            if command == "Not Paid":
                edit = "UPDATE Rented_Ticket SET paid = 'Not Paid' WHERE rentID = '" + id + "';"
            if command == "Remove":
                edit = "DELETE FROM Rented_Ticket WHERE rentID = '" + id + "';"
            
            edit_fromat(edit)
            show_customers()
    
    show_records_frame = tkinter.LabelFrame(frame, text= "Show Records")
    show_records_frame.grid(row= 1, column= 0, sticky= "news", padx= 20, pady= 10)
    

    # Information to finding customer information
    customers_button = tkinter.Button(show_records_frame, text="Search Customers", command= show_customers)
    customer_entry = tkinter.Entry(show_records_frame)
    customer_options = ["customerID", "parent_name" ,"student_name", "street", "city", "zipcode", "home_phone", "work_phone", "school" ]
    customers_combobox = ttk.Combobox(show_records_frame, values= customer_options)
    customer_info_combobox = ttk.Combobox(show_records_frame, values= ["Information", "Tickets"])
    customers_button.grid(row= 1, column=0)
    customers_combobox.grid(row= 1, column= 2)
    customer_info_combobox.grid(row= 1, column= 1)
    customer_entry.grid(row=1, column=3)



    instrument_button = tkinter.Button(show_records_frame, text="Search Instruments", command= show_instruments)
    instrument_entry = tkinter.Entry(show_records_frame)

    

    show_open_instruments_btn = tkinter.Button(show_records_frame, text= "Show how many available instruments", command= show_open_instruments)
    show_open_instruments_btn.grid(row=3, column= 0)

    items = []
    actions = []
    item_combobox = ttk.Combobox(show_records_frame, values= items)
    item_actions = ttk.Combobox(show_records_frame, values = actions)
    item_execute = tkinter.Button(show_records_frame, text= "Execute", command= execute_command)

    item_combobox.grid(row=3, column=1)
    item_actions.grid(row=3, column=2)
    item_execute.grid(row=3, column= 3)


    instrument_button.grid(row=2, column=0)
    instrument_entry.grid(row=2, column= 1)
    query_label = tkinter.Label(show_records_frame, text= "")
    query_label.grid(row=4, column=0, columnspan=4, padx= 10, pady= 10)

    for widget in show_records_frame.winfo_children():
        widget.grid_configure(padx=5, pady=5)


# The add ticket frame is for selecting a student and an instrument and creating a ticket
# for them that assings the instrument to that student, and changes the status of that instrument of the student to out
# This is just used for assigning instruments to students
def add_ticket_frame():

    
    # Query format used to find students and instruments
    def query_format(query):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()  
        c.execute(query)
        info = c.fetchall()

        

        conn.commit()
        conn.close()
        return info

    def find_student():
        student_name = student_entry.get()
        student_query = """ SELECT *   
                            FROM Renter
                            WHERE student_name LIKE '"""  + student_name + """%'    
                    """
        
        students = query_format(student_query)
        print(students)
        student_combobox["values"] = students
        
        
        #return students

    def find_instrument():
        instrument = instrument_entry.get()
        insrument_query = """ SELECT instrument, serial_num
                            FROM Instrument
                            Where instrument LIKE '""" + instrument + """%' and status == 'Ready'      
        """
        found_instruments = query_format(insrument_query)
        instrument_combobox["values"] = found_instruments
        

    def create_ticket():
        
        rentID = secrets.token_hex(4)
        # Get the selecected Customer ID      
        customer = student_combobox.get()
        customerID = customer.split()[0]
        # Get the selected Instrument ID
        selected_instrument = instrument_combobox.get()

        if selected_instrument[0] == '{':
            serial_num = selected_instrument.split('} ', 1)[1]

        else:   
            serial_num = selected_instrument.split()[1]

        if serial_num[0] == "{":
            serial_num = serial_num[1:]
            serial_num = serial_num[:-1]

        date_out = date_out_entry.get()
        due_back = due_back_entry.get()
        status = status_combobox.get()
        total_cost = cost_entry.get()
        paid = paid_status_var.get()

        student_entry.delete(0, 20)
        instrument_entry.delete(0, 20)
        instrument_combobox.set('')
        student_combobox.set('')
        date_out_entry.delete(0,20)
        due_back_entry.delete(0, 20)
        cost_entry.delete(0, 20)
        status_combobox.set('')
        paid_check.deselect()

        

        conn = sqlite3.connect('test.db')
        rented_table_create_query = """CREATE TABLE IF NOT EXISTS Rented_Ticket (
                                rentID Varchar(8),
                                customerID Varchar(6),
                                serial_num Varchar(6),
                                date_out date,
                                due_back date,
                                status Varchar(8),
                                total_cost double,
                                paid varchar(8),
                                PRIMARY KEY (rentID),
                                foreign KEY (customerID) references Renter(customerID),
                                foreign KEY (serial_num) references Instrument(serial_num)
                                );
                            """
        conn.execute(rented_table_create_query)
        
        # Insert Data Query
        new_ticket_query = '''Insert INTO Rented_Ticket (rentID, customerID, serial_num, date_out, due_back, status, total_cost,
                                paid) VALUES
                            (?, ?, ?, ?, ?, ?, ?, ?)'''
        
        data_tuple = (rentID, customerID, serial_num, date_out, due_back, status, total_cost, paid)

        # Change instrument to out query
        change_instrument_status = """ UPDATE instrument
                            SET status = "Out"
                            Where serial_num == '""" + serial_num + """'     
                            """

       
        # Conn Cursor  
        cursor = conn.cursor()
        cursor.execute(new_ticket_query, data_tuple)
        cursor.execute(change_instrument_status)
        conn.commit()
        conn.close()
        
    # Student
    students = []
    ticket_frame = tkinter.LabelFrame(frame, text= 'Add Ticket')
    student_label = tkinter.Label(ticket_frame, text= "Student Name")
    student_entry = tkinter.Entry(ticket_frame)
    student_combobox = ttk.Combobox(ticket_frame, values= students)
    find_student_btn = tkinter.Button(ticket_frame, text= "Find Student", command= find_student)
    
    # Instrument
    instruments = []
    instrument_label = tkinter.Label(ticket_frame, text= "Instrument")
    instrument_entry = tkinter.Entry(ticket_frame)
    instrument_combobox = ttk.Combobox(ticket_frame, values= instruments)
    find_instrument_btn = tkinter.Button(ticket_frame, text= "Find Instrument", command= find_instrument)

    # Ticket info
    date_out_label = tkinter.Label(ticket_frame, text= "Date Out (yyyy-mm-dd)")
    date_out_entry = tkinter.Entry(ticket_frame)
    due_back_label = tkinter.Label(ticket_frame, text= "Due Back (yyyy-mm-dd)")
    due_back_entry = tkinter.Entry(ticket_frame)

    # Status
    status_label = tkinter.Label(ticket_frame, text= "Status")
    status_combobox = ttk.Combobox(ticket_frame, values= ["Out", "Retuned", "Late"])

    # Cost
    cost_label = tkinter.Label(ticket_frame, text= "Cost")
    cost_entry = tkinter.Entry(ticket_frame)

    # Paid Status
    paid_status_var = tkinter.StringVar(value="Not Paid")
    paid_check = tkinter.Checkbutton(ticket_frame, text="Paid",
                                       variable=paid_status_var, onvalue="Paid", offvalue="Not Paid")



    # Placement of frames
    ticket_frame.grid(row= 1, column= 0, sticky= "news", padx= 20, pady= 10)
    student_label.grid(row= 0, column=0)
    student_entry.grid(row= 1, column= 0)
    find_student_btn.grid(row= 0, column=1)
    student_combobox.grid(row= 1, column= 1)
    instrument_label.grid(row= 0, column= 2)
    instrument_entry.grid(row= 1, column= 2)
    find_instrument_btn.grid(row= 0, column=3)
    instrument_combobox.grid(row= 1, column=3, columnspan= 4)  
    date_out_label.grid(row=2, column=0)
    date_out_entry.grid(row=3, column=0)
    due_back_label.grid(row=2, column=1)
    due_back_entry.grid(row=3, column=1)
    status_label.grid(row=2, column=2)
    status_combobox.grid(row=3, column=2)
    cost_label.grid(row=2, column=3)
    cost_entry.grid(row=3, column=3)
    paid_check.grid(row= 4, column=0)

    # Create Ticket Button
    create_ticket_btn = tkinter.Button(ticket_frame, text= "Create Ticket", command= create_ticket)
    create_ticket_btn.grid(row= 4, column= 1, columnspan= 3)

    # Configure the padding
    for widget in ticket_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)


#
def update_instruments_frame():
    update_instruments_frame =  tkinter.Frame



window.mainloop()


