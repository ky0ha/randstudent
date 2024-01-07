from tkinter import *
from tkinter import filedialog, dialog, ttk, messagebox, simpledialog
import tkinter.font as tkFont
import const

class MY_GUI:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
    
    def set_init_window(self):
        self.init_window_name.title("随机抽签")
        self.init_window_name.geometry('1680x960+100+25')

        self.init_title_label = Label(self.init_window_name, text='随机抽签程序 v1.0', font=tkFont.Font(family='KaiTi', size=30, weight=tkFont.BOLD))
        self.init_title_label.pack()
        self.empty_label = Label(self.init_window_name, text='')
        self.empty_label.pack()

        s = ttk.Style()
        s.configure("Treeview", rowheight=30, height=20, font=(None, 12))
        s.configure("Treeview.Heading", font=(None, 16))
        
        self.select_item_frame = Frame(self.init_window_name)
        self.select_item_frame.pack(expand=YES)
        
        self.select_label = Label(self.select_item_frame, text="请选择班级：", font=tkFont.Font(family='KaiTi', size=20, weight=tkFont.BOLD))
        self.select_label.pack(side=LEFT)
        
        self.select_combobox = ttk.Combobox(self.select_item_frame, state="readonly")
        self.select_combobox["values"] = ["周五18:30", "周六10:45", "周六13:00", "周六14:45", "周六16:30", "周日09:00", "周日10:45", "周日13:00", "周日16:30"]
        self.select_combobox.current(0)
        self.select_combobox.pack(side=RIGHT, anchor='c', expand='no', padx=5, pady=4)

        self.select_label = Label(self.init_window_name, text="幸运学生是：", font=tkFont.Font(family='KaiTi', size=20, weight=tkFont.BOLD))
        self.select_label.pack()
        self.select_result_label = Label(self.init_window_name, text="", font=tkFont.Font(family='KaiTi', size=30, weight=tkFont.BOLD))
        self.select_result_label.pack(pady=10)

        self.button_frame = Frame(self.init_window_name)
        self.button_frame.pack(expand=True, fill=X)
        self.create_searching_button = Button(self.button_frame, text="添加班级学生", bd=3, font=tkFont.Font(family='KaiTi', size=20), command=self.insert)
        self.create_searching_button.pack(expand=True, side="left")
        self.create_searching_button = Button(self.button_frame, text="开始抽签", bd=3, font=tkFont.Font(family='KaiTi', size=20))
        self.create_searching_button.pack(expand=True, side="left")
        self.create_updating_button = Button(self.button_frame, text="减少班级学生", bd=3, font=tkFont.Font(family='KaiTi', size=20))
        self.create_updating_button.pack(expand=True, side="right")

    def insert(self):
        current_selected = self.select_combobox.get()
        print(current_selected)


def gui_start():
    init_window = Tk()
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()

gui_start()
