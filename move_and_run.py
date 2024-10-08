import shutil
import subprocess
import os
from PIL import Image

# 移动素颜分割png
def move_and_run():
    source_file_nomakeup_parsed = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\res\\test_res\\nomakeup.png"
    destination_folder_nomakeup_parsed = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\test\\seg1\\non-makeup"
    destination_file_nomakeup_parsed = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\test\\seg1\\non-makeup\\nomakeup.png"
    # 确保目标目录存在
    os.makedirs(destination_folder_nomakeup_parsed, exist_ok=True)
    # 移动文件
    shutil.move(source_file_nomakeup_parsed, destination_file_nomakeup_parsed)


    # 移动妆容分割png
    # 定义文件路径
    source_file_makeup_parsed = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\res\\test_res\\makeup.png"
    destination_folder_makeup_parsed = 'D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\test\\seg1\\makeup'
    destination_file_makeup_parsed = 'D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\test\\seg1\\makeup\\makeup.png'
    # 确保目标目录存在
    os.makedirs(destination_folder_makeup_parsed, exist_ok=True)
    # 移动文件
    shutil.move(source_file_makeup_parsed, destination_file_makeup_parsed)

    # 将素颜原图转为png格式并移动
    source_path_nomakeup = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\data\\nomakeup.jpg"
    destination_path_nomakeup = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\data\\nomakeup.png"
    with Image.open(source_path_nomakeup) as img:
        img.save(destination_path_nomakeup, 'PNG')

    source_file_nomakeup = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\data\\nomakeup.png"
    destination_folder_nomakeup = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\test\\images\\non-makeup"
    destination_file_nomakeup = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\test\\images\\non-makeup\\nomakeup.png"
    # 确保目标目录存在
    os.makedirs(destination_folder_nomakeup, exist_ok=True)
    # 移动文件
    shutil.move(source_file_nomakeup, destination_file_nomakeup)

    # 将妆容照片转为png格式并移动
    source_path_makeup = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\data\\makeup.jpg"
    destination_path_makeup ="D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\data\\makeup.png"
    with Image.open(source_path_makeup) as img:
        img.save(destination_path_makeup, 'PNG')

    source_file_makeup = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\data\\makeup.png"
    destination_folder_makeup = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\test\\images\\makeup"
    destination_file_makeup = "D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\test\\images\\makeup\\makeup.png"
    # 确保目标目录存在
    os.makedirs(destination_folder_makeup, exist_ok=True)
    # 移动文件
    shutil.move(source_file_makeup, destination_file_makeup)

if __name__ == "__main__":
    move_and_run()