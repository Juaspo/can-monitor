# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk

LARGE_FONT = ("Consolas", 12)
MEDIUM_FONT = ("Consolas", 10)
SMALL_FONT = ("Verdana", 8)


class MainApplication(tk.Tk):

    def __init__(self, *args, **kwargs):
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

        self.frames = {} # dict of pages
        self.label_frames = {} # labellist
        self.receive_widgets = {}


        for F in (StartPage, PageOne): # Add pages to dict here
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            # self.show_frame(F)


        frame = CanReceiveWidget(container, self)
        self.receive_widgets["widdy1"] = frame
        frame.grid(row=0, column=1, sticky="nsew")


        for X in range(3):
            frame = LabelTwo(container, self, 3)
            frame.grid(row=X, column=2, sticky="nsew")


    def show_frame(self, cont):
        '''
        Raise frame (Page) to top. This is needed
        when multiple frames are stacked on top of
        each other thus making only the top frame
        visible.

        arg:
            cont, frame to raise
        '''

        frame = self.frames[cont]
        frame.tkraise()

    

########################################## Example pages ##########################################

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
        self.label0 = tk.Label(self, text="Hello World", font=LARGE_FONT)
        self.label0.pack(pady=10,padx=10)

        # Creating a label on parent frame (container)
        label1 = tk.Label(parent, text="Created on parent", font=LARGE_FONT)
        label1.grid(row=1, column=0) # since parent (container) is grid, pack cannot be used

        btn = tk.Button(self, text="Go2", command=lambda: controller.show_frame(PageOne))
        btn.pack()


class PageOne(tk.Frame): # Page example 2
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="yellow")
        label = tk.Label(self, text="Hello Earth", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        btn = tk.Button(self, text="Go1", command=lambda: controller.show_frame(StartPage))
        btn.pack()


class CanReceiveWidget(tk.Frame): # Example to create multiple labels
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="light blue")
        self.label_var=tk.StringVar()

        labels_to_build={
                         "canaddr": {"title": "CAN addr", "value": "0X00"},
                         "candata": {"title": "CAN data", "value": "0X998877665544332211"},
                         "fullcan": {"title": "CAN full", "value": "0X00#998877665544332211"},
        }
        self.labels_dict = {}
        lbl_dict = {}
        grid_r = grid_c = 0

        for lbls in labels_to_build:

            for lb_content in labels_to_build[lbls]:
                # print("lbls: ", lbls, "\nlb_content: ", lb_content)
                ###################/// why not working!!??
                self.label_var.set(str(labels_to_build[lbls][lb_content]))
                label = tk.Label(self, text=self.label_var, font=LARGE_FONT)
                

                label.grid(row=grid_r, column=grid_c, sticky="w")
                lbl_dict[lb_content] = label
                grid_c += 1

            self.labels_dict[lbls] = lbl_dict
            grid_r += 1
            grid_c = 0


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
            print("create nr", i)
            label = tk.Label(self, text="Created in frame LabelTwo", font=LARGE_FONT)
            label.pack()

if __name__ == '__main__':
    # Run app if started as main
    app = MainApplication()
    app.mainloop()
