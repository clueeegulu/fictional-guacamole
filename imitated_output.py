import os
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
import time
from PyQt5.QtCore import pyqtSignal

class ImitatedOutputWindow(QWidget):
    on_makeup_start = pyqtSignal()
    def __init__(self, image_directory2, switch_to_imitated_page_callback):
        super().__init__()
        self.image_directory = image_directory2
        self.switch_to_imitated_page_callback = switch_to_imitated_page_callback

        # 创建图片显示区域
        self.imitated_label = QLabel(self)
        self.imitated_label.setFixedSize(400, 400)  # 设置图片显示区域大小
        self.imitated_label.setAlignment(Qt.AlignCenter)  # 图片居中显示
        self.imitated_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 在图片上方添加居中的文本标签
        self.text_label = QLabel("❀美美上妆❀", self)
        self.text_label.setAlignment(Qt.AlignCenter)  # 文字居中显示
        self.text_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FF69B4;")  # 设置字体样式

        # 创建按钮
        self.change_button = QPushButton('重新选择妆容', self)
        self.change_button.clicked.connect(self.switch_to_imitated_page)

        # 创建布局
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.change_button, alignment=Qt.AlignLeft)  # 按钮位于左上角
        top_layout.addStretch(1)  # 右侧留空

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.text_label)  # 将文字标签添加到图片上方

        # 添加1cm的垂直间距
        spacer = QSpacerItem(0, 38, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_layout.addItem(spacer)  # 添加间距

        main_layout.addWidget(self.imitated_label, alignment=Qt.AlignCenter)  # 图片位于页面中央

        # 设置主布局的内边距，减小页面顶部与文字之间的距离
        main_layout.setContentsMargins(10, 10, 10, 10)  # 减少顶部间距
        self.setLayout(main_layout)

    def on_makeup_start(self):
        # 收到信号后，打印“start”
        print("start")
        self.load_latest_image_2()

    def load_latest_image_2(self):
        """ 从文件夹中读取最后一张图片 """
        # 获取文件夹中的所有文件路径
        files = [os.path.join(self.image_directory, f) for f in os.listdir(self.image_directory) if os.path.isfile(os.path.join(self.image_directory, f))]

        # 筛选图片文件
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

        # 如果文件夹中没有图片
        if not image_files:
            self.imitated_label.setText("没有图片")
            return

        # 根据修改时间获取最新的图片
        latest_image = max(image_files, key=os.path.getmtime)
        # 加载图片
        pixmap = QPixmap(latest_image).scaled(400, 400, Qt.KeepAspectRatio)

        # 如果图片加载成功则显示，否则显示加载失败提示
        if not pixmap.isNull():
            self.imitated_label.setPixmap(pixmap)
        else:
            self.imitated_label.setText("图片加载失败")

    def switch_to_imitated_page(self):
        # 触发页面切换回调
        self.switch_to_imitated_page_callback()
