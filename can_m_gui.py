#!/usr/bin/env python3

# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk
from tkinter import messagebox
import logging
import sys
import logging

logger = logging.getLogger(__name__)

LARGE_FONT = ("Consolas", 12)
MEDIUM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Verdana", 8)


class MainApplication(tk.Toplevel):
    def __init__(self, master, cfg_file, *args, **kwargs):
        tk.Toplevel.__init__(self, master)
        # use protocol to catch window close and destroy application.
        self.callbacks = {}
        self.protocol('WM_DELETE_WINDOW', self.on_exit_callback)

        container = tk.Frame(self, background = "red")
        container.pack(side="top", fill="both", expand=True)
        
        '''
        row- columnconfigure sets row and column size
        relative to each other. c0=1*c0, c1=3*c0, c2=2*c0.
        Can be seen when window is expanded.
        '''
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=3)
        container.grid_columnconfigure(2, weight=2)

        self.pages = {} # dict of pages
        # for F in (StartPage, PageOne): # Add pages to dict here
        #     page = F(container, self)
        #     self.pages[F] = page
        #     page.grid(row=0, column=0, sticky="nsew")
        #     # self.show_frame(F)

        page = StartPage(container, self)
        page.grid(row=0, column=0, sticky="nsew")
        self.pages["StartPage"] = page
        #self.pages["StartPage"].can_id_entry.insert('end', "Money") 

        ######## Receive widgets
        self.receive_widgets = {}
        self.label_frames = {} # labellist
        self.receive_widget_frame = tk.Frame(container, bg="pink")
        self.receive_widget_frame.grid(row=0, column=1, sticky="nsew")

        if cfg_file is not None:
            for k in cfg_file:
                frame = CanReceiveWidget(self.receive_widget_frame, self, k, cfg_file[k])
                self.receive_widgets[k] = frame
                frame.pack()
                # frame.grid(row=n, column=0, sticky="nsew")

        # data = {"widget": "enginge_speed", "can_data": "apple", "can_info": "pear"}
        # self.receive_widgets["engine_speed"].update_values(logger, data)

    def add_callback(self, callback_name, func):
        self.callbacks[callback_name] = func

    def on_exit_callback(self):
        if self.callbacks.get("exit") is None:
            if messagebox.askokcancel("Close", "Are you sure...?"):
                self.master.destroy()
        else:
            logger.info("running exit callback")
            self.callbacks["exit"]()
            self.master.destroy()

    def show_frame(self, cont):
        '''
        Raise frame (Page) to top. This is needed
        when multiple frames are stacked on top of
        each other thus making only the top frame
        visible.

        arg:
            cont, frame to raise
        '''

        page = self.pages[cont]
        page.tkraise()

    def updated_text(self, text):
        # label = self.receive_widgets["widdy1"].labels_dict["canaddr"]["title"]
        # label.set(text)
        pass


########################################## pages/widgets ##########################################

## For creating a new page copy this class and modify
class StartPage(tk.Frame): # Page example 1
    '''
    This class is a new page that will initialize itself as a frame.
    This frame can then be populated with whatever is needed using
    self. EX: tk.Label(self). Parent of this page is whatever is passed
    which in this case is container, see line: frame = F(container, self).
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="green") # create a local frame

        self.id_frame = tk.Frame(self)
        self.id_frame.grid_rowconfigure(0, weight=1)
        self.id_frame.grid_rowconfigure(1, weight=1)
        self.id_frame.grid_columnconfigure(0, weight=1)
        self.id_frame.grid_columnconfigure(1, weight=10)

        self.id_frame.pack()
        self.id_label = tk.Label(self.id_frame, text="CAN ID", font=LARGE_FONT)
        self.id_label.grid(row=0, column=0, sticky="w")
        self.can_id_entry = tk.Entry(self.id_frame, width=10)
        self.can_id_entry.grid(row=0, column=1, sticky="w")

        self.name_label = tk.Label(self.id_frame, text="CAN Name", font=LARGE_FONT)
        self.name_label.grid(row=1, column=0, sticky="w")
        self.can_name_entry = tk.Entry(self.id_frame, width=23)
        self.can_name_entry.grid(row=1, column=1, sticky="w")

        self.label = tk.Label(self.id_frame, text="CAN Data", font=LARGE_FONT)
        self.label.grid(row=2, column=0, sticky="w")
        self.can_entry = tk.Entry(self.id_frame, width=23)
        self.can_entry.grid(row=2, column=1, sticky="w")

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack()
        self.btn0 = tk.Button(self.btn_frame, text="send can")
        self.btn0.grid(row=0, column=0)
        self.btn1 = tk.Button(self.btn_frame, text="read can")
        self.btn1.grid(row=0, column=1)
        self.btn2 = tk.Button(self.btn_frame, text="stop can")
        self.btn2.grid(row=0, column=2)


    def set_entry(self, text):
        print("in set entry")
        self.can_id_entry.delete(0,'end')
        self.can_id_entry.insert('end', text)     


    def get_entry_data(self):
        print("inside get_entry_data")
        entry_data = {
                      "can_id_entry": self.can_id_entry.get(),
                      "can_name_entry": self. can_name_entry.get()
                      }
        return entry_data

class PageOne(tk.Frame): # Page example 2
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="yellow")
        label = tk.Label(self, text="Hello Earth", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        btn = tk.Button(self, text="Prev", command=lambda: controller.show_frame(StartPage))
        btn.pack()


class CanReceiveWidget(tk.Frame): # Example to create multiple labels
    def __init__(self, parent, controller, widget_name="ReceiveWidget", labels_to_build=None):
        tk.Frame.__init__(self, parent, background="light blue", borderwidth=1)

        '''
        create widget for can data receieve.

        input:
            parent: frame
            logger: Logger
            controller: Parent object
            widget_name: str
            labels_to_build: dict

        '''
        self.widget_name = tk.Label(self, text=widget_name, font=LARGE_FONT)
        self.widget_name.pack(pady=5, padx=5)
        grid_frame = tk.Frame(self, bg="light green")
        grid_frame.pack()

        label_titles = {
                        "can_name": "CAN name:",
                        "can_id": "CAN ID:",
                        "can_id_dec": "CAN ID dec:",
                        "can_data": "CAN data:",
                        "can_full": "CAN full:",
                        "can_info": "CAN info:"
        }

        self.labels_entries = {}
        
        grid_r = grid_c = 0
        cfg_keys = label_titles.keys()

        logger.debug("widget build data %s", labels_to_build)

        for lbl in labels_to_build:
            if lbl in cfg_keys:
                _temp_dict = {}
                label_title_var = tk.StringVar()
                label_title_var.set(label_titles[lbl])
                label = tk.Label(grid_frame, textvariable=label_title_var, font=MEDIUM_FONT)
                label.grid(row=grid_r, column=0, sticky="w")
                _temp_dict["title"] = label_title_var

                entry_value_var = tk.StringVar()
                entry_value_var.set(labels_to_build[lbl])
                label = tk.Entry(grid_frame, textvariable=entry_value_var, 
                                 width=23, font=MEDIUM_FONT, state='readonly',
                                 bd=0,)
                label.grid(row=grid_r, column=1, sticky="w")
                _temp_dict["value"] = entry_value_var
                logger.debug("created %s [%s %s]",lbl, label_titles[lbl], labels_to_build[lbl])
                grid_r += 1

                self.labels_entries[lbl] = _temp_dict

    def update_values(self, data_values):
        self.labels_entries
        keys = []

        for k in self.labels_entries:
            keys.append(k)

        logger.debug("update values - keys: %s # data_values: %s # labels_entries: %s",
                     keys, data_values, self.labels_entries)
        for entry in data_values:
            if entry in keys:
                logger.debug("found match on '%s' with value '%s'", entry, data_values[entry])
                self.labels_entries[entry]["value"].set(data_values[entry])
            else:
                logger.warning("[widget:%s] no '%s' object found to update", 
                               self.widget_name.cget("text"), entry)

    def update_label(self, label, sub, data_val):
        frame = self.labels_dict[label]
        # frame = self.frames[CanReceiveWidget]
        print("In update label")
        for val in data_val:
            if val == "data":
                frame["value"].set(data_val[val])


class LabelTwo(tk.Frame): # Example to create multiple labels (grey)
    def __init__(self, parent, controller, nr_of_labels):
        tk.Frame.__init__(self, parent, background="grey")
        for i in range(nr_of_labels):
            label = tk.Label(self, text="Created in frame LabelTwo", font=LARGE_FONT)
            label.pack()

if __name__ == '__main__':
    # Run app if started as main
    cfg_file = {"Test_data": {
                              "can_name": "EEC1",
                              "can_id": "0X00",
                              "can_data": "0X998877665544332211",
                              "can_full": "0X00#998877665544332211",
                              }
                }

    app = MainApplication(cfg_file)
    app.mainloop()
