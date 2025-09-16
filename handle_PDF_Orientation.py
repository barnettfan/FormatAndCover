from PIL import Image 
import os 
from PyPDF2 import PdfWriter  
import io 
import re

def images_to_pdf(output_pdf_path, image_paths, target_width=1920):
    """
    将多张图片合并为一个PDF文件 
    
    参数:
        output_pdf_path: 输出的PDF文件路径 
        image_paths: 图片路径列表 
        target_width: 目标宽度（默认800像素）
    """
    images = []
    for image_path in image_paths:
        img = Image.open(image_path) 
        
        # 计算调整后的高度（保持宽高比）
        width_percent = (target_width / float(img.size[0])) 
        target_height = int(float(img.size[1])  * width_percent)
        
        # 调整图片尺寸（保持比例）
        img_resized = img.resize((target_width,  target_height), Image.LANCZOS)

        if img_resized.mode  == 'RGBA':
            img_resized = img.convert('RGB') 
        images.append(img_resized) 
    
    if images:
        images[0].save(
            output_pdf_path, 
            save_all=True, 
            append_images=images[1:],
            resolution=600.0 
        )
    print(f"PDF已保存至: {output_pdf_path}")

def images_to_lossless_pdf(output_pdf_path, image_paths, target_width=1080):
    writer = PdfWriter()
    
    for image_path in image_paths:
        img = Image.open(image_path) 
        
        # 计算调整后的高度（保持宽高比）
        width_percent = (target_width / float(img.size[0])) 
        target_height = int(float(img.size[1])  * width_percent)
        
        # 调整图片尺寸（保持比例）
        img_resized = img.resize((target_width,  target_height), Image.LANCZOS)
        
        # 将图片转换为PDF页面（无压缩）
        img_byte_arr = io.BytesIO()
        img_resized.save(img_byte_arr,  format='PDF', quality=100)
        
        # 添加到PDF writer 
        img_byte_arr.seek(0) 
        writer.append(img_byte_arr) 
    
    # 保存最终PDF 
    with open(output_pdf_path, 'wb') as f:
        writer.write(f) 

def natural_sort_key(s):
    """
    提取字符串中的数字部分作为排序键。
    :param s: 字符串
    :return: 排序键
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def images_to_pdf_ui(base_dir, ):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
    for item in os.listdir(base_dir):
        path = os.path.join(base_dir, item)
        os.path.isdir(path + item_1)

        # 判断文件
        if not os.path.isdir(path):
            print('{0} 不是文件夹，跳过'.format(path))
            continue

        
        


if __name__ == '__main__':
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
    base_dir = f"Z:\\BaiduNetdiskDownload\\西西10\\"  # 当前目录
    for item in os.listdir(base_dir):
        path = os.path.join(base_dir, item) + '\\'
        list = os.listdir(path) 
        image_paths = []
        for item_1 in list:
            if os.path.isdir(path + item_1):
                path_1 = os.path.join(path, item_1) + '\\'
                list_1 = os.listdir(path_1) 
                for item_2 in list_1:
                    if os.path.splitext(item_2)[1].lower()  in image_extensions:
                        image_paths.append(path_1 + item_2)
            else:
                image_paths = [path + f for f in os.listdir(path)  if os.path.splitext(f)[1].lower()  in image_extensions]
                # 按文件名排序 
                # image_paths.sort()
                image_paths = sorted(image_paths, key=natural_sort_key)
        
        
        output_pdf = base_dir + item + ".pdf"  # 输出的 PDF 文件名
        images_to_pdf(output_pdf, image_paths)