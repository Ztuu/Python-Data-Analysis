# This work is licensed under the Creative Commons Attribution 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/
# or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

# Code based on Industrial Programming Python samples : feet2meter.py
from tkinter import *
from tkinter import ttk
import TaskController as tc

class DataGUI:

    # Methods for starting each individual task when corresponding button is pressed
    def CountCountry(self):
        self.StartTask('2a')

    def CountContinent(self):
        self.StartTask('2b')

    def CountFullBrowser(self):
        self.StartTask('3a')

    def CountShortBrowser(self):
        self.StartTask('3b')

    def AlsoLikes(self):
        self.StartTask('4d')

    def AlsoLikesGraph(self):
        self.StartTask('5')

    def StartTask(self, task_id):
        """Reads inputs from GUI text fields and starts the correct task if input is valid"""
        inp_doc_ID = self.docID.get()
        inp_user_id = self.userID.get()
        inp_filename = self.filename.get()

        if inp_doc_ID == "" or inp_filename == "":
            print("Please enter at least both a document uuid and filename")
        else:
            # Close the GUI before displaying results
            self.root.destroy()
            tc.TaskController(inp_filename, task_id, inp_doc_ID, inp_user_id)

    def __init__(self):
        self.root = Tk()
        self.root.title("SP96 Data Analysis")

        # Configure window
        mainframe = ttk.Frame(self.root, padding="12 12 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        # Text fields
        self.docID = StringVar()
        self.userID = StringVar()
        self.filename = StringVar()

        docID_entry = ttk.Entry(mainframe, width=7, textvariable=self.docID)
        docID_entry.grid(column=2, row=1, columnspan=2, sticky=(W, E))
        userID_entry = ttk.Entry(mainframe, width=7, textvariable=self.userID)
        userID_entry.grid(column=2, row=2, columnspan=2, sticky=(W, E))
        filename_entry = ttk.Entry(mainframe, width=7, textvariable=self.filename)
        filename_entry.grid(column=2, row=3, columnspan=2, sticky=(W, E))

        # Buttons for calling tasks
        ttk.Button(mainframe, text="2a", command=self.CountCountry).grid(column=1, row=4, sticky=W)
        ttk.Button(mainframe, text="2b", command=self.CountContinent).grid(column=2, row=4, sticky=W)
        ttk.Button(mainframe, text="3a", command=self.CountFullBrowser).grid(column=3, row=4, sticky=W)
        ttk.Button(mainframe, text="3b", command=self.CountShortBrowser).grid(column=1, row=5, sticky=W)
        ttk.Button(mainframe, text="4d", command=self.AlsoLikes).grid(column=2, row=5, sticky=W)
        ttk.Button(mainframe, text="5", command=self.AlsoLikesGraph).grid(column=3, row=5, sticky=W)

        # Text field labels
        ttk.Label(mainframe, text="Doc UUID").grid(column=1, row=1, sticky=E)
        ttk.Label(mainframe, text="User UUID").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="Filename").grid(column=1, row=3, sticky=E)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        docID_entry.focus()  # Start entering text in top most field immediately
        # root.bind('<Return>', calculate)  # Searches when return key pressed

        self.root.mainloop()
