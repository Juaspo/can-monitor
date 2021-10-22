#!/usr/bin/env python3

# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk
from tkinter import messagebox
import logging
import sys
import logging

logger = logging.getLogger(__name__)

LARGE_FONT = ("Helvetica", 12)
MEDIUM_FONT = ("Consolas", 10)
SMALL_FONT = ("Verdana", 8)


class MainApplication(tk.Toplevel):
    def __init__(self, master, cfg_file, *args, **kwargs):
        tk.Toplevel.__init__(self, master)
        # use protocol to catch window close and destroy application.
        self.callbacks = {}
        self.protocol('WM_DELETE_WINDOW', self.on_exit_callback)

        container = tk.Frame(self)
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

        ########## Send widgets
        self.send_widgets = {}
        self.send_widget_frame = tk.Frame(container)
        self.send_widget_frame.grid(row=0, column=1, sticky="nsew")

        self.create_widgets(cfg_file["can_send"], self.send_widget_frame, "send", self.send_widgets)

        ######## Receive widgets
        self.receive_widgets = {}
        self.receive_widget_frame = tk.Frame(container)
        self.receive_widget_frame.grid(row=0, column=2, sticky="nsew")

        self.create_widgets(cfg_file["can_receive"], self.receive_widget_frame, "receive", self.receive_widgets)

        # logger.debug("contents of send widget dicts: %s", self.send_widgets)
        # logger.debug("contents of rece widget dicts: %s", self.receive_widgets)

    def create_widgets(self, cfg_file, widget_frame, widget_type, add_to_dict=None):
        # logger.debug("cfg in create widget: %s", cfg_file)
        widget_key=None
        widget_name=None

        widgets_to_run = {"send": CanSendWidget,
                          "receive": CanReceiveWidget
                          }
        if cfg_file is not None and widgets_to_run.get(widget_type, None):
            for k in cfg_file:
                # logger.debug(k)
                try:
                    if widget_type == "receive":
                        widget_key = int(k, 0)
                        widget_name = cfg_file[k].get("can_name", None)
                    elif widget_type == "send":
                        widget_key = k
                        widget_name = k
                    frame = widgets_to_run[widget_type](widget_frame,
                                             k, widget_name, cfg_file[k])
                    frame.pack()
                    add_to_dict[widget_key] = frame
                except ValueError as e:
                    logger.error("Wrong format of HEX for %s: %s", k, e)

            return add_to_dict
        else:
            logger.error("Wrong widget type [%s] or config [%s] sent to create_widgets",
                         widget_type, cfg_file)
                # frame.grid(row=n, column=0, sticky="nsew")
        # logger.debug("widgets created: %s", self.receive_widgets)
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
        tk.Frame.__init__(self, parent) # create a local frame

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
        self.btn1 = tk.Button(self.btn_frame, text="start can")
        self.btn1.grid(row=0, column=1)
        self.btn2 = tk.Button(self.btn_frame, text="stop can")
        self.btn2.grid(row=0, column=2)

        self.filter_check = tk.BooleanVar()
        self.filter_check.set(False)
        self.continous_run = tk.BooleanVar()
        self.continous_run.set(False)
        self.check_box_frame = tk.Frame(self)
        self.check_box_frame.pack()
        self.check0 = tk.Checkbutton(self.check_box_frame, variable=self.filter_check, text="Filter messages")
        self.check0.grid(row=0, column=0)
        self.check1 = tk.Checkbutton(self.check_box_frame, variable=self.continous_run, text="Continous run")
        self.check1.grid(row=0, column=1)


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
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Hello Earth", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        btn = tk.Button(self, text="Prev", command=lambda: controller.show_frame(StartPage))
        btn.pack()


class CanReceiveWidget(tk.Frame): # Example to create multiple labels
    def __init__(self, parent, can_id, widget_name=None, labels_to_build=None):
        tk.Frame.__init__(self, parent, borderwidth=1)

        '''
        create widget for can data receieve.

        input:
            parent: frame
            logger: Logger
            controller: Parent object
            widget_name: str
            labels_to_build: dict

        '''
        self.widget_name = widget_name

        if self.widget_name is None:
            self.widget_name = "Recieve Widget"
        widget_title_lbl = tk.Label(self, text=self.widget_name, font=LARGE_FONT)
        widget_title_lbl.pack(pady=5, padx=5)
        grid_frame = tk.Frame(self)
        grid_frame.pack()

        label_titles = {
                        "can_id": "CAN ID:",
                        "can_name": "CAN name:",
                        "can_label": "CAN label:",
                        "can_id_dec": "CAN ID dec:",
                        "can_value": "CAN value",
                        "can_data": "CAN data:",
                        #"can_full": "CAN full:",
                        "can_info": "CAN info:"
        }

        self.labels_entries = {}
        
        grid_r = grid_c = 0
        cfg_keys = label_titles.keys()
        # logger.debug("widget build data %s", labels_to_build)

        for lbl in labels_to_build:
            if lbl in cfg_keys:
                _temp_dict = {}
                label_title_var = tk.StringVar()
                label_title_var.set(label_titles[lbl])
                label = tk.Label(grid_frame, textvariable=label_title_var, 
                                 width=10, font=MEDIUM_FONT, anchor='w')
                label.grid(row=grid_r, column=0)
                _temp_dict["title"] = label_title_var

                entry_value_var = tk.StringVar()
                if(lbl == "can_id" and labels_to_build[lbl]):
                    entry_value_var.set(can_id)
                elif(lbl == "can_id_dec" and labels_to_build[lbl]):

                    entry_value_var.set(int(can_id, 0))
                else:
                    entry_value_var.set(labels_to_build[lbl])

                entry = tk.Entry(grid_frame, textvariable=entry_value_var, 
                                 width=24, font=MEDIUM_FONT, state='readonly',
                                 bd=0,)
                entry.grid(row=grid_r, column=1, sticky="w")
                _temp_dict["value"] = entry_value_var
                # logger.debug("created %s [%s %s]",lbl, label_titles[lbl], labels_to_build[lbl])
                grid_r += 1

                self.labels_entries[lbl] = _temp_dict
        # logger.debug(self.labels_entries)

    def update_values(self, data_values):
        self.labels_entries
        keys = []

        for k in self.labels_entries:
            keys.append(k)

        # logger.debug("update values - keys: %s # data_values: %s # labels_entries: %s",
        #              keys, data_values, self.labels_entries)
        for entry in data_values:
            if entry in keys:
                logger.debug("found match on '%s' with value '%s'", entry, data_values[entry])
                self.labels_entries[entry]["value"].set(data_values[entry])
            else:
                logger.warning("[widget:%s] no '%s' object found to update", 
                               self.widget_name, entry)

    def update_label(self, label, sub, data_val):
        frame = self.labels_dict[label]
        # frame = self.frames[CanReceiveWidget]
        print("In update label")
        for val in data_val:
            if val == "data":
                frame["value"].set(data_val[val])


class CanSendWidget(tk.Frame): # Example to create multiple labels
    def __init__(self, parent, can_id, widget_name, labels_to_build=None):
        tk.Frame.__init__(self, parent, borderwidth=1)

        '''
        create widget for can data receieve.

        input:
            parent: frame
            logger: Logger
            controller: Parent object
            widget_name: str
            labels_to_build: dict

        '''
        if widget_name is None:
            logger.error("'can_name' is None. 'can_name' required for 'can_send' config")
            return None

        widget_title_lbl = tk.Label(self, text=widget_name, font=LARGE_FONT)
        widget_title_lbl.pack(pady=5, padx=5)
        grid_frame = tk.Frame(self)
        grid_frame.pack()

        label_titles = {
                        "can_name": "CAN name:",
                        "can_id": "CAN ID:",
                        "can_id_dec": "CAN ID dec:",
                        "can_label": "CAN label:",
                        "can_value": "CAN value",
                        #"can_data": "CAN data:",
                        #"can_full": "CAN full:",
                        "can_info": "CAN info:",
                        "can_period": "Delay(ms)"
        }

        self.labels_entries = {}

        grid_r = grid_c = 0
        cfg_keys = label_titles.keys()
        # logger.debug("widget build data %s", labels_to_build)
        if labels_to_build.get("get_can", False):
            logger.info("Fetching CAN info")

        for lbl in label_titles:
            _temp_dict = {}
            label_title_var = tk.StringVar()
            label_title_var.set(label_titles[lbl])
            label = tk.Label(grid_frame, textvariable=label_title_var, 
                             width=10, font=MEDIUM_FONT, anchor='w')
            label.grid(row=grid_r, column=0)
            _temp_dict["title"] = label_title_var

            entry_value_var = tk.StringVar()
            entry = tk.Entry(grid_frame, textvariable=entry_value_var, 
                             width=24, font=MEDIUM_FONT, bd=0,
                             )
            entry.grid(row=grid_r, column=1, sticky="w")
            _temp_dict["value"] = entry_value_var
            # logger.debug("created %s [%s %s]",lbl, label_titles[lbl], labels_to_build[lbl])
            self.labels_entries[lbl] = _temp_dict
            grid_r += 1

        if labels_to_build.get("get_can_info"):
            pass
        else:
            for post in labels_to_build:
                if post in cfg_keys:
                    self.labels_entries[post]["value"].set(labels_to_build[post])


        # logger.debug(self.labels_entries)

    def update_values(self, data_values):
        self.labels_entries
        keys = []

        for k in self.labels_entries:
            keys.append(k)

        # logger.debug("update values - keys: %s # data_values: %s # labels_entries: %s",
        #              keys, data_values, self.labels_entries)
        for entry in data_values:
            if entry in keys:
                logger.debug("found match on '%s' with value '%s'", entry, data_values[entry])
                self.labels_entries[entry]["value"].set(data_values[entry])
            else:
                logger.warning("[widget:%s] no '%s' object found to update", 
                               self.widget_name, entry)

    def update_label(self, label, sub, data_val):
        frame = self.labels_dict[label]
        # frame = self.frames[CanReceiveWidget]
        print("In update label")
        for val in data_val:
            if val == "data":
                frame["value"].set(data_val[val])

class LabelTwo(tk.Frame): # Example to create multiple labels (grey)
    def __init__(self, parent, controller, nr_of_labels):
        tk.Frame.__init__(self, parent)
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
