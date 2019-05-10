"""
Program Created By:
David Ellis  ID: 3728275  Email: ellisd5@lsbu.ac.uk
Elliott Gipson  ID: ...  Email: gipsone@lsbu.ac.uk
"""

from datetime import date
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import calendar

# this is effectively a list that prints the contents one by one
class __Database(list):
    def __str__(self):
        for item in self:
            print(item)


# this is the foundation of all screens
class ScreenBase(Frame):
    def __init__(self, master):
        self.months = {name: num for num, name in enumerate(calendar.month_name) if num}
        super().__init__(master)  # this initialises the parent class
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        pass


class ToDo(object):
    def __init__(self, description, start_date=date.today(), due_date=None, priority=5, status='Incomplete', reminder=0):
        self.description = description
        self.start = start_date
        self.due = due_date
        self.priority = float(priority)
        self.status = status
        self.reminder = int(reminder)

    # this is a special method that is called whenever the object is printed
    def __str__(self):
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
        except FileNotFoundError:
            pass
        self.reminders()

    def create_widgets(self):
        image = Image.open('LSBU Logo.png')
        photo = ImageTk.PhotoImage(image)
        logo = Label(self, image=photo)
        logo.image = photo

        add_todo = Button(self, text='Add TO-DO', command=self.add_to_do)
        to_dos = Button(self, text='TO-DOs', command=self.to_dos)
        reminder = Button(self, text='Reminders', command=self.reminders)
        exit = Button(self, text='Exit', command=self.master.destroy)

        logo.grid(column=0, row=0)
        add_todo.grid(column=0, row=1)
        to_dos.grid(column=0, row=2)
        reminder.grid(column=0, row=3)
        exit.grid(column=0, row=4)

    def add_to_do(self):
        AddTODOScreen(self.master)

    def to_dos(self):
        DatabaseScreen(self.master)

    def reminders(self):
        for todo in Database:
            if int(todo.reminder) and (todo.due - date.today()).total_seconds() <= 172800 and todo.status != 'Finished':
                ReminderScreen(self.master, todo)


class DatabaseScreen(ScreenBase):
    def __init__(self, master):
        self.todos = Toplevel(master)
        self.todos.title('TO-DOs To Do')
        super().__init__(master)
        self.master = master

    def create_widgets(self):

        class ModifyLater(object):
            def __init__(self, screen, master_screen, todo):
                self.todo = todo
                self.master = master_screen
                self.screen = screen

            # this special method is called when an instance of this class is called
            def __call__(self):
                self.screen.todos.destroy()
                ModifyScreen(self.master, self.todo)

        class DeleteLater(object):
            def __init__(self, master_screen, todo):
                self.todo = todo
                self.master = master_screen
                self.widgets = []

            # this special method is called when an instance of this class is called
            def __call__(self):
                for widget in self.widgets:
                    widget.grid_remove()
                self.todo.delete()

            def widgets_to_kill(self, widgets):
                for widget in widgets:
                    self.widgets.append(widget)

        title = Label(self.todos, text='TO-DOs To Do:')

        count = 0
        for item in Database:
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
        start_day = Spinbox(self.add_window, from_=1, to=31, width=2, textvariable=self.start_day)
        start_month = Combobox(self.add_window, values=calendar.month_name[1:], width=9, textvariable=self.start_month)
        start_month.set(calendar.month_name[today.month])
        start_year = Spinbox(self.add_window, from_=today.year, to=today.year+100, width=4, textvariable=self.start_year)

        due_date_label = Label(self.add_window, text='Due Date: ')
        due_day = Spinbox(self.add_window, from_=1, to=31, width=2, textvariable=self.due_day)
        due_month = Combobox(self.add_window, values=calendar.month_name[1:], width=9, textvariable=self.due_month)
        due_month.set(calendar.month_name[today.month])
        due_year = Spinbox(self.add_window, from_=today.year, to=today.year+100, width=4, textvariable=self.due_year)

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

        self.master = master

    def create_widgets(self):
        today = date.today()

        description_label = Label(self.modify_window, text='Description: ')
        description = Entry(self.modify_window, textvariable=self.description)

        start_date_label = Label(self.modify_window, text='Start Date: ')
        start_day = Spinbox(self.modify_window, from_=1, to=31, width=2, textvariable=self.start_day)
        start_month = Combobox(self.modify_window, values=calendar.month_name[1:], width=9, textvariable=self.start_month)
        start_year = Spinbox(self.modify_window, from_=today.year, to=today.year+100, width=4, textvariable=self.start_year)

        due_date_label = Label(self.modify_window, text='Due Date: ')
        due_day = Spinbox(self.modify_window, from_=1, to=31, width=2, textvariable=self.due_day)
        due_month = Combobox(self.modify_window, values=calendar.month_name[1:], width=9, textvariable=self.due_month)
        due_year = Spinbox(self.modify_window, from_=today.year, to=today.year+100, width=4, textvariable=self.due_year)

        priority_label = Label(self.modify_window, text='Priority: ')
        priority = Scale(self.modify_window, orient=HORIZONTAL, length=100, from_=0, to=10, variable=self.priority)

        status_label = Label(self.modify_window, text='Status: ')
        states = ['Not Started', 'In Progress', 'Finished']
        status = Combobox(self.modify_window, values=states, textvariable=self.status)

        reminder_label = Label(self.modify_window, text='Reminder: ')
        reminder = Checkbutton(self.modify_window, onvalue=1, offvalue=0, variable=self.reminder)

        modify = Button(self.modify_window, text='Modify', command=self.modify_to_do)
        cancel = Button(self.modify_window, text='Cancel', command=self.destroy)

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
        self.destroy()

    def find_month_by_num(self, month_number):
        return list(self.months.keys())[list(self.months.values()).index(month_number)]

    def destroy(self):
        self.modify_window.destroy()
        DatabaseScreen(self.master)


class ReminderScreen(ScreenBase):
    def __init__(self, master, todo):
        self.reminder_window = Toplevel(master)
        self.reminder_window.title('ATTENTION!')
        self.reminder_window.attributes("-topmost", True)  # keeps window ontop of others
        self.todo = todo
        super().__init__(master)

    def create_widgets(self):
        text = '%s is nearly due:' % self.todo.description
        reminder = Label(self.reminder_window, text=text, font=('Helvetica', 20, 'bold'))
        due_text = 'Due Date: %s' % self.todo.due
        due = Label(self.reminder_window, text=due_text, font=('Helvetica', 20))

        close = Button(self.reminder_window, text='Close', command=self.reminder_window.destroy)
        disable = Button(self.reminder_window, text='Disable Reminder', command=self.disable_reminder)
        complete = Button(self.reminder_window, text='Complete', command=self.complete_todo)

        reminder.grid(column=1, row=0)
        due.grid(column=1, row=1)
        close.grid(column=0, row=2)
        disable.grid(column=1, row=2)
        complete.grid(column=2, row=2)

    def disable_reminder(self):
        self.todo.reminder = 0
        write_to_file()
        self.reminder_window.destroy()

    def complete_todo(self):
        self.todo.status = 'Finished'
        self.todo.reminder = 0
        write_to_file()
        self.reminder_window.destroy()


def write_to_file():
    # gets all data from database list, puts it all in a string and writes that string to the database file
    to_write = ""
    for todo in Database:
        for item in todo.attributes():  # iterates through the important attributes of todo
            to_write += "%s," % todo.__getattribute__(item)  # appends the value of the current object attribute to the write string
        to_write += "\n"  # adds new line at end of every todo
    # writes
    with open('database.csv', 'w') as fp:
        fp.write(to_write)


def get_file_contents():
    # reads all data in database file and sores is in a list
    with open('database.csv', 'r') as fp:
        for todo in fp:  # todos are separated by a new line
            args = todo.split(',')  # attributes are separated by ','s
            Database.append(ToDo(*args[:6]))  # uses stored data, excluding '\n' to recreate todo objects
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


if __name__ == '__main__':
    Database = __Database()

    root = Tk()
    root.title('TO-DOs')

    menu = MenuScreen(root)
    root.mainloop()
