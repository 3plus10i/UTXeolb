# -*- coding: utf-8 -*-
from CommentSet import CommentSet
import tkinter as tk
import hashlib
import time


class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.LOG_LINE_NUM = 0
        self.LOG_LINE_MAX = 7
        self.headshot = 9
        self.startn = 1


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("ADNMB跑团计点工具")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = tk.Label(self.init_window_name, text="将回复文本粘贴在此处")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = tk.Label(self.init_window_name, text="计点结果(可向下滚动)")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = tk.Label(self.init_window_name, text="状态日志")
        self.log_label.grid(row=12, column=0)
        #文本框
        self.init_data_Text = tk.Text(self.init_window_name, width=67, height=35)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = tk.Text(self.init_window_name, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = tk.Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        #按钮
        self.count_button = tk.Button(self.init_window_name, text="点击开始计点", bg="lightblue", width=10,command=self.count_it)  # 调用内部方法  加()为直接调用
        self.count_button.grid(row=1, column=11)


    #功能函数
    def count_it(self):
        src = self.init_data_Text.get(1.0,tk.END) ###
        #print("src =",src)
        if src:
            try:
                cs = CommentSet(src)
                report_txt = cs.count_point(headshot=self.headshot,startn=self.startn,silent=True)

                self.result_data_Text.delete(1.0,tk.END)
                self.result_data_Text.insert(1.0,report_txt)
                self.write_log_to_Text("计点成功")
            except:
                self.result_data_Text.delete(1.0,tk.END)
                self.result_data_Text.insert(1.0,"计点异常")
                self.write_log_to_Text("计点失败")
        else:
            self.write_log_to_Text("获取文本时出错")



    #日志动态打印
    def write_log_to_Text(self,logmsg):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"
        if self.LOG_LINE_NUM <= self.LOG_LINE_MAX:
            self.log_data_Text.insert(tk.END, logmsg_in)
            self.LOG_LINE_NUM = self.LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(tk.END, logmsg_in)


def gui_start():
    init_window = tk.Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

if __name__=="__main__":
    gui_start()


