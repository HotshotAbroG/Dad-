import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import cv2
from tkinter import Menu
from tkinter import filedialog
from tkinter import END  # 引入END 以便清空
from PIL import Image
import numpy as np

# DST/
global One_name
global Path_names
global command
global destination
global Copy_list
global Rotation_list
global Translat_list
from matplotlib import pyplot as plt

Translat_list = [1, 2]
Rotation_list = [0, 1]
Copy_list = [0, 1, 2, 3, 4, 5]
destination = ''
command = 0
Path_names = []
One_name = ''

def Image_Splice(Original_img, col_max, row_max, weight_i, height_i):
    # 实现图片拼接
    # 输入: 原图片，几列，几行，每张图片压缩宽，每张图片压缩高
    # 返回： 拼接好的完图
    print('Splice start')
    print("col_max: ", col_max)
    print("row_max: ", row_max)
    num = 0
    pic_max = col_max * row_max
    # 创建空白画板，（背景）
    toImage = Image.new("RGBA", (weight_i * col_max, height_i * row_max))
    # 内循环为行，外循环为列，
    # 先行后列的出图
    for i in range(0, col_max):
        for j in range(0, row_max):
            temp_image = Image.open(Original_img[num])

            # 图像压缩 双线性插值
            Zip_picture = temp_image.resize((weight_i, height_i))

            # 确定位置， i%10 = 第几张*所占行像素
            loc = (int(i * weight_i), int(j * height_i))
            # 若为 4列2行 （0,0）、(0,300)、(300,0)、(300,300)
            toImage.paste(Zip_picture, loc)
            num += 1
            if num >= len(Original_img):
                print("Outing the Fucking")
                break

        if num >= pic_max:
            break
    print("OK")
    return toImage


def Image_translate(src_name, delta_x, delta_y):
    # 图像平移函数
    # 输入：源图像，delta_x,delta_y
    # 输出：平移后的图像
    src = cv2.imread(src_name)
    row, col, channel = src.shape
    # print("row: %s columns: %s" % (row, col))
    Transform_Matrix = np.float32([[1, 0, delta_x], [0, 1, delta_y]])
    # 仿射变换
    # 注意仿射变换的输入shape是（列，行）
    # 而普通读取的是（行，列）
    shifted = cv2.warpAffine(src, Transform_Matrix,
                             (col, row))
    return shifted


def Copy_Move(src_name, x0, y0, x1, y1, dst_x, dst_y):
    # 图像复制-粘贴
    # 输入：目标图像的名字,感兴趣目标区域，目的区域
    # 输出：复制完的图像
    #  ！！！！！！必须用 PIL Image 来打开
    src = Image.open(src_name)
    width, height = src.size
    dst = src.copy()
    # print("columns: %s,rows: %s" % (width, height))
    temp_image = src.crop((x0, y0, x1, y1))
    dst.paste(temp_image, (dst_x, dst_y))
    return dst


def Rotation(name, size, angle):
    """
    Get_rotat_img
    输入值： 图片name，结果存储name，缩放比例，旋转角度
    返回值： 128旋转图、128原始图、128原始灰度图
    """
    img = cv2.imread(name,0)
    # rows, cols = img.shape[:2]
    # img1 = cv2.resize(img, (256, 256), cv2.INTER_LINEAR)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, cols = img.shape
    M = cv2.getRotationMatrix2D((rows / 2, cols / 2), angle, size)  # 旋转重心、角度、缩放因子

    dst = cv2.warpAffine(img, M, (cols, rows))  # 需要图像、变换矩阵、变换后的大小
    return dst


# 我现在想实现的目标：
# 1、 按健读取文件，并且再下面的text栏显示

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


# ==激活函数=============================================================
# ===================================================================
def createToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


# 读取多个文件
def read_files1():
    global Path_names
    global command
    command = 1
    Path_names = filedialog.askopenfilenames()

    for i in Path_names:
        scr.insert(tk.INSERT, i + '\n')
    scr.insert(tk.INSERT, 'Read Finished\nParameter Set\n')


# 读取多个文件
def read_files3():
    # win.withdraw()
    global command
    global Path_names
    command = 3
    Path_names = filedialog.askopenfilenames()
    for i in Path_names:
        scr.insert(tk.INSERT, i + '\n')
    scr.insert(tk.INSERT, 'Read Finished\nParameter Set\n')


# 读取多个文件
def read_files():
    global Path_names
    global command
    command = 4
    Path_names = filedialog.askopenfilenames()
    # print(type(file_path))
    for i in Path_names:
        scr.insert(tk.INSERT, i + '\n')
    scr.insert(tk.INSERT, 'Read Finished\nParameter Set\n')


# 读取多个文件2
def read_files2():
    global Path_names
    global command
    command = 2
    # del Path_names[:]
    Path_names = filedialog.askopenfilenames()
    # print(type(file_path))
    for i in Path_names:
        scr.insert(tk.INSERT, i + '\n')
    scr.insert(tk.INSERT, 'Read Finished\nParameter Set\n')


def ClearAll():
    # action.configure(text='Hello\n ' + name.get())
    # action.configure(state='disabled')    # Di\
    global command
    scr.delete(1.0, END)  # 使用 delete
    command = 0
    print("OK")


def Image_TRANSLATE(src_names, dst):
    """
    # 输入：操作图像的源地址名称
    # 输出: 无
    # 功能: 地址中的图像读取，平移，后存储
    """
    global Translat_list
    j = dst
    print(Translat_list)
    print("Translate Start")
    for i in src_names:
        # 截取所有图片的名字 方便处理完毕后，存储
        wanted_name = i.split('/')[-1]
        # 得到完整存储路径
        dst_path = j + wanted_name
        # 图像平移
        dst = Image_translate(i, int(Translat_list[0]), int(Translat_list[1]))
        cv2.imwrite(dst_path, dst)
    print("Translate Finish")


def Image_ROTATION(src_names, dst):
    """
    # 输入：操作图像的源地址名称，缩放尺寸，旋转角度
    # 输出: 无
    # 功能: 地址中的图像读取，旋转，后存储
    """
    global Rotation_list
    j = dst
    print('Rotation Start')
    for i in src_names:
        # 截取所有图片的名字 方便处理完毕后，存储
        wanted_name = i.split('/')[-1]
        # 得到完整存储路径
        # dst_path = 'DST/' + wanted_name
        dst_path = j + wanted_name
        # 图像旋转
        dst = Rotation(i, float(Rotation_list[0]), float(Rotation_list[1]))
        cv2.imwrite(dst_path, dst)
    print('Rotation Finish')


def Image_Copy_Move(src_names, dst):
    """
    # 输入：操作图像的源地址名称，缩放尺寸，旋转角度
    # 输出: 无
    # 功能: 地址中的图像读取，旋转，后存储
    """
    # DST/
    global Copy_list
    print('Copy_Move Start')
    j = dst
    print(Copy_list)
    for i in src_names:
        # 截取所有图片的名字 方便处理完毕后，存储
        wanted_name = i.split('/')[-1]
        # 得到完整存储路径
        # wanted_name = str(wanted_name)
        dst_path = j + wanted_name
        # print(dst_path)
        # 图像COPY MOVE
        # 得到处理后的图片
        dst = Copy_Move(i, int(Copy_list[0]), int(Copy_list[1]),
                        int(Copy_list[2]), int(Copy_list[3]),
                        int(Copy_list[4]), int(Copy_list[5]))
        dst.save(dst_path)
    print('Copy_Move Finish')


def Image_SPLICE(src_names):
    """
    # 输入：操作图像的源地址名称
    # 输出: 无
    # 功能: 地址中的图像读取,拼接，后存储
    """
    # 计算图片数量
    Image_number = len(src_names)  # int 类型
    # 自动优化行列
    # first 判断是否为方阵
    temp = int(np.sqrt(Image_number))
    result = temp * temp
    if result is Image_number:
        row, col = temp, temp
    elif Image_number % 2 != 0:
        temptation = Image_number + 1
        row = int(temptation / 2)
        col = 2
    else:
        row = int(Image_number / 2)
        col = 2
    dst_path = 'DST/dst.png'
    dst = Image_Splice(src_names, col, row, 300, 300)
    dst.save(dst_path)
    plt.subplot(111), plt.imshow(dst)
    plt.show()
    print('Splice Finish')


def execute():
    # 1：旋转
    # 2：平移
    # 3：复制
    # 4：拼接
    global One_name
    global Path_names
    global destination
    print(type(destination))
    if command == 1:
        scr.insert(tk.INSERT, 'Mission Start\n')
        Image_ROTATION(Path_names, destination)
        scr.insert(tk.INSERT, 'Mission Finished\n')
    elif command == 2:
        scr.insert(tk.INSERT, 'Mission Start\n')
        Image_TRANSLATE(Path_names, destination)
        scr.insert(tk.INSERT, 'Mission Finished\n')
    elif command == 3:
        scr.insert(tk.INSERT, 'Mission Start\n')
        Image_Copy_Move(Path_names, destination)
        scr.insert(tk.INSERT, 'Mission Finished\n')
    elif command == 4:
        scr.insert(tk.INSERT, 'Mission Start\n')
        Image_SPLICE(Path_names)
        scr.insert(tk.INSERT, 'Mission Finished\n')


def New_window():
    if command == 1:
        window1()
        print("111OK")
    elif command == 2:
        window2()
        print("222OK")
    elif command == 3:
        window3()


def window1():
    top = tk.Toplevel()
    top.title('Python')
    tk.Label(top, text="缩放因数：").grid(row=1, column=0, padx=1, pady=1)
    tk.Label(top, text="旋转角度：").grid(row=2, column=0, padx=1, pady=1)

    v1 = tk.StringVar()
    e1 = tk.Entry(top, textvariable=v1, width=10)
    e1.grid(row=1, column=1, padx=1, pady=1)

    def show():
        global destination
        global Rotation_list
        destination = e7.get()

        Rotation_list[0] = e1.get()
        Rotation_list[1] = e2.get()
        print("SCA:%s, Rota:%s" % (Rotation_list[0], Rotation_list[1]))

        print("Dst save: ", destination)

    v2 = tk.StringVar()
    e2 = tk.Entry(top, textvariable=v2, width=10)
    e2.grid(row=2, column=1, padx=1, pady=1)

    tk.Label(top, text="存储地点").grid(row=3, column=0, padx=1, pady=1)
    v7 = tk.StringVar()
    e7 = tk.Entry(top, textvariable=v7, width=10)
    e7.grid(row=3, column=1, padx=1, pady=1)

    tk.Button(top, text="确定", width=7, command=show).grid(row=4, column=0, padx=1, pady=1)


def window2():
    top = tk.Toplevel()
    top.title('Python')
    tk.Label(top, text="水平平移：").grid(row=1, column=0, padx=1, pady=1)
    tk.Label(top, text="垂直平移：").grid(row=2, column=0, padx=1, pady=1)

    v1 = tk.StringVar()
    e1 = tk.Entry(top, textvariable=v1, width=10)
    e1.grid(row=1, column=1, padx=1, pady=1)

    def show():
        global destination
        global Translat_list
        destination = e7.get()

        Translat_list[0] = e1.get()
        Translat_list[1] = e2.get()
        print("DELTA_X:%s, DELTA_Y:%s" % (Translat_list[0], Translat_list[1]))

        print("Dst save: ", destination)

    v2 = tk.StringVar()
    e2 = tk.Entry(top, textvariable=v2, width=10)
    e2.grid(row=2, column=1, padx=1, pady=1)

    tk.Label(top, text="存储地点").grid(row=3, column=0, padx=1, pady=1)
    v7 = tk.StringVar()
    e7 = tk.Entry(top, textvariable=v7, width=10)
    e7.grid(row=3, column=1, padx=1, pady=1)

    tk.Button(top, text="确定", width=7, command=show).grid(row=4, column=0, padx=1, pady=1)


def window3():
    top = tk.Toplevel()
    top.title('Python')
    tk.Label(top, text="起始坐标x0：").grid(row=1, column=0, padx=1, pady=1)
    tk.Label(top, text="起始坐标y0：").grid(row=2, column=0, padx=1, pady=1)
    tk.Label(top, text="起始坐标x1：").grid(row=3, column=0, padx=1, pady=1)
    tk.Label(top, text="起始坐标y1：").grid(row=4, column=0, padx=1, pady=1)
    tk.Label(top, text="目的坐标x2：").grid(row=5, column=0, padx=1, pady=1)
    tk.Label(top, text="目的坐标y2：").grid(row=6, column=0, padx=1, pady=1)

    v1 = tk.StringVar()
    e1 = tk.Entry(top, textvariable=v1, width=10)
    e1.grid(row=1, column=1, padx=1, pady=1)

    def show():
        global destination
        global Copy_list

        Copy_list[0] = e1.get()
        Copy_list[1] = e2.get()
        Copy_list[2] = e3.get()
        Copy_list[3] = e4.get()
        Copy_list[4] = e5.get()
        Copy_list[5] = e6.get()
        destination = e7.get()
        print("SRC location:(%s,%s)---(%s,%s)" % (Copy_list[0], Copy_list[1], Copy_list[2], Copy_list[3]))
        print("DST location: (%s,%s" % (Copy_list[4], Copy_list[5]))
        print("Dst save: ", destination)

    v2 = tk.StringVar()
    e2 = tk.Entry(top, textvariable=v2, width=10)
    e2.grid(row=2, column=1, padx=1, pady=1)

    v3 = tk.StringVar()
    e3 = tk.Entry(top, textvariable=v3, width=10)
    e3.grid(row=3, column=1, padx=1, pady=1)

    v4 = tk.StringVar()
    e4 = tk.Entry(top, textvariable=v4, width=10)
    e4.grid(row=4, column=1, padx=1, pady=1)

    v5 = tk.StringVar()
    e5 = tk.Entry(top, textvariable=v5, width=10)
    e5.grid(row=5, column=1, padx=1, pady=1)

    v6 = tk.StringVar()
    e6 = tk.Entry(top, textvariable=v6, width=10)
    e6.grid(row=6, column=1, padx=1, pady=1)

    tk.Label(top, text="存储地点").grid(row=7, column=0, padx=1, pady=1)
    v7 = tk.StringVar()
    e7 = tk.Entry(top, textvariable=v7, width=10)
    e7.grid(row=7, column=1, padx=1, pady=1)

    tk.Button(top, text="确定", width=7, command=show).grid(row=8, column=0, padx=1, pady=1)


# ===================================================================

win = tk.Tk()
# Add a title
win.title("图形处理用户界面")

# win.resizable(0,0)
# Tab Control introduced here --------------------------------------
tabControl = ttk.Notebook(win)  # Create Tab Control

tab1 = ttk.Frame(tabControl)  # Create a tab
tabControl.add(tab1, text='第一页')  # Add the tab

tabControl.pack(expand=1, fill="both")  # Pack to make visible
# ~ Tab Control introduced here -----------------------------------------
# ---------------Tab1控件介绍------------------#
# We are creating a container tab3 to hold all other widgets
monty = ttk.LabelFrame(tab1, text='Main Surface')
monty.grid(column=1, row=1, padx=8, pady=4)

# Changing our Label
ttk.Label(monty, text="功能栏:").grid(column=0, row=0, sticky='W')
# 第一个按钮
action = ttk.Button(monty, text="图像旋转\nImage\nRotation", width=10, command=read_files1)
action.grid(column=0, row=1, rowspan=5, ipady=7)
# 第二个按钮
action = ttk.Button(monty, text="图像平移\nImage\nTranslate", width=10, command=read_files2)
action.grid(column=1, row=1, rowspan=5, ipady=7)
# 第三个按钮
action = ttk.Button(monty, text="图像复制\nImage\nCopy", width=10, command=read_files3)
action.grid(column=2, row=1, rowspan=5, ipady=7)
# 第四个按钮
action = ttk.Button(monty, text="图像拼接\nImage\nSplice", width=10, command=read_files)
action.grid(column=3, row=1, rowspan=5, ipady=7)
# 第五个按钮
action = ttk.Button(monty, text="清空", width=5, command=ClearAll)
action.grid(column=3, row=19, rowspan=1, ipady=1)
# 第六个按钮
action = ttk.Button(monty, text="运行", width=6, command=execute)
action.grid(column=0, row=19, rowspan=5, ipady=1)
# 第七个按钮
action = ttk.Button(monty, text="参数设置", width=7, command=New_window)
action.grid(column=1, row=19, rowspan=5, ipady=1)


def _spin2():
    lis = ('a', 'b', 'c', 'd', 'e')
    temp = []
    for i in lis:
        i = i + '\n'
        temp.append(i)
    # value = spin2.get()
    # print(value)
    # scr.insert(tk.INSERT, value + '\n')
    scr.insert(tk.INSERT, temp)


# ==============文本框构造=====================
scrolW = 30
scrolH = 5
scr = scrolledtext.ScrolledText(monty, width=scrolW, height=scrolH, wrap=tk.WORD)
scr.grid(column=0, row=15, sticky='WE', columnspan=4)

# 一次性控制各控件之间的距离139
for child in monty.winfo_children():
    child.grid_configure(padx=3, pady=1)


# =============================
# Exit GUI cleanly
def _quit():
    win.quit()
    win.destroy()
    exit()


# Creating a Menu Bar
menuBar = Menu(win)
win.config(menu=menuBar)

# Add menu items
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label="新建")
fileMenu.add_separator()
fileMenu.add_command(label="退出", command=_quit)
menuBar.add_cascade(label="文件", menu=fileMenu)

# ----------------菜单栏介绍-------------------#

# =================================
# Start GUI
# ======================

# Place cursor into name Entry

print(command)
win.mainloop()
