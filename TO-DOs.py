#Program Created By David Ellis   ID: 3728275    Email: ellisd5@lsbu.ac.uk - Elliott Gipson ID: ... Email: gipsone@lsbu.ac.uk

from datetime import date
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import calendar


class __Database(list):
    def __str__(self):
        for item in self:
            print(item)


class ScreenBase(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        pass


class ToDo(object):
    def __init__(self, Description, Start_Date=date.today(), Due_Date=None, Priority=5, Status='Incomplete', Reminder=False):
        self.description = Description
        self.start = Start_Date
        self.due = Due_Date
        self.priority = Priority
        self.status = Status
        self.reminder = Reminder

    def __str__(self):  # this is a special method that is called whenever the object is printed
        return_value = ""
        for item in self.__dir__()[:6]:  # this iterated over the first 5 items from the list of the object's attributes and methods
            return_value += '%s: %s  ' % (item, str(self.__getattribute__(item)))  # this adds the current item and it's value to the return string
        return return_value

    def modify(self, master):
        mod = master.Toplevel()

    def delete(self):
        Database.remove(self)
        write_to_file()


class MenuScreen(ScreenBase):
    def __init__(self, master):
        super().__init__(master)
        get_file_contents()

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
        self.todos = Toplevel(master)
        self.todos.title('TO-DOs To Do')
        super().__init__(master)

    def create_widgets(self):
        title = Label(self.todos, text='TO-DOs To Do:')

        count = 0
        for item in Database:
            count += 1
            lable = Label(self.todos, text=item)
            modify = Button(self.todos, text='Modify', command=item.modify)
            delete = Button(self.todos, text='Delete', command=item.delete)

            lable.grid(column=0, row=count)
            modify.grid(column=1, row=count)
            delete.grid(column=2, row=count)

        exit = Button(self.todos, text='Exit', command=self.todos.destroy)

        title.grid(column=0, row=0)
        exit.grid(column=0, row=count+1)


class AddTODOScreen(ScreenBase):
    def __init__(self, master):
        self.add_window = Toplevel(master)
        self.add_window.title('Add TO-DO')
        self.description = StringVar()
        self.start_date = StringVar()
        self.end_date = StringVar()
        self.priority = StringVar()
        self.status = StringVar()
        self.reminder = IntVar()
        super().__init__(master)

    def create_widgets(self):
        today = date.today()

        description_label = Label(self.add_window, text='Description: ')
        description = Entry(self.add_window, textvariable=self.description)

        start_date_label = Label(self.add_window, text='Start Date: ')
        start_day = Spinbox(self.add_window, from_=1, to=30, width=2)  # TODO: get how many days are in given month, make it 'to' value
        start_month = Combobox(self.add_window, values=calendar.month_name[1:], width=9)
        start_month.set(calendar.month_name[today.month])
        start_year = Spinbox(self.add_window, from_=today.year, to=today.year+100, width=4)

        due_date_label = Label(self.add_window, text='Due Date: ')
        due_day = Spinbox(self.add_window, from_=1, to=30, width=2)  # TODO: get how many days are in given month, make it 'to' value
        due_month = Combobox(self.add_window, values=calendar.month_name[1:], width=9)
        due_month.set(calendar.month_name[today.month])
        due_year = Spinbox(self.add_window, from_=today.year, to=today.year+100, width=4)

        priority_label = Label(self.add_window, text='Priority: ')
        priority = Scale(self.add_window, orient=HORIZONTAL, length=100, from_=0, to=10, variable=self.priority)
        priority.set(5)

        status_label = Label(self.add_window, text='Status: ')
        states = ['Not Started', 'In Progress', 'Finished']
        status = Combobox(self.add_window, values=states, textvariable=self.status)
        status.set(states[0])

        reminder_label = Label(self.add_window, text='Reminder: ')
        reminder = Checkbutton(self.add_window, onvalue=1, offvalue=0, variable=self.reminder)

        add = Button(self.add_window, text='Add', command=self.add_to_do)
        cancel = Button(self.add_window, text='Cancel', command=self.add_window.destroy)

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
        Database.append(ToDo(desc, start, due, priority, status, reminder))
        write_to_file()
        self.add_window.destroy()


class Menu(object):

    def __init__(self):
        # tries to get database data from file. makes new one if file doesn't exist
        try:
            self.get_file_contents()
        except:
            self.write_to_file()

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

def write_to_file():
    # gets all data from database list, puts it all in a string and writes that string to the database file
    to_write = ""
    for todo in Database:
        for item in todo.__dir__()[:6]:  # iterates through the important attributes of employee
            to_write += "%s," % todo.__getattribute__(item)  # appends the value of the current object attribute to the write string
        to_write += "\n"  # adds new line at end of every employee
    # writes
    with open('database.csv', 'w') as fp:
        fp.write(to_write)

def get_file_contents():
    # reads all data in database file and sores is in a list
    with open('database.csv', 'r') as fp:
        for employee in fp:  # employees are seporated by a new line
            args = employee.split(',')  # attributes are seporated by ','s
            Database.append(ToDo(*args[:6]))  # uses stored data, excluding '\n' to recreate employee objects


# Menu()

Database = __Database()

root = Tk()
root.title('TO-DOs')
#root.geometry('300x200+600+200')

menu = MenuScreen(root)

current_screen = MenuScreen
root.mainloop()
