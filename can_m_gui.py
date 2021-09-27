# Use Tkinter for python 2, tkinter for python 3
import tkinter as tk

LARGE_FONT = ("Verdana", 12)

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

        '''
        This loop example below creates multiple windows in same
        grid position (0,0). This means grids are created on top
        of each other and therefore needs to be raised to be
        visible 'show_frame(F)'. It will create pages that are
        defined in loop.
        '''
        for F in (StartPage, PageOne): # Add pages to dict here
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            # self.show_frame(F)


        '''
        This will create a new page (LabelOne) on grid pos (0,1).
        This page will thus be created next to the previous pages
        and will be visible on creation.
        '''
        frame = LabelOne(container, self)
        frame.grid(row=0, column=1, sticky="nsew")


        '''
        This loop will create multiple pages on grid pos (n,2).
        Each page will be created below and will therefor be
        visible whitout using show_frame().
        '''
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

    # def create_labels(self, nr_of_labels, frame):

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
        label = tk.Label(self, text="Hello World", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        # Creating a label on parent frame (container)
        label = tk.Label(parent, text="Created on parent", font=LARGE_FONT)
        label.grid(row=1, column=0) # since parent (container) is grid, pack cannot be used

        btn = tk.Button(self, text="Go2", command=lambda: controller.show_frame(PageOne))
        btn.pack()


class PageOne(tk.Frame): # Page example 2
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="yellow")
        label = tk.Label(self, text="Hello Earth", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        btn = tk.Button(self, text="Go1", command=lambda: controller.show_frame(StartPage))
        btn.pack()


class LabelOne(tk.Frame): # Example to create multiple labels
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="blue")

        # Creating multiple labels on self frame.
        nr_of_labels = 5
        for i in range(nr_of_labels):
            print("create nr", i)
            label = tk.Label(self, text="Created in frame LabelOne", font=LARGE_FONT)
            label.pack()
            # self.show_frame(LabelOne)


class LabelTwo(tk.Frame): # Example to create multiple labels (grey)
    def __init__(self, parent, controller, nr_of_labels):
        tk.Frame.__init__(self, parent, background="grey")
        for i in range(nr_of_labels):
            print("create nr", i)
            label = tk.Label(self, text="Created in frame LabelTwo", font=LARGE_FONT)
            label.pack()


app = MainApplication()
app.mainloop()
