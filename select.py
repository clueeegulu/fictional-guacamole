import os
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, QWidget, QScrollArea, QMainWindow, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap, QIcon, QPainterPath, QPainter
from PyQt5.QtCore import Qt, QRect
import time
import threading
import shared
import time
import shutil
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal

class SelectPageWindow(QWidget):
    def __init__(self, switch_to_imitated_page_callback, switch_to_main_page_callback):
        super().__init__()
        self.switch_to_imitated_page_callback = switch_to_imitated_page_callback
        self.switch_to_main_page_callback = switch_to_main_page_callback
        self.setup_ui()



    def setup_ui(self):
        self.setWindowTitle("选择功能")
        self.setGeometry(100, 100, 648, 762)

        # 创建主布局
        self.main_layout = QHBoxLayout(self)

        # 创建顶部、中间、底部的空白间距，使距离保持一致
        spacer_top = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer_middle = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer_bottom = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # 创建顶部图片框（圆形）
        self.topmost_label = QLabel(self)
        self.topmost_label.setFixedSize(400, 400)
        self.topmost_label.setStyleSheet("border-radius: 100px; background-color: white;")
        self.topmost_label.setAlignment(Qt.AlignCenter)

        # 创建底部图片框（圆形）
        self.top_label = QLabel(self)
        self.top_label.setFixedSize(400, 400)
        self.top_label.setStyleSheet("border-radius: 100px; background-color: white;")
        self.top_label.setAlignment(Qt.AlignCenter)

        # 创建返回主页按钮
        self.button = QPushButton("返回主页", self)
        #self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button.resize(100, 100)
        self.button.clicked.connect(self.switch_to_main_page)

        # 使用布局将图片和按钮排列在中间垂直方向
        image_layout = QHBoxLayout()
        image_layout.addSpacerItem(spacer_top)  # 顶部空白距离
        image_layout.addWidget(self.topmost_label, alignment=Qt.AlignCenter)
        image_layout.addSpacerItem(spacer_middle)  # 图片与按钮之间的距离
        image_layout.addWidget(self.button, alignment=Qt.AlignCenter)
        image_layout.addSpacerItem(spacer_middle)  # 按钮与底部图片的距离
        image_layout.addWidget(self.top_label, alignment=Qt.AlignCenter)
        image_layout.addSpacerItem(spacer_bottom)  # 底部空白距离

        self.main_layout.addLayout(image_layout)

        # 加载固定图片
        self.load_fixed_images()

    def switch_to_main_page(self):
        print("返回主页")

    def load_fixed_images(self):
        # 加载第一张图片
        image_path_1 = "D:\software\PyCharm\Py_Projects\pifect_mirror\logo\imitation.jpg"
        if os.path.exists(image_path_1):
            pixmap1 = QPixmap(image_path_1).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if not pixmap1.isNull():
                self.topmost_label.setPixmap(self.get_rounded_pixmap(pixmap1))
                self.topmost_label.mousePressEvent = self.switch_to_imitated_page
            else:
                self.topmost_label.setText("图片1加载失败")
        else:
            self.topmost_label.setText("图片1加载失败")

        # 加载第二张图片
        image_path_2 = "D:\software\PyCharm\Py_Projects\pifect_mirror\logo\makeup.jpg"
        if os.path.exists(image_path_2):
            pixmap2 = QPixmap(image_path_2).scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if not pixmap2.isNull():
                self.top_label.setPixmap(self.get_rounded_pixmap(pixmap2))
            else:
                self.top_label.setText("图片2加载失败")
        else:
            self.top_label.setText("图片2加载失败")

    def get_rounded_pixmap(self, pixmap):
        """ 将图片转换为圆形 """
        size = pixmap.size()
        mask = QPixmap(size)
        mask.fill(Qt.transparent)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, size.width(), size.height())
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        return mask

    def switch_to_imitated_page(self, event):
        # 触发页面切换回调
        self.switch_to_imitated_page_callback()

    def switch_to_main_page(self,event):
        # 触发页面切换回调
        self.switch_to_main_page_callback()


class ImitatedPageWindow(QWidget):
    start_makeup_signal = pyqtSignal()
    def __init__(self, switch_to_select_page_callback, image_directory,switch_to_i_output_page_callback):
        super().__init__()
        self.image_directory = image_directory
        self.switch_to_select_page_callback = switch_to_select_page_callback
        self.switch_to_i_output_page_callback = switch_to_i_output_page_callback
        self.selected_image_path = None
        self.setup_ui()
        self.load_image_delay()

    def load_image_delay(self):
        self.load_image_button.clicked.connect(self.load_latest_image)

    def check_images_in_folder(self,folder_path):
        # 定义常见的图片扩展名0
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

        # 列出指定文件夹中的所有文件
        files_in_folder = os.listdir(folder_path)

        # 遍历文件夹中的所有文件，检查是否有图片
        for file_name in files_in_folder:
            if file_name.lower().endswith(image_extensions):
                return True  # 存在图片文件
        print('文件夹中没有照片')
        return False  # 不存在图片文件

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # 左上角的返回按钮
        back_button = self.create_button("选择其他功能", self.switch_to_select_page)
        layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # 创建间距对象，用于均匀分布组件
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # 创建水平布局用于两张图片和对应按钮的排列
        image_button_layout = QHBoxLayout()

        # 左边的图片和“点我拍摄”按钮垂直排列
        left_layout = QVBoxLayout()

        # 显示模拟页面的顶部图片
        self.imitated_label = QLabel(self)
        self.imitated_label.setFixedSize(400, 400)
        self.imitated_label.setStyleSheet("border: 2px solid black; background-color: white;")
        left_layout.addWidget(self.imitated_label, alignment=Qt.AlignCenter)

        # 创建按钮以读取最后一张图片，放在左边的图片下方
        self.load_image_button = self.create_button("点我拍摄",self.send_message_0)
        left_layout.addWidget(self.load_image_button, alignment=Qt.AlignCenter)

        # 将左边的图片和按钮布局添加到水平布局中
        image_button_layout.addLayout(left_layout)

        # 添加一个宽度为100px的间距
        spacer_between_images = QSpacerItem(100, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        image_button_layout.addItem(spacer_between_images)

        # 右边的图片和两个按钮垂直排列
        right_layout = QVBoxLayout()

        # 显示底部图片
        self.bottom_label = QLabel(self)
        self.bottom_label.setFixedSize(400, 400)
        self.bottom_label.setStyleSheet("border: 2px solid black; background-color: white;")
        right_layout.addWidget(self.bottom_label, alignment=Qt.AlignCenter)

        # 创建两个按钮并垂直排列在右边图片下方
        button_layout = QVBoxLayout()
        button_1 = self.create_button("确认妆容", self.send_message_1)
        button_2 = self.create_button("开始仿妆", self.switch_to_i_output_page)
        button_2.clicked.connect(self.start_makeup)
        button_layout.addWidget(button_1, alignment=Qt.AlignCenter)
        button_layout.addWidget(button_2, alignment=Qt.AlignCenter)
        right_layout.addLayout(button_layout)

        # 将右边的图片和按钮布局添加到水平布局中
        image_button_layout.addLayout(right_layout)

        # 创建一个 QWidget 来包含布局，然后设置居中对齐
        container_widget = QWidget()
        container_widget.setLayout(image_button_layout)

        # 将这个 QWidget 添加到主布局，并确保其居中对齐
        layout.addSpacerItem(spacer)  # 添加顶部空白间距
        layout.addWidget(container_widget, alignment=Qt.AlignCenter)  # 确保图片居中对称放置
        layout.addSpacerItem(spacer)  # 添加底部空白间距

        # 创建水平滚动区域用于显示图片选择器
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setFixedHeight(125)
        self.scroll_content = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addSpacerItem(spacer)  # 添加滚动区域上方间距
        layout.addWidget(self.scroll_area)

        # 填充滚动区域
        self.fill_item_selector(100, [
            {"name": "Item 1", "pictureURL": "D:\software\PyCharm\Py_Projects\pifect_mirror\makeup\Item 1.jpg"},
            {"name": "Item 2", "pictureURL": "D:\software\PyCharm\Py_Projects\pifect_mirror\makeup\Item 2.jpg"},
            {"name": "Item 3", "pictureURL": "D:\software\PyCharm\Py_Projects\pifect_mirror\makeup\Item 3.jpg"},
            {"name": "Item 4", "pictureURL": "D:\software\PyCharm\Py_Projects\pifect_mirror\makeup\Item 4.jpg"},
        ])

        self.setLayout(layout)

    def create_button(self, text, callback):
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        # 将高度设置为原来的两倍
        height = button.height() * 2
        width = button.width() * 2
        button.setFixedHeight(height)
        button.setFixedWidth(width)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        return button

    def load_latest_image(self):
        """ 从文件夹中读取最后一张图片 """
        #time.sleep(1)
        files = [os.path.join(self.image_directory, f) for f in os.listdir(self.image_directory) if os.path.isfile(os.path.join(self.image_directory, f))]
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        if not image_files:
            self.imitated_label.setText("没有图片")
            return

        latest_image = max(image_files, key=os.path.getmtime)
        pixmap = QPixmap(latest_image).scaled(400, 400)
        if not pixmap.isNull():
            self.imitated_label.setPixmap(pixmap)
        else:
            self.imitated_label.setText("图片0加载失败")

    def fill_item_selector(self, picture_size, items):
        for item in items:
            image_path = item["pictureURL"]
            button = QPushButton(self.scroll_content)
            button.setFixedSize(picture_size, picture_size)
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path).scaled(picture_size, picture_size)
                if not pixmap.isNull():
                    icon = QIcon(pixmap)  # 将 QPixmap 转换为 QIcon
                    button.setIcon(icon)
                    button.setIconSize(button.size())
                    button.clicked.connect(lambda _, p=image_path: self.display_selected_image(p))  # 绑定点击事件
                else:
                    button.setText("图片加载失败（空图像）")
            else:
                button.setText("图片未找到")
            self.scroll_layout.addWidget(button)

    def display_selected_image(self, image_path):
        """ 在底部标签显示选中的图片 """
        pixmap = QPixmap(image_path).scaled(400, 400)
        if not pixmap.isNull():
            self.bottom_label.setPixmap(pixmap)
            self.selected_image_path = image_path  # 这里更新选中的图片路径
        else:
            self.bottom_label.setText("图片加载失败")

    def start_makeup(self):
        """ 模拟发送消息2 """
        print("开始仿妆")
        self.start_makeup_signal.emit()

    def switch_to_i_output_page(self,event):
        # 触发页面切换回调
        self.switch_to_i_output_page_callback()

    def send_message_0(self):
        shared.capture_event.set()
        print("已按下拍摄键")

    def send_message_1(self):
        """ 确认妆容并将display_selected_image显示的图片上传至指定文件夹，并重新命名为 'new_image.jpg' """
        if not self.selected_image_path:
            QMessageBox.warning(self, "警告", "没有选择图片上传")
            return

        # 确定目标文件夹
        destination_folder = os.path.expanduser(r'D:\software\PyCharm\Py_Projects\pifect_mirror\data')

        if not os.path.exists(destination_folder):
            try:
                os.makedirs(destination_folder, exist_ok=True)  # 如果文件夹不存在，则创建
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法创建目标文件夹: {e}")
                return

        # 检查源文件是否存在
        if not os.path.exists(self.selected_image_path):
            QMessageBox.critical(self, "错误", "源图片不存在，无法上传")
            return

        # 确保目标文件夹可写
        if not os.access(destination_folder, os.W_OK):
            QMessageBox.critical(self, "错误", f"没有目标文件夹 {destination_folder} 的写入权限")
            return

        # 指定新的文件名
        new_file_name = "makeup.jpg"
        destination_path = os.path.join(destination_folder, new_file_name)

        # try:
        shutil.copy(self.selected_image_path, destination_path)  # 复制图片到目标文件夹并重命名
        #     QMessageBox.information(self, "成功", f"图片已上传并重命名为 {destination_path}")
        # except PermissionError:
        #     QMessageBox.critical(self, "错误", "权限不足，无法写入文件。请检查文件夹权限或尝试使用其他文件夹。")
        # except Exception as e:
        #     QMessageBox.critical(self, "错误", f"图片上传失败: {e}")

        from testparsed import evaluate
        evaluate(dspth='D:\software\PyCharm\Py_Projects\pifect_mirror\data', cp='79999_iter.pth')
        from move_and_run import move_and_run
        move_and_run()

        #if os.listdir('D:\software\PyCharm\Py_Projects\pifect_mirror\test\images'):
            #time.sleep(1)
        from test import pair_test
        pair_test()



    def send_message_2(self):
        """ 模拟发送消息2 """
        print("开始仿妆")

    def switch_to_select_page(self):
        """ 返回主页面 """
        self.switch_to_select_page_callback()


