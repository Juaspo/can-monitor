#!/usr/bin/env python3

# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk
import logging
from logging import Logger
import sys

LARGE_FONT = ("Consolas", 12)
MEDIUM_FONT = ("Consolas", 10)
SMALL_FONT = ("Verdana", 8)


class MainApplication(tk.Tk):

    def __init__(self, logger, cfg_file, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
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

        ######## Receive widgets
        self.receive_widgets = {}
        self.label_frames = {} # labellist
        self.receive_widget_frame = tk.Frame(container, bg="pink")
        self.receive_widget_frame.grid(row=0, column=1, sticky="nsew")

        if cfg_file is not None:
            for k in cfg_file:
                frame = CanReceiveWidget(self.receive_widget_frame, self, logger, k, cfg_file[k])
                self.receive_widgets[k] = frame
                frame.pack()
                # frame.grid(row=n, column=0, sticky="nsew")
            print(self.label_frames)

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

        id_frame = tk.Frame(self)
        id_frame.grid_rowconfigure(0, weight=1)
        id_frame.grid_rowconfigure(1, weight=1)
        id_frame.grid_columnconfigure(0, weight=1)
        id_frame.grid_columnconfigure(1, weight=10)

        id_frame.pack()
        id_label = tk.Label(id_frame, text="CAN ID", font=LARGE_FONT)
        id_label.grid(row=0, column=0, sticky="w")
        can_id_entry = tk.Entry(id_frame, width=10)
        can_id_entry.grid(row=0, column=1, sticky="w")

        id_frame.pack()
        name_label = tk.Label(id_frame, text="CAN Name", font=LARGE_FONT)
        name_label.grid(row=1, column=0, sticky="w")
        can_name_entry = tk.Entry(id_frame, width=20)
        can_name_entry.grid(row=1, column=1, sticky="w")

        label = tk.Label(id_frame, text="CAN Data", font=LARGE_FONT)
        label.grid(row=2, column=0, sticky="w")
        can_entry = tk.Entry(id_frame, width=20)
        can_entry.grid(row=2, column=1, sticky="w")

        btn_frame = tk.Frame(self)
        btn_frame.pack()
        btn0 = tk.Button(btn_frame, text="send", command=lambda: controller.show_frame(PageOne))
        btn0.grid(row=0, column=0)
        btn1 = tk.Button(btn_frame, text="next", command=lambda: controller.show_frame(PageOne))
        btn1.grid(row=0, column=1)

class PageOne(tk.Frame): # Page example 2
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="yellow")
        label = tk.Label(self, text="Hello Earth", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        btn = tk.Button(self, text="Prev", command=lambda: controller.show_frame(StartPage))
        btn.pack()


class CanReceiveWidget(tk.Frame): # Example to create multiple labels
    def __init__(self, parent, controller, logger, widget_name="ReceiveWidget", labels_to_build=None):
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
        widget_name = tk.Label(self, text=widget_name, font=LARGE_FONT)
        widget_name.pack(pady=5, padx=5)
        grid_frame = tk.Frame(self, bg="light green")
        grid_frame.pack()

        label_titles = {
                        "can_name": "CAN name:",
                        "can_id": "CAN ID:",
                        "can_data": "CAN data:",
                        "can_full": "CAN full:",
                        "can_info": "CAN info"
        }

        self.labels_dict = {}
        lbl_dict = {}
        grid_r = grid_c = 0
        cfg_keys = label_titles.keys()

        logger.debug("widget build data %s", labels_to_build)

        for lbl in labels_to_build:
            if lbl in cfg_keys:
                # print("lbl: ", lbl, "\nlb_content: ", lb_content)
                label_title_var = tk.StringVar()
                label_title_var.set(label_titles[lbl])
                label = tk.Label(grid_frame, textvariable=label_title_var, font=MEDIUM_FONT)
                label.grid(row=grid_r, column=0, sticky="w")
                lbl_dict["title"] = label_title_var

                label_value_var = tk.StringVar()
                label_value_var.set(labels_to_build[lbl])
                label = tk.Label(grid_frame, textvariable=label_value_var, font=MEDIUM_FONT)
                label.grid(row=grid_r, column=1, sticky="w")
                lbl_dict["value"] = label_value_var
                grid_r += 1

        self.labels_dict[lbl] = lbl_dict


    def update_label(self, label, sub, data_val):
        frame = self.labels_dict[label]
        # frame = self.frames[CanReceiveWidget]
        print("In update label")
        for val in data_val:
            if val == "data":
                pass
                print("Widdy frame:", frame)
                frame["value"].set(data_val[val])


class LabelTwo(tk.Frame): # Example to create multiple labels (grey)
    def __init__(self, parent, controller, nr_of_labels):
        tk.Frame.__init__(self, parent, background="grey")
        for i in range(nr_of_labels):
            label = tk.Label(self, text="Created in frame LabelTwo", font=LARGE_FONT)
            label.pack()

def create_logger(logging_level: str) -> Logger:
    '''
    Set up logger for this script
    input:
        logging_level :string
    return:
        logger :Logger
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, logging_level.upper(), 10))
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                                  datefmt='%Y-%m-%d:%H:%M:%S')
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger

if __name__ == '__main__':
    # Run app if started as main
    cfg_file = {"Test_data": {
                              "can_name": "EEC1",
                              "can_id": "0X00",
                              "can_data": "0X998877665544332211",
                              "can_full": "0X00#998877665544332211",
                              }
                }
    logging_level = "DEBUG"
    logger = create_logger(logging_level)
    logger.info("Logging level set to: %s", logging_level)

    app = MainApplication(logger, cfg_file)
    app.mainloop()
