import tkinter as tk
from tkinter import filedialog, messagebox, ttk, StringVar, Tk, Label
import cv2
import pytesseract
import os
import time
from datetime import datetime
import json
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from pytesseract import Output
import threading
import tkinter.messagebox as msgbox
import webbrowser

VERSION = "0.0.1"

pytesseract.pytesseract.tesseract_cmd = r".\static\Tesseract-OCR\tesseract.exe"

# 初始化GUI组件和状态变量
check = Tk()
check.title(f"识别图片文字程序 正在初始化 By HJWZH 版本:{VERSION}")

progress = ttk.Progressbar(check, orient='horizontal', length=500, mode='determinate')
progress.pack(pady=20)

status_var = StringVar()
status_label = Label(check, textvariable=status_var)
status_label.pack()

current_step = 0
total_steps = 5

def update_status(message):
    global status_var
    status_var.set(message)
    check.update()

def check_and_create():
    global current_step
    try:
        time.sleep(0.5)  # 模拟操作耗时
        # 步骤 1: 检查并创建 static 文件夹
        if not os.path.exists('static'):
            os.makedirs('static')
            current_step += 1
            progress['value'] = (current_step / total_steps) * 100
            update_status("已创建 static 文件夹")
        else:
            current_step += 1
            progress['value'] = (current_step / total_steps) * 100
            update_status("static 文件夹已存在")
        
        time.sleep(0.5)  # 模拟操作耗时
        # 步骤 2: 进入 static 文件夹
        os.chdir('static')
        current_step += 1
        progress['value'] = (current_step / total_steps) * 100
        update_status("已进入 static 文件夹")
        
        time.sleep(0.5)  # 模拟操作耗时
        # 步骤 3: 检查并创建 result 文件夹及 history.json
        if not os.path.exists('results'):
            os.makedirs('results')
            update_status("创建 results 文件夹")
            with open('results/history.json', 'w') as f:
                pass  # 创建空文件
            current_step += 1
            progress['value'] = (current_step / total_steps) * 100
        else:
            if not os.path.exists('results/history.json'):
                with open('results/history.json', 'w') as f:
                    pass  # 创建空文件
                update_status("创建 results 文件夹中的 history. json")
            else:
                current_step += 1
                progress['value'] = (current_step / total_steps) * 100
                update_status("results 文件夹和 history.json 已存在")
        
        time.sleep(0.5)  # 模拟操作耗时
        # 步骤 4: 检查并创建 Tesseract_OCR 文件夹
        if not os.path.exists('Tesseract-OCR'):
            os.makedirs('Tesseract-OCR')
            current_step += 1
            progress['value'] = (current_step / total_steps) * 100
            update_status("已创建 Tesseract-OCR 文件夹")
        else:
            current_step += 1
            progress['value'] = (current_step / total_steps) * 100
            update_status("Tesseract-OCR 文件夹已存在")
        
        time.sleep(0.5)  # 模拟操作耗时
        current_step += 1
        progress['value'] = (current_step / total_steps) * 100
        update_status("启动中……")

    
        time.sleep(0.5)  # 模拟操作耗时
        check.destroy()
    except Exception as e:
        msgbox.showerror("错误", f"程序初始化失败: {e}，请不要关闭进度条窗口！")
        return 0

# 程序启动后直接执行检查和创建操作
if check_and_create() == 0:
    exit()

check.mainloop()


class ImageToTextApp:
    def __init__(self, root):
        self.root = root
        self.image_path = None
        self.text_box = None
        self.result_label = None
        self.create_widgets()
        self.history_records = []

    def create_widgets(self):
        # 程序描述
        self.result_label = tk.Label(self.root,text=f"图片文字识别程序(ImageToText)\n作者：HJWZH\n版本号：{VERSION}\n目前仅支持中英文及数字识别\nBUG、建议反馈:https://github.com/HJWZH/ImageToText/issues或联系3437559454@qq.com")
        self.result_label.pack(padx=5, pady=5)

        # 创建按钮框架并将所有按钮放在同一行
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # 选择图片按钮
        select_btn = tk.Button(button_frame, text="选择图片", command=self.select_image)
        select_btn.grid(row=0, column=0, padx=2)

        # 开始识别按钮
        recognize_btn = tk.Button(button_frame, text="开始识别", command=self.recognize_text)
        recognize_btn.grid(row=0, column=1, padx=2)

        # 清除结果按钮
        clear_btn = tk.Button(button_frame, text="清除结果", command=self.clear_result)
        clear_btn.grid(row=0, column=2, padx=2)

        # 历史记录查询按钮
        history_btn = tk.Button(button_frame, text="查看历史记录", command=self.show_history)
        history_btn.grid(row=0, column=3, padx=2)

        # 开源及意见、BUG反馈按钮
        history_btn = tk.Button(button_frame, text="开源及意见、BUG反馈", command=self.BUGs)
        history_btn.grid(row=0, column=3, padx=2)

        # 显示文字的文本框，随窗口变化而变化大小
        self.text_box = tk.Text(self.root, wrap=tk.WORD)
        self.text_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

        # 配置根窗口以允许调整大小
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def BUGs(self):
        """显示BUG反馈窗口"""
        webbrowser.open("https://github.com/HJWZH/ImageToText/issues")

    def select_image(self):
        global file_path
        file_path = filedialog.askopenfilename(title="选择图片", filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            self.image_path = file_path
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, f"已选择文件：{file_path}")

    def clear_result(self):
        self.text_box.delete(1.0, tk.END)
        self.result_label.config(image=None)

    def recognize_text(self):
        global file_path

        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, f"已选择文件：{file_path}\n正在识别文字，请稍候...\n请不要关闭窗口！")

        if not self.image_path:
            messagebox.showwarning("警告", "请先选择图片！")
            return
        
        #try:
        #if 1==1:
        start_time = time.time()
        
        # 识别文字并获取位置信息
        image = cv2.imread(file_path)
        if image is None:
            #print("错误!无法读取图像，请检查文件名称和路径(不能含有中文字符)和文件格式是否正确")
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, f"已选择文件：{file_path}\n出现错误！无法读取图像，请检查文件名称和路径(不能含有中文字符)和文件格式是否正确")
            msgbox.showerror("错误", "无法读取图像，请检查文件名称和路径(不能含有中文字符)和文件格式是否正确")
            return "程序错误退出!"
        #gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 将OpenCV图像转换为Pillow图像
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)

        # 使用pytesseract进行OCR并获取位置信息
        data = pytesseract.image_to_data(image, output_type=Output.DICT,config='--psm 3 --oem 1 -c preserve_interword_spaces=1',lang='chi_sim+chi_tra+eng')# 高精度识别
        #print(data['text'])
        texts = pytesseract.image_to_string(image, output_type=Output.DICT,config='--psm 3 --oem 1 -c preserve_interword_spaces=1',lang='chi_sim+chi_tra+eng')
        #print(data)

        # 计算处理时间
        end_time = time.time()
        processing_time = end_time - start_time

        text = data['text']
        if  text == []:
            messagebox.showinfo("提示", "未检测到可识别的文本。")
            return

        # 在图片中标注文字位置
        annotated_image = self.draw_boxes_on_image(image, data,draw,pil_image)
        
        result_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # 保存标注后的图片和结果信息
        save_path = os.path.join('./static/results', f'result_{result_time}.png')
        cv2.imwrite(save_path, annotated_image)

        # 创建JSON记录
        record = {
            "timestamp": result_time,
            "text": texts['text'],
            "image_path": save_path,
            "processing_time": processing_time
        }
        
        self.history_records.append(record)
        self.save_history_to_json(result_time)

        # 更新显示
        self.update_display(annotated_image, texts, processing_time)

        """except Exception as e:
            messagebox.showerror("错误", f"OCR识别失败: {e}")
            print(e)"""

    def draw_boxes_on_image(self, image, d,draw,pil_image):
        """在图片中标注文字位置"""
        font_path = r'.\static\simsun.ttc'  # 确保路径正确
        #font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 12         # 字体大小
        font = ImageFont.truetype(font_path, font_size)
        n_boxes = len(d['level'])
        for i in range(n_boxes):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            text = d['text'][i]
            if text.strip():
                # 在图像上绘制矩形框和文字
                #image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                draw.rectangle((x, y, x + w, y + h), outline=(0, 255, 0), width=1)
                #image = cv2.putText(image, text, (x, y - 10), font, 0.5, (0, 255, 0), 2)
                draw.text((x, y - 10),text,(0, 255, 0),font=font,thickness=5)
        
            # 将Pillow图像转换回OpenCV格式
        image_with_text = np.array(pil_image)
        """# 显示结果图像
            cv2.imshow('Image with Text', image_with_text)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return image"""
        return image_with_text

    def update_display(self, annotated_image, texts, processing_time):
        """更新显示内容"""
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, f"识别结果：\n{texts['text']}\n\n{"-"*20}\n处理时间：{processing_time:.2f}秒")

        # 将标注后的图片显示在GUI中
        """image_for_display = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        if annotated_image is not None:
            self.result_label.image = cv2.resize(image_for_display, (400, 300))
            self.result_label.config(image=self.result_label.image)"""
        # 显示结果图像
        #showimage('Image with Text',annotated_image)
        threading.Thread(target=showimage,args=('Image with Text',annotated_image)).start()

    def save_history_to_json(self,result_time):
        """将历史记录保存到JSON文件"""
        with open(f'static/results/result_{result_time}.json', 'w',encoding='UTF-8') as f:
            json.dump(self.history_records, f, indent=2, ensure_ascii=False)

    def show_history(self):
        """显示历史记录窗口"""
        """history_window = tk.Toplevel()
        history_window.title("历史记录")
        
        treeview = ttk.Treeview(history_window)
        treeview.pack(pady=10)
        
        # 创建列
        columns = ('时间', '处理时间（秒）')
        treeview.config(columns=columns, show='headings')
        
        for col in columns:
            treeview.heading(col, text=col)

        # 读取历史记录
        with open('static/results/history.json') as f:
            history = json.load(f)
        
        # 插入数据
        for record in history:
            treeview.insert('', 'end', values=(record['timestamp'], round(record['processing_time'], 2)))

        # 添加滚动条
        scrollbar = ttk.Scrollbar(history_window, command=treeview.yview)
        scrollbar.pack(side='right', fill='y')
        treeview.configure(yscrollcommand=scrollbar.set)"""
        # 打开历史记录文件夹
        os.system('start explorer static\\results')

def showimage(title,img):
    """cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""
    #print(img)
    """# 将 BGR 转换为 RGB
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 创建图形并显示图像
    plt.figure(figsize=(10, 6))
    plt.imshow(rgb_image)
    plt.title('Interactive Image Display')
    plt.axis('off')  # 关闭坐标轴

    # 显示图形，启用工具栏
    plt.show()"""
    # 创建可调整大小的窗口
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    # 显示图像
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 创建主窗口
root = tk.Tk()
app = ImageToTextApp(root)
root.title(f"图片文字识别程序 By HJWZH 版本:{VERSION}")
os.chdir('..')
root.mainloop()