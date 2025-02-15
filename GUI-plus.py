import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from PIL import Image, ImageTk
import pytesseract
import os
import time

# 配置Pytesseract路径（根据实际情况调整）
pytesseract.pytesseract.tesseract_ocr_cmd = r'.\static\Tesseract-OCR\tesseract.exe'  # Windows示例路径

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR识别工具")
        
        # 初始化变量
        self.image_path = None
        
        # 创建组件
        self.text_box = tk.Text(self.root, height=5, width=30)
        self.text_box.pack()
        
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack()
        
        self.load_button = ttk.Button(
            self.button_frame,
            text="选择图片",
            command=self.load_image
        )
        self.load_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.ocr_button = ttk.Button(
            self.button_frame,
            text="开始识别",
            command=self.start_ocr
        )
        self.ocr_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.clear_button = ttk.Button(
            self.button_frame,
            text="清除结果",
            command=self.clear_text
        )
        self.clear_button.grid(row=0, column=2, padx=5, pady=5)
        
    def load_image(self):
        """选择图片文件"""
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            # 显示加载成功的提示
            self.text_box. delete(1.0, tk.END)
            self.text_box.insert(tk.INSERT, f"已选择图片：{os.path.basename(file_path)}")
    
    def start_ocr(self):
        """开始OCR识别"""
        if not self.image_path:
            messagebox.showwarning("提示", "请先选择一张图片！")
            return
        
        # 更新文本框内容
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.INSERT, "正在识别中，请稍候...")
        
        # 启动OCR线程
        thread = threading.Thread(target=self.perform_ocr)
        thread.start()
    
    def perform_ocr(self):
        """执行OCR识别"""
        try:
            start_time = time.time()
            
            # 加载图像并预处理（这里可以根据需要添加更多预处理步骤）
            image = Image.open(self.image_path).convert('L')  # 转换为灰度图
            
            # 使用pytesseract进行OCR
            text = pytesseract.pytesseract.image_to_string(image,config='--psm 3 --oem 1 -c preserve_interword_spaces=1',lang='chi_sim+chi_tra+eng')
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            self.root.after(0, self.display_result, text, processing_time)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"OCR识别失败：{str(e)}"))
    
    def display_result(self, text, processing_time):
        """显示识别结果和处理时间"""
        if not text.strip():
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.INSERT, "未检测到可识别的文本。")
        else:
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.INSERT, text)
            # 添加处理时间
            self.text_box.insert(
                tk.INSERT,
                f"\n\n{'-'*20}\n处理时间为：{processing_time:.2f} 秒"
            )
    
    def clear_text(self):
        """清除文本框内容"""
        self.text_box.delete(1.0, tk.END)
        self.image_path = None

# 运行应用程序
if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()