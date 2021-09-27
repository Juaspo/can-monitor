'''
can_monitor_gui.py
GUI main for can-monitor


'''
from can_monitor import create_logger
from can_monitor import get_config
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class App:
    def __init__(self, master):
        # tabControl = ttk.Notebook(top)          # Create Tab Control
        # tab1 = ttk.Frame(tabControl)            # Create a tab
        # tabControl.add(tab1, text='WOL')        # Add the tab
        # tabControl.pack(expand=1, fill="both")  # Pack to make visible

        #top.geometry("100x100")
        self.main_frame0 = Frame(master)
        self.main_frame0.pack()

        self.main_frame1 = Frame(self.main_frame0)
        self.main_frame1.pack()

        main_frame1_1 = Frame(self.main_frame0, highlightbackground="black", highlightthickness=1, pady=5)
        main_frame1_1.pack()

        label = Label(self.main_frame1, pady=20, width=24, relief=RIDGE, text="WOL", wraplength=250, bg="white", fg="black", font="sans 12 bold")
        label.pack()

        gen_label = Label(main_frame1_1, text="Broadcast address", fg="black", width = 17)
        gen_label.grid(row = 0, column = 0)
        general_ip_entry = Entry(main_frame1_1, width = 15)
        general_ip_entry.grid(row = 0, column = 1)

        main_frame1_2 = Frame(main_frame1_1)
        main_frame1_2.grid(row=1, column=0)

        repeat_label = Label(main_frame1_2, text="Repeat ping", fg="black", width = 10)
        repeat_label.grid(row = 0, column = 1)
        repeat_ping_entry = Entry(main_frame1_2, width = 3)
        repeat_ping_entry.grid(row = 0, column = 0)

        quit_after_wol_var=BooleanVar()

        quit_cb = Checkbutton(main_frame1_1, width = 12, text="Quit after", variable=quit_after_wol_var, onvalue=True, offvalue=False)
        quit_cb.grid(row = 1, column = 1)

        #test_button = Button(main_frame1_1, text="test", command=debug_def)
        #test_button.grid(row=2, column=0)

        self.frames = []
        self.mac_labels = []
        self.btn = []
        self.ip_labels = []

        ############################################# Configurations

        # tab3 = ttk.Frame(tabControl)            # Create a tab
        # tabControl.add(tab3, text='Configure')      # Add the tab
        # tabControl.pack(expand=1, fill="both")  # Pack to make visible

        # conv_frame2 = Frame(tab3)
        # conv_frame2.pack()


        ################################## Functions

    def remove_buttons_and_labels(self):
        global frames
        global mac_labels
        global btn
        global ip_labels

        for i in range(len(frames)):
            frames[i].destroy()
            mac_labels[i].destroy()
            btn[i].destroy()
            ip_labels[i].destroy()

    def quit_func(self):
        print ("good bye")
        top.destroy()


    def set_btn_labels(self):
        '''
        Functions for creating buttons and
        text fields
        '''

        # config_content = get_config()
        config_content = {"t0": 0, "t1": 100, "t2": 200}
        number_of_items = len(config_content)
        # if "Config" in config_content:
        #     number_of_items -= 1
        self.create_buttons_and_labels(number_of_items)

        n = 0

        for devices in config_content:
            if devices != "Config":
                try:
                    # print("number:",n)
                    self.btn[n].config(text = devices)
                    mac = 23
                    
                    ip_addr=config_content[devices]
                    ip_labels[n].config(text=ip_addr)

                    n += 1
                except KeyError:
                    print("Error with key:", devices)
        return

    def create_buttons_and_labels(self, nr_to_create):
        global frames
        global mac_labels
        global btn
        global ip_labels

        for i in range(nr_to_create):
            print("create:",i)
            self.frames.append(Frame(self.main_frame0, pady=5))
            self.frames[-1].pack()

            self.mac_labels.append(Label(self.frames[-1], text="MAC", fg="black", font="Verdana 10 bold"))
            self.mac_labels[-1].grid(row = 0, column = 0)

            self.btn.append(Button(self.frames[-1], text="No host", width = 15, command=lambda n=i: btn_action(n)))
            self.btn[-1].grid(row = 0, column = 1)

            self.ip_labels.append(Label(self.frames[-1], text="IP", fg="black"))
            self.ip_labels[-1].grid(row = 1, column = 0)

    def set_configuration(self):
        # config_content = get_config()
        config_content = "test"
        if "test" in config_content:
            try:
                general_ip_entry.delete(0, END)
                general_ip_entry.insert(0, "general ip entry")
                repeat_ping_entry.delete(0, END)
                repeat_ping_entry.insert(0, "99")

            except Exception as e:
                print("config error:", e)
                label.config(text=f"CFG error: {e}")

        else:
            general_ip_entry.delete(0, END)
            general_ip_entry.insert(0, "Bad config")
            return False

def main(argv):

    top = Tk()
    top.minsize(width=250, height=150)
    top.title("Can Monitor")

    app = App(top)
    app.set_btn_labels()
    app.set_configuration()
    
    top.mainloop()


    # try:
    #     opts, args = getopt.getopt(argv, "hs:t:", ["help"])
    # except getopt.GetoptError:
    #     print("Wrong input try -h for help")
    #     sys.exit(2)

    # for opt, arg in opts:
    #     print("arg:", arg)
    #     if opt in ("-h", "--help"):
    #         print("\nTimeCounter help screen\n")
    #         print("-h\tfor this help text\n-s\tfor auto start\n-t\tfor timestamp")
    #         sys.exit()
    #     elif opt == "-t":
    #         timestamp(arg)
    #         take_timestamp = True
    #     elif opt == "-s":
    #         run_end_clocking(arg)
    #         autostart = True

        # print ("auto start:", autostart, "timestamp:", take_timestamp, "argv:", argv, "opts:", opts)

if __name__ == '__main__':
    main(sys.argv[1:])

