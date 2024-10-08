import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from Magicmain import MagicUI
from select import SelectPageWindow
from select import ImitatedPageWindow
from imitated_output import ImitatedOutputWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Magic Mirror")
        self.setGeometry(100, 100, 825, 1317) #设置窗口的位置和大小

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # 创建选择页面
        self.select_page_window = SelectPageWindow(switch_to_imitated_page_callback=self.switch_to_imitated_page,
                                                   switch_to_main_page_callback=self.switch_to_main_page)
        self.stack.addWidget(self.select_page_window)

        # 创建仿妆页面，初始时隐藏
        self.imitated_page_window = ImitatedPageWindow(switch_to_select_page_callback=self.switch_to_select_page,
                                                       image_directory=r"D:\software\PyCharm\Py_Projects\pifect_mirror\data",
                                                       switch_to_i_output_page_callback=self.switch_to_i_output_page)
        self.stack.addWidget(self.imitated_page_window)

       # 创建主页面，初始时隐藏
        self.main_page_window = MagicUI(switch_to_select_page_callback=self.switch_to_select_page)
        self.stack.addWidget(self.main_page_window)

        # 创建结果显示页面，初始时隐藏
        self.i_output_page_window = ImitatedOutputWindow(switch_to_imitated_page_callback=self.switch_to_imitated_page,
                                                         image_directory2=r"D:\software\PyCharm\Py_Projects\pifect_mirror\results\test_pair")
        self.stack.addWidget(self.i_output_page_window)

        # 设置主页面为默认页面 (主页面在索引 2 处)
        self.stack.setCurrentIndex(2)

        self.imitated_page_window.start_makeup_signal.connect(self.i_output_page_window.on_makeup_start)

    def switch_to_imitated_page(self):
        """ 切换到仿妆页面 """
        self.stack.setCurrentIndex(1)

    def switch_to_select_page(self):
        """ 切换回选择页面 """
        self.stack.setCurrentIndex(0)

    def switch_to_main_page(self):
        """ 切换回主页面 """
        self.stack.setCurrentIndex(2)

    def switch_to_i_output_page(self):
        """ 切换回仿妆结果输出页面 """
        self.stack.setCurrentIndex(3)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
