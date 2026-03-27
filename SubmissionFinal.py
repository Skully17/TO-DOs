"""
Program Created By:
David Ellis  ID: 3728275  Email: ellisd5@lsbu.ac.uk
Elliott Gipson  ID: 3727604  Email: gipsone@lsbu.ac.uk
"""

from datetime import date #This code draws from the datetime function and imports it into the code
from tkinter import *
from tkinter.ttk import * #This imports the TK inter function
from PIL import Image, ImageTk #This imports both image and imageTk from the PIL library
import calendar #This imports the calender function


class ScreenBase(Frame):  # This is the foundation of all screens
    def __init__(self, master):
        self.months = {name: num for num, name in enumerate(calendar.month_name) if num}
        super().__init__(master)  # This initialises the parent class
        self.grid()
        self.create_widgets()

    def create_widgets(self):  # This function creates a pass widget
        pass


class ToDo(object):  # This designates a class function that sets out different segments of the system
    def __init__(self, description, start_date=date.today(), due_date=None, priority=5, status='Incomplete', reminder=0):
        self.description = description
        self.start = start_date
        self.due = due_date
        self.priority = float(priority)
        self.status = status
        self.reminder = int(reminder)

    def __str__(self):  #This function is called whenever something needs to be printed
        return_value = ""
        for item in self.attributes():
            return_value += '%s: %s  ' % (item, str(self.__getattribute__(item)))  #This adds the current item and it's value to the return string
        return return_value

    def modify(self, description, start, due, priority, status, reminder): #This function is for the modify segment
        self.description = description
        self.start = start
        self.due = due
        self.priority = priority
        self.status = status
        self.reminder = reminder

    def delete(self): #This function is used to remove from the database
        Database.remove(self)
        write_to_file()

    def attributes(self):
        #This iterated over the first 6 items from the list of the object's attributes and methods
        return self.__dir__()[:6]

    def values(self): #This function creates a values list
        values = []
        for item in self.attributes():
            values.append(self.__getattribute__(item))
        return values


class MenuScreen(ScreenBase): #This class if for the menu screen of the system
    def __init__(self, master):
        super().__init__(master)
        try:
            get_file_contents() #This line gets contents from a file
        except FileNotFoundError:
            pass
        self.reminders()

    def create_widgets(self): #This function is used to create widgets inside the application
        image = Image.open('LSBU Logo.png')
        photo = ImageTk.PhotoImage(image)
        logo = Label(self, image=photo)
        logo.image = photo

        add_todo = Button(self, text='Add TO-DO', command=self.add_to_do) #These lines add buttons to the app
        to_dos = Button(self, text='TO-DOs', command=self.to_dos)
        reminder = Button(self, text='Reminders', command=self.reminders)
        exit = Button(self, text='Exit', command=self.master.destroy)

        logo.grid(column=0, row=0) #These lines organise the app into grids/columns
        add_todo.grid(column=0, row=1)
        to_dos.grid(column=0, row=2)
        reminder.grid(column=0, row=3)
        exit.grid(column=0, row=4)

    def add_to_do(self): #This function is used to launch the add function
        AddTODOScreen(self.master)

    def to_dos(self): #This function is used to present the database
        DatabaseScreen(self.master)

    def reminders(self):
        for todo in Database:
            if int(todo.reminder) and (todo.due - date.today()).total_seconds() <= 172800 and todo.status != 'Finished':
                ReminderScreen(self.master, todo)


class DatabaseScreen(ScreenBase): #This class is used for defining the database screen
    def __init__(self, master):
        self.todos = Toplevel(master)
        self.todos.title('TO-DOs To Do')
        super().__init__(master)
        self.master = master

    def create_widgets(self):#This function is used to override the above of a similar name

        class ModifyLater(object): #This modifies the master screen
            def __init__(self, screen, master_screen, todo):
                self.todo = todo
                self.master = master_screen
                self.screen = screen

            def __call__(self):  #This method is called when an instance of its class is called
                self.screen.todos.destroy()
                ModifyScreen(self.master, self.todo)

        class DeleteLater(object): #This modifies the master screen
            def __init__(self, master_screen, todo):
                self.todo = todo
                self.master = master_screen
                self.widgets = []

            #This Method is called when an instance of this class is called
            def __call__(self):
                for widget in self.widgets:
                    widget.grid_remove()
                self.todo.delete()

            def widgets_to_kill(self, widgets): #This function kills the widgets on screen
                for widget in widgets:
                    self.widgets.append(widget)

        title = Label(self.todos, text='TO-DOs To Do:')

        count = 0
        for item in Database: #This goes through all the todos and creates different widgets for them
            count += 1
            label = Label(self.todos, text=item)
            modify = Button(self.todos, text='Modify', command=ModifyLater(self, self.master, item))
            delete_later = DeleteLater(self.todos, item)
            delete = Button(self.todos, text='Delete', command=delete_later)
            delete_later.widgets_to_kill([label, modify, delete])

            label.grid(column=0, row=count)
            modify.grid(column=1, row=count)
            delete.grid(column=2, row=count)

        exit = Button(self.todos, text='Exit', command=self.todos.destroy)

        title.grid(column=0, row=0)
        exit.grid(column=0, row=count+1)


class AddTODOScreen(ScreenBase):  #This creates a class for the Add function screen
    def __init__(self, master):
        self.add_window = Toplevel(master)
        self.add_window.title('Add TO-DO')
        self.description = StringVar()
        self.start_day = IntVar()
        self.start_month = StringVar()
        self.start_year = IntVar()
        self.due_day = IntVar()
        self.due_month = StringVar()
        self.due_year = IntVar()
        self.priority = StringVar()
        self.status = StringVar()
        self.reminder = IntVar()
        super().__init__(master)

    def create_widgets(self): #This creates the necessary widgets for the add function
        today = date.today()

        description_label = Label(self.add_window, text='Description: ') #This creates widgets for the description segment
        description = Entry(self.add_window, textvariable=self.description)

        start_date_label = Label(self.add_window, text='Start Date: ') #This creates labels and widgets for the start date
        start_day = Spinbox(self.add_window, from_=1, to=31, width=2, textvariable=self.start_day)
        start_month = Combobox(self.add_window, values=calendar.month_name[1:], width=9, textvariable=self.start_month)
        start_month.set(calendar.month_name[today.month])
        start_year = Spinbox(self.add_window, from_=today.year, to=today.year+100, width=4, textvariable=self.start_year)

        due_date_label = Label(self.add_window, text='Due Date: ') #This creates labels and widgets for the start date
        due_day = Spinbox(self.add_window, from_=1, to=31, width=2, textvariable=self.due_day)
        due_month = Combobox(self.add_window, values=calendar.month_name[1:], width=9, textvariable=self.due_month)
        due_month.set(calendar.month_name[today.month])
        due_year = Spinbox(self.add_window, from_=today.year, to=today.year+100, width=4, textvariable=self.due_year)

        priority_label = Label(self.add_window, text='Priority: ') #This creates widgets for the priority segment
        priority = Scale(self.add_window, orient=HORIZONTAL, length=100, from_=0, to=10, variable=self.priority)
        priority.set(5)

        status_label = Label(self.add_window, text='Status: ') #This creates the widgets for the status segment
        states = ['Not Started', 'In Progress', 'Finished']
        status = Combobox(self.add_window, values=states, textvariable=self.status)
        status.set(states[0])

        reminder_label = Label(self.add_window, text='Reminder: ') #This creates the widgets for the reminder segment
        reminder = Checkbutton(self.add_window, onvalue=1, offvalue=0, variable=self.reminder)

        add = Button(self.add_window, text='Add', command=self.add_to_do) #These two lines are for the add and cancer buttons
        cancel = Button(self.add_window, text='Cancel', command=self.add_window.destroy)

        description_label.grid(column=0, row=0) #This section is for the different grid placements
        description.grid(column=1, row=0)
        start_date_label.grid(column=0, row=1)
        start_day.grid(column=1, row=1)
        start_month.grid(column=2, row=1)
        start_year.grid(column=3, row=1)
        due_date_label.grid(column=0, row=2)
        due_day.grid(column=1, row=2)
        due_month.grid(column=2, row=2)
        due_year.grid(column=3, row=2)
        
        priority_label.grid(column=0, row=3) #This section is for the different grid placements
        priority.grid(column=1, row=3)
        status_label.grid(column=0, row=4)
        status.grid(column=1, row=4)
        reminder_label.grid(column=0, row=5)
        reminder.grid(column=1, row=5)
        add.grid(column=3, row=6)
        cancel.grid(column=0, row=6) 

    def add_to_do(self): #This fucntion is for adding a to do
        desc = self.description.get()
        start = date(self.start_year.get(), self.months[self.start_month.get()], self.start_day.get())
        due = date(self.due_year.get(), self.months[self.due_month.get()], self.due_day.get())
        priority = self.priority.get()
        status = self.status.get()
        reminder = self.reminder.get()
        Database.append(ToDo(desc, start, due, priority, status, reminder))
        write_to_file()
        self.add_window.destroy()


class ModifyScreen(ScreenBase): #This class is for any work done to modify the screen
    def __init__(self, master, todo):
        self.modify_window = Toplevel(master)
        self.modify_window.title('Modify TO-DO')
        self.todo = todo

        self.description = StringVar() #This segment changes these items to string objects
        self.start_day = IntVar()
        self.start_month = StringVar()
        self.start_year = IntVar()
        self.due_day = IntVar()
        self.due_month = StringVar()
        self.due_year = IntVar()
        self.priority = StringVar()
        self.status = StringVar()
        self.reminder = IntVar()
        super().__init__(master)
        self.description.set(self.todo.description)  #Sets the variables that contain data already
        self.start_day.set(self.todo.start.day)
        self.start_month.set(self.find_month_by_num(self.todo.start.month))
        self.start_year.set(self.todo.start.year)
        self.due_day.set(self.todo.due.day)
        self.due_month.set(self.find_month_by_num(self.todo.due.month))
        self.due_year.set(self.todo.due.year)
        self.priority.set(self.todo.priority)
        self.status.set(self.todo.status)
        self.reminder.set(self.todo.reminder)

        self.master = master

    def create_widgets(self):#This function is for creating widgets for this page
        today = date.today() #This shows todays date

        description_label = Label(self.modify_window, text='Description: ')  #This segment is for the description section
        description = Entry(self.modify_window, textvariable=self.description)

        start_date_label = Label(self.modify_window, text='Start Date: ')
        start_day = Spinbox(self.modify_window, from_=1, to=31, width=2, textvariable=self.start_day) #This segment is for the start section
        start_month = Combobox(self.modify_window, values=calendar.month_name[1:], width=9, textvariable=self.start_month)
        start_year = Spinbox(self.modify_window, from_=today.year, to=today.year+100, width=4, textvariable=self.start_year)

        due_date_label = Label(self.modify_window, text='Due Date: ')
        due_day = Spinbox(self.modify_window, from_=1, to=31, width=2, textvariable=self.due_day) #This segment is for the due dates section
        due_month = Combobox(self.modify_window, values=calendar.month_name[1:], width=9, textvariable=self.due_month)
        due_year = Spinbox(self.modify_window, from_=today.year, to=today.year+100, width=4, textvariable=self.due_year)

        priority_label = Label(self.modify_window, text='Priority: ') #this code is for the priority segment
        priority = Scale(self.modify_window, orient=HORIZONTAL, length=100, from_=0, to=10, variable=self.priority)

        status_label = Label(self.modify_window, text='Status: ') #This section is for the status segment
        states = ['Not Started', 'In Progress', 'Finished']
        status = Combobox(self.modify_window, values=states, textvariable=self.status)

        reminder_label = Label(self.modify_window, text='Reminder: ') #This is for the reminder section
        reminder = Checkbutton(self.modify_window, onvalue=1, offvalue=0, variable=self.reminder)

        modify = Button(self.modify_window, text='Modify', command=self.modify_to_do) #this creates the modify and cancel buttons
        cancel = Button(self.modify_window, text='Cancel', command=self.destroy)

        description_label.grid(column=0, row=0) #This section places each widget in their respective grid
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
        modify.grid(column=3, row=6)
        cancel.grid(column=0, row=6)

    def modify_to_do(self): #This if a function for modifying the to do list
        desc = self.description.get()
        self.todo.start.replace(int(self.start_year.get()), self.months[self.start_month.get()], int(self.start_day.get()))
        self.todo.due.replace(int(self.due_year.get()), self.months[self.due_month.get()], int(self.due_day.get()))
        priority = self.priority.get()
        status = self.status.get()
        reminder = self.reminder.get()
        self.todo.modify(desc, self.todo.start, self.todo.due, priority, status, reminder)
        write_to_file()
        self.destroy()

    def find_month_by_num(self, month_number): #This is a function for finding a month by the number
        return list(self.months.keys())[list(self.months.values()).index(month_number)]

    def destroy(self): #This function destroys the screen/window
        self.modify_window.destroy()
        DatabaseScreen(self.master)


class ReminderScreen(ScreenBase): #this class creates a screen for reminders
    def __init__(self, master, todo):
        self.reminder_window = Toplevel(master)
        self.reminder_window.title('ATTENTION!')
        self.reminder_window.attributes("-topmost", True)  # keeps window ontop of others
        self.todo = todo
        super().__init__(master)

    def create_widgets(self):  #This function is for creating widgets for this page
        text = '%s is nearly due:' % self.todo.description
        reminder = Label(self.reminder_window, text=text, font=('Helvetica', 20, 'bold'))
        due_text = 'Due Date: %s' % self.todo.due
        due = Label(self.reminder_window, text=due_text, font=('Helvetica', 20))

        close = Button(self.reminder_window, text='Close', command=self.reminder_window.destroy) #This is used to create budget widgets
        disable = Button(self.reminder_window, text='Disable Reminder', command=self.disable_reminder)
        complete = Button(self.reminder_window, text='Complete', command=self.complete_todo)

        reminder.grid(column=1, row=0) #This section places each widget in their respective grid
        due.grid(column=1, row=1)
        close.grid(column=0, row=2)
        disable.grid(column=1, row=2)
        complete.grid(column=2, row=2)

    def disable_reminder(self): #This disables an active reminder
        self.todo.reminder = 0
        write_to_file()
        self.reminder_window.destroy()

    def complete_todo(self): #This completes an active reminder
        self.todo.status = 'Finished'
        self.todo.reminder = 0
        write_to_file()
        self.reminder_window.destroy()


def write_to_file():
    #This gets all data from database list, puts it all in a string and writes that string to the database file
    to_write = ""
    for todo in Database:
        for item in todo.attributes():  #This iterates through the important attributes of todo
            to_write += "%s," % todo.__getattribute__(item)  #This appends the value of the current object attribute to the write string
        to_write += "\n"  #This adds new line at end of every todo
    # writes
    with open('database.csv', 'w') as fp:
        fp.write(to_write)


def get_file_contents():
    #This reads all data in database file and sores is in a list
    with open('database.csv', 'r') as fp:
        for todo in fp:  # todos are separated by a new line
            args = todo.split(',')  # attributes are separated by ','s
            Database.append(ToDo(*args[:6]))  #This uses stored data, excluding '\n' to recreate todo objects
    objectify_todo_dates()


def objectify_todo_dates(): #This segment searches and splits a text depending on the variety of Todos inside
    try:
        for todo in Database:
            start_str = todo.start.split('-')
            todo.start = date(*[int(x) for x in start_str])
            due_str = todo.due.split('-')
            todo.due = date(*[int(x) for x in due_str])
    except Exception as ex:
        print(ex.args[0])


if __name__ == '__main__':
    Database = []  # This is a list that holds all the to-dos which was made at the start

    root = Tk()  # This is theot object for the TKinter
    root.title('TO-DOs')  # This makes the app title say To-Dos

    menu = MenuScreen(root)  # This opens up the Tkinter frame using the root object to launch the main menu
    root.mainloop()  # Checks the application for any events
