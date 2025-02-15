import cv2
import pytesseract
from pytesseract import Output
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import tkinter.filedialog
# 设置tesseract可执行文件的路径
pytesseract.pytesseract.tesseract_cmd = r'.\static\Tesseract-OCR\tesseract.exe'

def extract_text_and_draw_boxes(image_path,font_path):
    # 加载中文字体文件
    #font_path = r'C:\Users\Administrator\Desktop\屏幕识别\simsun.ttc'  # 确保路径正确
    #font = cv2.FONT_HERSHEY_SIMPLEX

    font_size = 12         # 字体大小
    font = ImageFont.truetype(font_path, font_size)
    #font = ImageFont.truetype(font_path)

    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("错误！无法读取图像，请检查文件名称和路径(不能含有中文字符)和文件格式是否正确")
        return "程序错误退出！"
    
    # 将OpenCV图像转换为Pillow图像
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    # 使用pytesseract提取文字和位置信息
    d = pytesseract.image_to_data(image, output_type=Output.DICT,config='--psm 3 --oem 1 -c preserve_interword_spaces=1',lang='chi_sim+chi_tra+eng')
    
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
    # 显示结果图像
    cv2.imshow('Image with Text', image_with_text)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(d)
    for i in d['text']:
        print(i,end='')

# 示例使用
image_path = tkinter.filedialog.askopenfilename(filetypes=[("图片文件","*.png;*.jpg;*.jpeg"),("所有文件","*.*")])  # 打开文件选择对话框
#image_path = r"C:\Users\Administrator\Desktop\test.png"  # 替换为你的图片路径
# 将文件路径从默认编码转换为UTF-8编码
#print(image_path)
#image_path = input()
if image_path == "":
    print("未选择文件！")
    exit()
#print(image_path)
result = extract_text_and_draw_boxes(image_path,r'simsun.ttc')
#print(result)