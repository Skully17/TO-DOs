#Program Created By David Ellis   ID: 3728275    Email: ellisd5@lsbu.ac.uk - Elliott Gipson ID: ... Email: gipsone@lsbu.ac.uk

from datetime import date
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import calendar

Database = []  # this will be where all of the employees are stored within the program


class Database(list):
    def __init__(self):
        self.database = []

    def __str__(self):
        for item in self.database:
            print(item)

    def append(self, item):
        self.database.append(item)

    def remove(self, item):
        self.database.remove(item)


class ToDo(object):
    def __init__(self, Description, Start_Date=date.today(), Due_Date=None, Priority=0, Status='Incomplete', Reminder=False):
        self.description = Description
        self.start = Start_Date
        self.due = Due_Date
        self.priority = Priority
        self.status = Status
        self.reminder = Reminder

    def __str__(self):  # this is a special method that is called whenever the object is printed
        return_value = ""
        for item in self.__dir__()[:5]:  # this iterated over the first 5 items from the list of the object's attributes and methods
            return_value += '%s: %s  ' % (item, str(self.__getattribute__(item)))  # this adds the current item and it's value to the return string
        return return_value


class ScreenBase(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        pass


class MenuScreen(ScreenBase):
    def __init__(self, master):
        super().__init__(master)

    def create_widgets(self):
        image = Image.open('LSBU Logo.png')
        photo = ImageTk.PhotoImage(image)
        logo = Label(self, image=photo)
        logo.image = photo

        self.add_employee = Button(self, text='Add TO-DO', command=self.add_to_do)
        self.to_dos = Button(self, text='TO-DOs', command=self.to_dos)
        self.exit = Button(self, text='Exit', command=self.master.destroy)

        logo.grid(column=0, row=0)
        self.add_employee.grid(column=0, row=1)
        self.to_dos.grid(column=0, row=2)
        self.exit.grid(column=0, row=3)

    def to_dos(self):
        DatabaseScreen(self.master)

    def add_to_do(self):
        AddTODOScreen(self.master)


class DatabaseScreen(ScreenBase):
    def __init__(self, master):
        self.ae = Toplevel(master)
        self.ae.title('TO-DOs To Do')
        super().__init__(master)

    def create_widgets(self):
        pass  # TODO: make database screen whitch shows all of the TO-DOs


class AddTODOScreen(ScreenBase):
    def __init__(self, master):
        self.ae = Toplevel(master)
        self.ae.title('Add TO-DO')
        self.description = StringVar()
        self.start_date = StringVar()
        self.end_date = StringVar()
        self.priority = StringVar()
        self.status = StringVar()
        self.reminder = IntVar()
        super().__init__(master)

    def create_widgets(self):
        today = date.today()

        description_label = Label(self.ae, text='Description: ')
        description = Entry(self.ae, textvariable=self.description)

        start_date_label = Label(self.ae, text='Start Date: ')
        start_day = Spinbox(self.ae, from_=1, to=30, width=2)  # TODO: get how many days are in given month, make it 'to' value
        start_month = Combobox(self.ae, values=calendar.month_name[1:], width=9)
        start_month.set(calendar.month_name[today.month])
        start_year = Spinbox(self.ae, from_=today.year, to=today.year+100, width=4)

        due_date_label = Label(self.ae, text='Due Date: ')
        due_day = Spinbox(self.ae, from_=1, to=30, width=2)  # TODO: get how many days are in given month, make it 'to' value
        due_month = Combobox(self.ae, values=calendar.month_name[1:], width=9)
        due_year = Spinbox(self.ae, from_=today.year, to=today.year+100, width=4)

        priority_label = Label(self.ae, text='Priority: ')
        priority = Scale(self.ae, orient=HORIZONTAL, length=100, from_=0, to=10, variable=self.priority)
        priority.set(5)

        status_label = Label(self.ae, text='Status: ')
        states = ['Not Started', 'In Progress', 'Finished']
        status = Combobox(self.ae, values=states, textvariable=self.status)
        status.set(states[0])

        reminder_label = Label(self.ae, text='Reminder: ')
        reminder = Checkbutton(self.ae, onvalue=1, offvalue=0, variable=self.reminder)

        add = Button(self.ae, text='Add', command=self.add_to_do)
        cancel = Button(self.ae, text='Cancel', command=self.ae.destroy)

        description_label.grid(column=0, row=0)
        description.grid(column=1, row=0)
        start_date_label.grid(column=0, row=1)
        start_day.grid(column=1, row=1)
        start_month.grid(column=2, row=1)
        start_year.grid(column=3, row=1)
        due_date_label.grid(column=0, row=2)
        due_day.grid(column=1, row=2)
        due_month.grid(column=2, row=2)
        due_year.grid(column=3, row=2)
        
        priority_label.grid(column=0, row=3)
        priority.grid(column=1, row=3)
        status_label.grid(column=0, row=4)
        status.grid(column=1, row=4)
        reminder_label.grid(column=0, row=5)
        reminder.grid(column=1, row=5)
        add.grid(column=3, row=6)
        cancel.grid(column=0, row=6) 

    def add_to_do(self):
        desc = self.description.get()
        start = self.start_date.get()
        due = self.end_date.get()
        priority = self.priority.get()
        status = self.status.get()
        reminder = self.reminder.get()
        print(desc, start, due, priority, status, reminder)


class Menu(object):

    def __init__(self):
        # tries to get database data from file. makes new one if file doesn't exist
        try:
            self.get_file_contents()
        except:
            self.write_to_file()
        # keeps asking user for input until valid one is given
        while True:
            print('\n{:-^40}'.format('Main Menu')) # format used to print spaces wide, using '-'s to fill in the blanks, with 'Main Menue' located in the center
            print("""
1) Add Employee
2) Remove Employee
3) Modify Employee
4) Search Database
5) Display Database
0) Exit
""")
            choice = input('Enter Action To Make: ')
            if choice == '0':
                break
            elif choice == '1':
                self.add()  # starts process of adding an employee to the database
                self.write_to_file()
            elif choice == '2':
                self.delete()  # starts process of removing an employee from the database
                self.write_to_file()
            elif choice == '3':
                self.modify()  # starts process of modifying an employee from the database
                self.write_to_file()
            elif choice == '4':
                self.employee_search()  # starts process of searching employees in the database
            elif choice == '5':
                self.display_list_of_employees(Database)  # prints all employees in the database

    def add(self):
        print('\n{:-^40}'.format('Add Employee'))  # prints 40 charactors, '-' replacing spaces, with 'Add Employee' in the center
        print("Enter '0' To Exit\n")
        while True:
            _id = self.persist_while_empty('Enter ID Of Employee: ')  # asks for id until user enters something
            if self.grab_employee(_id):  # this tries to get the employee using the given id. if it succeeds, the id exists, if not, the id is valid
                print('ID already exists: %s' % _id)
                continue  # sends back to start of loop to get new input from user
            break  # ends loop as valid id has been given
        if _id == '0':
            return
        name = self.persist_while_empty('Enter Name Of Employee: ')  # asks for name until user enters data
        if name == '0':
            return
        dep = self.persist_while_empty('Enter Department The Employee Is In: ')  # asks for department until user enters data
        if dep == '0':
            return
        des = self.persist_while_empty('Enter The Designation Of The Employee: ')  # asks designation until user enters data
        if des == '0':
            return
        jd = self.persist_while_empty('Enter The Date The Employee Joined: ')  # asks when the employee joined until the user enters data
        if jd == '0':
            return
        while True:
            # asks if employee is active until the user enters ether a 'y' or 'n'
            es = self.persist_while_empty('Activate Employee? (y/n) ')
            if es.lower() == 'y':
                es = 'Active'
                break
            elif es.lower() == 'n':
                es = 'Inactive'
                break
            elif es == '0':
                break
        if es == '0':
            return

        Database.append(Employee(_id, name, dep, des, jd, es))  # creates a nwe employe with data given and adds them to the list of employees


    def delete(self):
        print('\n{:-^40}'.format('Remove Employee'))  # prints 40 charactors, '-' replacing spaces, with 'Remove Employee' in the center
        print("Enter '0' To Exit\n")
        while True:
            to_remove = self.persist_while_empty('Enter ID of the Employee you want to remove: ')  # keeps asking for an id untill user enters one
            if to_remove == '0':
                return
            employee_being_removed = self.grab_employee(to_remove)  # tries to get employee with matching id
            # if there is not a match, send to top of loop
            if not employee_being_removed:
                print('ID not found in database: {0}'.format(to_remove))
                continue
            # if the employee is currently active, send to top of loop
            if employee_being_removed.employee_status.lower() == 'active':
                print('Employee Has To Be Inactive Before Being Removed')
                continue
            # the employee is removed from the list of employees and is returned
            return Database.pop(Database.index(employee_being_removed))

    def modify(self):
        print('\n{:-^40}'.format('Modify Employee'))  # prints 40 charactors, '-' replacing spaces, with 'Modify Employee' in the center
        print("Enter '0' To Exit")
        self.display_list_of_employees(Database)
        while True:
            _id = self.persist_while_empty('Enter ID Of Employee You Want To Modify: ')  # keeps asking for employee id until user enters data
            if _id == '0':
                return
            # if there are no employees with a matching id, send to top of loop
            if not self.grab_employee(_id):
                print('ID not found in database: {0}'.format(_id))
                continue
            break
        print("""
1) Name
2) Department
3) Designation
4) Employee's Status
0) Exit
""")
        while True:
            # gets what attribute the user wants to change for the chosen employee
            attribute = input('what attribute do you want to change for this employee? ')
            if attribute == '0':
                return
            # gets employee using given id and changes it's name attribute to whatever data the user inputs
            if attribute == '1':
                self.grab_employee(_id).name = self.persist_while_empty('Enter Replacement Name: ')
                print('Employee Name Has Been Changed...')
            # gets employee using given id and changes it's department attribute to whatever data the user inputs
            if attribute == '2':
                self.grab_employee(_id).department = self.persist_while_empty('Enter Replacement Department: ')
                print('Employee Department Has Been Changed...')
            # gets employee using given id and changes it's designation attribute to whatever data the user inputs
            if attribute == '3':
                self.grab_employee(_id).designation = self.persist_while_empty('Enter Replacement Designation: ')
                print('Employee Designation Has Been Changed...')
            # gets employee using given id and asks user if they want to make the employee Active/Inactive depending on the state of employee
            if attribute == '4':
                if self.grab_employee(_id).employee_status == 'Active':  # if the employee with given id is active...
                    confirm = input('Employee Is Active. Would You Like To Make Them Inactive? (y/n) ')  # asks user if they want to Deactivate employee
                    # if the user enter 'y', the employee status is changed to 'Inactive'
                    if confirm.lower() == 'y':
                        self.grab_employee(_id).employee_status = 'Inactive'
                        print('Employee Has Been Activated...')
                else:
                    confirm = input('Employee is Inactive. Would You Like To Activate Them? (y/n) ')  # asks user if they want to Activate employee
                    # if the user enters 'y', the employee status is changed to 'Active'
                    if confirm.lower() == 'y':
                        self.grab_employee(_id).employee_status = 'Active'
                        print('Employee Has Been Deactivated...')

    def employee_search(self):
        print('\n{:-^40}'.format('Search Employees'))  # prints 40 charactors, '-' replacing spaces, with 'Search Employees' in the center
        print("Enter '0' To Exit")
        while True:
            employees = []  # empty list to store employees found in search
            print("""
1) ID
2) name
3) Department
4) Designation
5) Joining Date
6) Employee Status
""")
            to_search = self.persist_while_empty('Enter field you want to search with: ')  # keeps asking for search field until user enters data
            if to_search == '0':
                return
            if to_search == '1':
                while True:
                    _id = self.persist_while_empty('Enter ID Of Employee: ')  # keeps asking for id until user enters data
                    if _id == '0':
                        break
                    # tries to get employee using given id. if there is no match, send to top of loop. if there is, stop the loop
                    employee = self.grab_employee(_id)
                    if not employee:
                        continue
                    break
                # if user breaks out of previouse loop using '0', 'employee' won't exist. this ignores the UnboundLocalError that would be raised
                try:
                    print(employee)
                except:
                    pass
            if to_search == '2':
                while True:
                    name = self.persist_while_empty('Enter Name To Search: ')  # keeps asking for name until user enters data
                    if name == '0':
                        break
                    # for every employee, if that employee's name attribute matches the search criteria given, append that employee to the search list
                    for employee in Database:
                        if name.lower() == employee.name.lower():
                            employees.append(employee)
                    # if there are items in the search list print them, if not, tell the user there were no employees found
                    if employees:
                        self.display_list_of_employees(employees)
                        break
                    print('There are no Employees in the Database with that name...')
            if to_search == '3':
                while True:
                    department = self.persist_while_empty('Enter Department To Search: ')  # keeps asking user for department until they enter data
                    if department == '0':
                        break
                    # for every employee, if that employee's darpartment attribute matches the search criteria given, append that employee to the search list
                    for employee in Database:
                        if department.lower() == employee.department.lower():
                            employees.append(employee)
                    # if there are items in the search list print them, if not, tell the user there were no employees found
                    if employees:
                        self.display_list_of_employees(employees)
                        break
                    print('There are no Employees that work under that department...')
            if to_search == '4':
                while True:
                    designation = self.persist_while_empty('Enter Designation To Search: ')  # keeps asking for designation until user enters data
                    if designation == '0':
                        break
                    # for every employee, if that employee's designation attribute matches the search criteria given, append that employee to the search list
                    for employee in Database:
                        if designation.lower() == employee.designation.lower():
                            employees.append(employee)
                    # if there are items in the search list print them, if not, tell the user there were no employees found
                    if employees:
                        self.display_list_of_employees(employees)
                        break
                    print('There are no Employees with that designation...')
            if to_search == '5':
                while True:
                    jd = self.persist_while_empty('Enter Joining Date To Search: ')  # keeps asking for joining date until user enters data
                    if jd == '0':
                        break
                    # for every employee, if that employee's joining_date attribute matches the search criteria given, append that employee to the search list
                    for employee in Database:
                        if jd.lower() == employee.joining_date.lower():
                            employees.append(employee)
                    # if there are items in the search list print them, if not, tell the user there were no employees found
                    if employees:
                        self.display_list_of_employees(employees)
                        break
                    print('There are no Employees with that Joining Date...')
            if to_search == '6':
                while True:
                    es = self.persist_while_empty('Enter Employee Status To Search: ')  # keeps asking for employee status until user enters data
                    if es == '0':
                        break
                    # for every employee, if that employee's employee_status attribute matches the search criteria given, append that employee to the search list
                    for employee in Database:
                        if es.lower() == employee.employee_status.lower():
                            employees.append(employee)
                    # if there are items in the search list print them, if not, tell the user there were no employees found
                    if employees:
                        self.display_list_of_employees(employees)
                        break
                    print('There are no Employees with this status...')

    def write_to_file(self):
        # gets all data from database list, puts it all in a string and writes that string to the database file
        to_write = ""
        for employee in Database:
            for item in employee.__dir__()[:6]:  # iterates through the important attributes of employee
                to_write += "%s," % employee.__getattribute__(item)  # appends the value of the current object attribute to the write string
            to_write += "\n"  # adds new line at end of every employee
        # writes
        with open('database.csv', 'w') as fp:
            fp.write(to_write)

    def get_file_contents(self):
        # reads all data in database file and sores is in a list
        with open('database.csv', 'r') as fp:
            for employee in fp:  # employees are seporated by a new line
                args = employee.split(',')  # attributes are seporated by ','s
                Database.append(Employee(*args[:6]))  # uses stored data, excluding '\n' to recreate employee objects

    def persist_while_empty(self, sentence):
        # keeps on asking given question until they enter something
        while True:
            data = input(sentence)
            if not data:
                print('please enter data...')
                continue
            return data

    def grab_employee(self, ID):
        # iterates through database returning object with matching id
        for employee in Database:
            if employee.id == ID:
                return employee
        return False

    def display_list_of_employees(self, _list):
        # iterates through employees in database and prints them
        print('')
        for item in _list:
            print(item)
        print('')


# Menu()

root = Tk()
root.title('TO-DOs')
#root.geometry('300x200+600+200')

menu = MenuScreen(root)

current_screen = MenuScreen
root.mainloop()
