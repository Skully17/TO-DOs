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
        self.months = {name: num for num, name in enumerate(calendar.month_name) if num}
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
        for item in self.attributes():
            return_value += '%s: %s  ' % (item, str(self.__getattribute__(item)))  # this adds the current item and it's value to the return string
        return return_value

    def modify(self, description, start, due, priority, status, reminder):
        self.description = description
        self.start = start
        self.due = due
        self.priority = priority
        self.status = status
        self.reminder = reminder

    def delete(self):
        Database.remove(self)
        write_to_file()
        root.update_idletasks()
        root.update()
        root.pack_slaves()

    def attributes(self):
        # this iterated over the first 6 items from the list of the object's attributes and methods
        return self.__dir__()[:6]

    def values(self):
        values = []
        for item in self.attributes():
            values.append(self.__getattribute__(item))
        return values


class MenuScreen(ScreenBase):
    def __init__(self, master):
        super().__init__(master)
        try:
            get_file_contents()
        except:
            pass

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

        class ModifyLater(DatabaseScreen):
            def __init__(self, master_screen, todo):
                self.todo = todo
                self.master = master_screen

            def __call__(self):
                ModifyScreen(self.master, self.todo)

        class DeleteLater(DatabaseScreen):
            def __init__(self, master_screen, todo):
                self.todo = todo
                self.master = master_screen

            def __call__(self):
                self.todo.delete()
                self.create_widgets()

        title = Label(self.todos, text='TO-DOs To Do:')

        count = 0
        for item in Database:
            count += 1
            label = Label(self.todos, text=item)
            modify = Button(self.todos, text='Modify', command=ModifyLater(self.todos, item))
            delete = Button(self.todos, text='Delete', command=DeleteLater(self.todos, item))

            label.grid(column=0, row=count)
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

    def create_widgets(self):
        today = date.today()

        description_label = Label(self.add_window, text='Description: ')
        description = Entry(self.add_window, textvariable=self.description)

        start_date_label = Label(self.add_window, text='Start Date: ')
        start_day = Spinbox(self.add_window, from_=1, to=30, width=2, textvariable=self.start_day)  # TODO: get how many days are in given month, make it 'to' value
        start_month = Combobox(self.add_window, values=calendar.month_name[1:], width=9, textvariable=self.start_month)
        start_month.set(calendar.month_name[today.month])
        start_year = Spinbox(self.add_window, from_=today.year, to=today.year+100, width=4, textvariable=self.start_year)

        due_date_label = Label(self.add_window, text='Due Date: ')
        due_day = Spinbox(self.add_window, from_=1, to=30, width=2, textvariable=self.due_day)  # TODO: get how many days are in given month, make it 'to' value
        due_month = Combobox(self.add_window, values=calendar.month_name[1:], width=9, textvariable=self.due_month)
        due_month.set(calendar.month_name[today.month])
        due_year = Spinbox(self.add_window, from_=today.year, to=today.year+100, width=4, textvariable=self.due_year)

        priority_label = Label(self.add_window, text='Priority: ')
        priority = Scale(self.add_window, orient=HORIZONTAL, length=100, from_=0, to=10, variable=self.priority)
        # TODO: round number to whole
        # TODO: display current number
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
        start = date(self.start_year.get(), self.months[self.start_month.get()], self.start_day.get())
        due = date(self.due_year.get(), self.months[self.due_month.get()], self.due_day.get())
        priority = self.priority.get()
        status = self.status.get()
        reminder = self.reminder.get()
        Database.append(ToDo(desc, start, due, priority, status, reminder))
        write_to_file()
        self.add_window.destroy()


class ModifyScreen(ScreenBase):
    def __init__(self, master, todo):
        self.modify_window = Toplevel(master)
        self.modify_window.title('Modify TO-DO')
        self.todo = todo

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
        self.description.set(self.todo.description)
        self.start_day.set(self.todo.start.day)
        self.start_month.set(self.find_month_by_num(self.todo.start.month))
        self.start_year.set(self.todo.start.year)
        self.due_day.set(self.todo.due.day)
        self.due_month.set(self.find_month_by_num(self.todo.due.month))
        self.due_year.set(self.todo.due.year)
        self.priority.set(self.todo.priority)
        self.status.set(self.todo.status)
        self.reminder.set(self.todo.reminder)

    def create_widgets(self):
        today = date.today()

        description_label = Label(self.modify_window, text='Description: ')
        description = Entry(self.modify_window, textvariable=self.description)
        # self.set_text(description, self.description)

        start_date_label = Label(self.modify_window, text='Start Date: ')
        start_day = Spinbox(self.modify_window, from_=1, to=30, width=2, textvariable=self.start_day)  # TODO: get how many days are in given month, make it 'to' value
        # self.set_text(start_day, self.start_day)
        start_month = Combobox(self.modify_window, values=calendar.month_name[1:], width=9, textvariable=self.start_month)
        # start_month.set(self.find_month_by_num(int(self.start_month.get())))
        start_year = Spinbox(self.modify_window, from_=today.year, to=today.year+100, width=4, textvariable=self.start_year)
        # self.set_text(start_year, self.start_year)

        due_date_label = Label(self.modify_window, text='Due Date: ')
        due_day = Spinbox(self.modify_window, from_=1, to=30, width=2, textvariable=self.due_day)  # TODO: get how many days are in given month, make it 'to' value
        # self.set_text(due_day, self.due_day)
        due_month = Combobox(self.modify_window, values=calendar.month_name[1:], width=9, textvariable=self.due_month)
        # due_month.set(self.find_month_by_num(int(self.due_month.get())))
        due_year = Spinbox(self.modify_window, from_=today.year, to=today.year+100, width=4, textvariable=self.due_year)
        # self.set_text(due_year, self.due_year)

        priority_label = Label(self.modify_window, text='Priority: ')
        priority = Scale(self.modify_window, orient=HORIZONTAL, length=100, from_=0, to=10, variable=self.priority)
        # TODO: round number to whole
        # TODO: display current number
        # priority.set(self.priority.get())

        status_label = Label(self.modify_window, text='Status: ')
        states = ['Not Started', 'In Progress', 'Finished']
        status = Combobox(self.modify_window, values=states, textvariable=self.status)
        # status.set(self.status.set())

        reminder_label = Label(self.modify_window, text='Reminder: ')
        reminder = Checkbutton(self.modify_window, onvalue=1, offvalue=0, variable=self.reminder)

        modify = Button(self.modify_window, text='Modify', command=self.modify_to_do)
        cancel = Button(self.modify_window, text='Cancel', command=self.modify_window.destroy)

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
        modify.grid(column=3, row=6)
        cancel.grid(column=0, row=6)

    def modify_to_do(self):
        desc = self.description.get()
        self.todo.start.replace(int(self.start_year.get()), self.months[self.start_month.get()], int(self.start_day.get()))
        self.todo.due.replace(int(self.due_year.get()), self.months[self.due_month.get()], int(self.due_day.get()))
        priority = self.priority.get()
        status = self.status.get()
        reminder = self.reminder.get()
        self.todo.modify(desc, self.todo.start, self.todo.due, priority, status, reminder)
        write_to_file()
        self.modify_window.destroy()

    def set_text(self, widget, text):
        widget.delete(0, END)
        widget.insert(0, text)

    def find_month_by_num(self, month_number):
        return list(self.months.keys())[list(self.months.values()).index(month_number)]


def write_to_file():
    # gets all data from database list, puts it all in a string and writes that string to the database file
    to_write = ""
    for todo in Database:
        for item in todo.attributes():  # iterates through the important attributes of employee
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
    objectify_todo_dates()


def objectify_todo_dates():
    try:
        for todo in Database:
            start_str = todo.start.split('-')
            todo.start = date(*[int(x) for x in start_str])
            due_str = todo.due.split('-')
            todo.due = date(*[int(x) for x in due_str])
    except Exception as ex:
        print(ex.args[0])


# Menu()

Database = __Database()

root = Tk()
root.title('TO-DOs')
#root.geometry('300x200+600+200')

menu = MenuScreen(root)
root.mainloop()
