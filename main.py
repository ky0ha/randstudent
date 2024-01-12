from tkinter import *
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import pickle, logging, random, time, sys, io

import logging

# logger = logging.getLogger('logger')

# # 创建一个格式化器
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# file_handler = logging.FileHandler('my.log')
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)
logging.basicConfig(filename='my.log', level=logging.INFO, filemode='a', format='%(levelname)s:%(asctime)s:%(message)s')

# 创建一个io.StringIO对象来保存标准错误输出
error_output = io.StringIO()
# 重定向标准错误输出到error_output对象
sys.stderr = error_output
# 在这里执行你的代码，任何错误信息都会被保存到error_output中


class MY_GUI:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
    
    def set_init_window(self):
        self.init_window_name.title("随机抽签")
        self.init_window_name.geometry('1024x768+100+25')

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
        # self.select_combobox.current(0)
        self.select_combobox.bind("<<ComboboxSelected>>", self.load_treeview_data)
        self.select_combobox.pack(side=RIGHT, anchor=CENTER, expand=NO, padx=5, pady=4)

        self.currnet_student_frame = Frame(self.init_window_name)
        self.currnet_student_frame.pack(fill=X, padx=100)

        self.current_class_frame = Frame(self.currnet_student_frame)
        self.current_class_frame.pack(side=LEFT, expand=YES)
        self.student_current_label = Label(self.current_class_frame, text="当前班级学生有：", font=tkFont.Font(family='KaiTi', size=20, weight=tkFont.BOLD))
        self.student_current_label.pack()
        columns = ("class", "sname")
        self.class_member_treeview = ttk.Treeview(self.current_class_frame, show='headings', columns=columns, selectmod=BROWSE)
        self.class_member_treeview.column("class", anchor='center')
        self.class_member_treeview.column("sname", anchor='center')
        self.class_member_treeview.heading("class", text="班级")
        self.class_member_treeview.heading("sname", text="学生姓名")
        self.class_member_treeview.pack()

        self.lucky_student_frame = Frame(self.currnet_student_frame)
        self.lucky_student_frame.pack(side=RIGHT, expand=YES, fill=Y)
        self.select_label = Label(self.lucky_student_frame, text="幸运学生是：", font=tkFont.Font(family='KaiTi', size=20, weight=tkFont.BOLD))
        self.select_label.pack(side=TOP, expand=YES)
        self.select_result_label = Label(self.lucky_student_frame, text="", font=tkFont.Font(family='KaiTi', size=50, weight=tkFont.BOLD))
        self.select_result_label.pack(side=TOP, expand=YES)
        self.empty_label = Label(self.lucky_student_frame, text="", font=tkFont.Font(family='KaiTi', size=30, weight=tkFont.BOLD))
        self.empty_label.pack(side=BOTTOM, expand=YES)

        self.button_frame = Frame(self.init_window_name)
        self.button_frame.pack(expand=YES, fill=X)
        self.create_searching_button = Button(self.button_frame, text="添加班级学生", bd=3, font=tkFont.Font(family='KaiTi', size=20), command=self.insert)
        self.create_searching_button.pack(expand=YES, side=LEFT)
        self.create_searching_button = Button(self.button_frame, text="开始抽签", bd=3, font=tkFont.Font(family='KaiTi', size=20), command=self.start)
        self.create_searching_button.pack(expand=YES, side=LEFT)
        self.create_updating_button = Button(self.button_frame, text="减少班级学生", bd=3, font=tkFont.Font(family='KaiTi', size=20), command=self.delete)
        self.create_updating_button.pack(expand=YES, side=RIGHT)
        
        # 0 未选择
        # 1 临时增加
        # 2 永久增加
        # 3 临时减少
        # 4 永久减少
        self.update_mode = {"mode": 0, "value": ""}
        # self.init_window_name.protocol("WM_DELETE_WINDOW", self.on_closing)

    def insert(self):
        class_selected = self.select_combobox.get()
        if class_selected == "":
            messagebox.showerror("错误", "错误：名字不能为空，请选择一个班级。")
            return 0
            
        pw = InsertPopup(self, class_selected)       #弹窗对象的创建和储存
        self.init_window_name.wait_window(pw)       #等待弹窗对象结束
        
        self.raw_data[class_selected].append(self.update_mode["value"])
        self.update_display()
        if self.update_mode["mode"] == 2:
            logging.info(f" {class_selected} 永久增加 \"{self.update_mode['value']}\"")
            with open("class_data.dat", "wb") as f:
                pickle.dump(self.raw_data, f)
        self.update_mode = {"mode": 0, "value": ""}
    
    def delete(self):
        class_selected = self.select_combobox.get()
        student_selected = self.class_member_treeview.selection()
        student_selected = self.class_member_treeview.item(student_selected)["values"][1]
        
        if student_selected == "":
            messagebox.showerror("错误", "错误：名字不能为空，请选择一个要删除的学生。")
            return 0
        
        pw = DeletePopup(self, student_selected)       #弹窗对象的创建和储存
        self.init_window_name.wait_window(pw)       #等待弹窗对象结束
        print(self.raw_data[class_selected], student_selected)
        self.raw_data[class_selected].remove(str(student_selected))
        print(self.raw_data)
        self.update_display()
        print(self.update_mode)
        if self.update_mode["mode"] == 4:
            logging.info(f" {class_selected} 永久删除 \"{self.update_mode['value']}\"")
            with open("class_data.dat", "wb") as f:
                pickle.dump(self.raw_data, f)
                print(self.raw_data)
    
    def load_treeview_data(self, event: Event):
        with open("class_data.dat", "rb") as f:
            self.raw_data = pickle.load(f)
        self.update_display()
    
    def update_display(self):
        data = self.raw_data[self.select_combobox.get()]
        self.class_member_treeview.delete(*self.class_member_treeview.get_children())
        for i in data:
            self.class_member_treeview.insert("", END, values=(self.select_combobox.get(), i))

    def start(self):
        with open("random_data.dat", "rb") as f:
            random_data = pickle.load(f)
        
        current_random_data = {}    # 键为 姓名，值为 次数，取倒数做出权重
        for i in self.raw_data[self.select_combobox.get()]:
            current_random_data[i] = 1 / random_data.get(i, 1)
        print(current_random_data)
        for i in range(30):
            lucky_student = random.choices(list(current_random_data.keys()), weights=list(current_random_data.values()), k=1)
            self.select_result_label.config(text=lucky_student[0])
            self.init_window_name.update()
            time.sleep(0.05)
        random_data[lucky_student[0]] = random_data.setdefault(lucky_student[0], 0) + 1
        print(random_data)
        
        with open("random_data.dat", "wb") as f:
            pickle.dump(random_data, f)
    
    # def on_closing(self):
    #     # 恢复标准错误输出
    #     sys.stderr = sys.__stderr__
    #     # 获取保存的错误信息
    #     error_message = error_output.getvalue()
    #     # 打印错误信息
    #     logging.error(error_message)
    #     self.init_window_name.destroy()
    #     exit()

class PopupDisplay(Toplevel):
    '''
    弹窗部分
    通过构造函数继承父类MY_GUI，并在按钮内显性的更新父类的simulate_mode属性
    更新完成后自动关闭弹窗
    '''
    def __init__(self, parent, current_values):
        super().__init__()
        self.init_window_name = self
        self.parents = parent
        self.current_values = current_values if current_values else ""
        self.set_init_window()
    

class InsertPopup(PopupDisplay):
    def set_init_window(self):
        self.init_window_name.title("选择需要修改的内容")
        self.init_window_name.geometry('600x400+200+200')
        
        self.update_frame = Frame(self.init_window_name)
        self.update_frame.pack(expand=YES)
        self.update_label = Label(self.update_frame, text="请输入要添加的学生姓名：", font=tkFont.Font(family='KaiTi', size=20, weight=tkFont.BOLD))
        self.update_label.pack(pady=50)
        self.student_add_entry = Entry(self.update_frame, font=tkFont.Font(family='KaiTi', size=20))
        self.student_add_entry.pack()
        
        self.confirm_frame = Frame(self.init_window_name)
        self.confirm_frame.pack(fill=X, expand=YES)
        self.temp_confirm_button = Button(self.confirm_frame, text="临时修改", bd=3, font=tkFont.Font(family='KaiTi', size=20), command=self.temp_insert)
        self.temp_confirm_button.pack(padx=5, pady=4, side=LEFT, expand=YES)
        self.confirm_button = Button(self.confirm_frame, text="永久修改", bd=3, font=tkFont.Font(family='KaiTi', size=20), command=self.insert)
        self.confirm_button.pack(padx=5, pady=4, side=LEFT, expand=YES)
        self.cancle_confirm_button = Button(self.confirm_frame, text="取消修改", bd=3, font=tkFont.Font(family='KaiTi', size=20), command=self.init_window_name.destroy)
        self.cancle_confirm_button.pack(padx=5, pady=4, side=RIGHT, expand=YES)

        self.empty_frame = Frame(self.init_window_name)
        self.empty_frame.pack()
    
    def temp_insert(self):
        self.parents.update_mode["mode"] = 1
        self.parents.update_mode["value"] = self.student_add_entry.get()
        self.init_window_name.destroy()
        
    def insert(self):
        confirm = messagebox.askokcancel("警告", "警告：你正在进行敏感操作，是否确认本次操作（本次操作会被记录）！")
        if confirm:
            self.parents.update_mode["mode"] = 2
            self.parents.update_mode["value"] = self.student_add_entry.get()
            self.init_window_name.destroy()

class DeletePopup(PopupDisplay):
    def set_init_window(self):
        self.init_window_name.title("选择删除的方式")
        self.init_window_name.geometry('600x400+200+200')

        self.update_label = Label(self.init_window_name, text="请选择删除使用的模式：", font=tkFont.Font(family='KaiTi', size=20, weight=tkFont.BOLD))
        self.update_label.pack(pady=50)

        self.confirm_frame = Frame(self.init_window_name)
        self.confirm_frame.pack(fill=X, expand=YES)
        self.temp_confirm_button = Button(self.confirm_frame, text="临时修改", bd=3, font=tkFont.Font(family='KaiTi', size=20), command=self.temp_delete)
        self.temp_confirm_button.pack(padx=5, pady=4, side=LEFT, expand=YES)
        self.confirm_button = Button(self.confirm_frame, text="永久修改", bd=3, font=tkFont.Font(family='KaiTi', size=20), command=self.delete)
        self.confirm_button.pack(padx=5, pady=4, side=LEFT, expand=YES)
        self.cancle_confirm_button = Button(self.confirm_frame, text="取消修改", bd=3, font=tkFont.Font(family='KaiTi', size=20), command=self.init_window_name.destroy)
        self.cancle_confirm_button.pack(padx=5, pady=4, side=RIGHT, expand=YES)

        self.empty_frame = Frame(self.init_window_name)
        self.empty_frame.pack()
    
    def temp_delete(self):
        self.parents.update_mode["mode"] = 3
        self.parents.update_mode["value"] = self.current_values
        self.init_window_name.destroy()
        
    def delete(self):
        confirm = messagebox.askokcancel("警告", "警告：你正在进行敏感操作，是否确认本次操作（本次操作会被记录）！")
        if confirm:
            self.parents.update_mode["mode"] = 4
            self.parents.update_mode["value"] = self.current_values
            self.init_window_name.destroy()


def gui_start():
    init_window = Tk()
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()

gui_start()

# 恢复标准错误输出
sys.stderr = sys.__stderr__
# 获取保存的错误信息
error_message = error_output.getvalue()
# 打印错误信息
if error_message:
    logging.error(error_message)