"""
  fu
time:2024/8/29 9:54
"""
import time
from MirrorUI import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QMovie
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
from bs4 import BeautifulSoup
import urllib.request,urllib.error
import re
import pprint
import socket
import threading
from MirrorUI import Ui_MainWindow

class MQTT(QObject):
    mqttSignal = pyqtSignal(object)  # 发送Python对象
    def __init__(self):
        super(MQTT, self).__init__()
        self.mqttSignal.emit("que")

class ThirdPartInfo:
    def __init__(self):
        pass
    # 获取外网IP
    def GetOuterIP(self):
        try:
            ip = requests.get('http://whatismyip.akamai.com/', timeout=30).text
            return ip
        except requests.RequestException as e:
            print("Error occurred while getting outer IP:", str(e))
            return None
    def IPLocation(self, ip, max_retries=5):
        url = f"http://ip-api.com/json/{ip}?fields=country,city"
        # 第一次请求，打印国家和城市信息
        try:
            response = requests.get(url)
            data = response.json()
            print("Country: ", data.get('country', 'Not found'))
            print("City: ", data.get('city', 'Not found'))
        except requests.RequestException as e:
            print("Initial request error:", str(e))
            return None

        # 循环请求以获取 IP 信息，处理错误和重试
        attempt = 0
        while attempt < max_retries:
            try:
                sess = requests.session()
                sess.keep_alive = False
                ip_dict = sess.get(url, timeout=30).json()

                # 检查 API 响应中的状态
                if ip_dict.get('status') == 'fail':
                    print("Error: ", ip_dict.get('message', 'No error message provided'))
                    attempt += 1
                    continue  # 重新尝试
                else:
                    return ip_dict

            except requests.RequestException as e:
                print("IPLocation Err!", str(e))
                attempt += 1
                continue  # 重新尝试

        print("Failed to retrieve IP information after several attempts.")
        return None
    # 输入位置，查询天气
    def weather(self,locate):
        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={locate}&appid=8d92d3404e812a0066a720a9e4d12b62&units=metric'
            response = requests.get(url)
            response.raise_for_status()  # 确保请求成功
            data = response.json()
            if 'weather' in data and 'main' in data:
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                wind_speed = data['wind']['speed']
                humidity = data['main']['humidity']
                return [weather_description, '', temperature, wind_speed, '', humidity]
                print(weather_description, '', temperature, wind_speed, '',humidity)
            else:
                print("无法提取天气信息")
                return []

        except requests.RequestException as e:
            print(f"网络请求错误: {e}")
            return []
        except Exception as e:
            print(f"未知错误: {e}")
            return []
    # 下载图片
    def downloadPic(self, url, path):
        with open(path, 'wb') as f:
            f.write(requests.get(url).content)

class ExQThread(QThread):
    weatherSignal = pyqtSignal(list, str)
    timeSignal = pyqtSignal(str, str, str)
    def __init__(self):
        super(ExQThread, self).__init__()
        self.thirdPart = ThirdPartInfo()
        self.running = True
    def updateTime(self):
        datetime = QDateTime.currentDateTime()
        time = datetime.toString('hh:mm')
        date = datetime.toString('yyyy年MM月dd日')
        week = datetime.toString('dddd')
        self.timeSignal.emit(time, date, week)
    def updateWeather(self):
        ip = self.thirdPart.GetOuterIP()
        print('>> ip:', ip)
        locate = self.thirdPart.IPLocation(ip)
        print('>> locate:', locate)
        res = self.thirdPart.weather(locate['city'])
        print('>> weather:', res)
        weather = res[0]
        iconURL = res[1]
        path = 'source/icon/' + weather + '.png'
        # 判断是否为极端天气
        extreme_weather = False
        weather_description = weather.lower()
        if 'thunderstorm' in weather_description or 'snow' in weather_description or 'moderate rain' in weather_description:
            extreme_weather = True

        if extreme_weather:
            self.weatherSignal.emit(res, path)
            self.mqttSignal.emit("极端天气，请注意安全~")
        else:
            for i in os.listdir('source/icon/'):
             if weather == i.split('.')[0]:
                path = 'source/icon/' + i
                self.weatherSignal.emit(res, path)
                return
        self.weatherSignal.emit(res, path)
    def run(self):
        cnt = 0
        while self.running:
            try:
                if cnt % 10 == 0:
                    self.updateTime()
                    print('updateTime')
                if cnt % 600 == 0:
                    self.updateWeather()
                    print('updateWeather')
                '''if cnt % 10 == 0:
                    self.updateHistory()
                    print('updateHistory')
                if cnt % 10 == 0:
                    self.updateHeadlines()
                    print('updateHeadlines')
                if cnt % 5 == 0:
                    self.updateTempHum()
                    print('updateTempHum')
                if cnt >= 600:
                    cnt = 0'''
            except Exception as e:
                print(e)
            cnt += 1
            time.sleep(1)

class MagicUI(QMainWindow, Ui_MainWindow):  # 或者 QWidget，如果你只需要一个基本的窗口
    def __init__(self, switch_to_select_page_callback=None):
        super(MagicUI, self).__init__()  # 初始化 QMainWindow 或 QWidget
        self.switch_to_select_page_callback = switch_to_select_page_callback
        self.todo_string = ''
        self.todo_cnt = 0

        self.setupUi(self)  # 设置 UI

        # 创建线程
        self.exQthread = ExQThread()
        # 连接信号槽
        self.exQthread.timeSignal.connect(self.updateTime)
        self.exQthread.weatherSignal.connect(self.updateWeather)

        # 启动线程
        self.exQthread.start()

    def mousePressEvent(self, event):
        # 捕捉整个页面的点击事件
        if event.button() == Qt.LeftButton:
            # 发射点击信号或执行切换页面的操作
            self.switch_to_select_page_callback()

    def setupUi(self, MainWindow):
        super(MagicUI, self).setupUi(MainWindow)
        self.label_nong.setText("今天好！也要继续加油o！")
        self.gif = QMovie("source/chiikawa.gif")
        self.label.setMovie(self.gif)
        self.gif.setSpeed(25)
        self.gif.start()
        pass

    def updateCommunicate(self, msg):
        if "警报：" in msg:
            self.label_nong.setText(msg)
        else:
            self.label_nong.setText("今天好！也要继续加油o！")
    def updateTime(self, time, date, week):
        print(f"Time received in UI: {time}, {date}, {week}")
        self.label_time.setText(time)
        self.label_date.setText(date)
        self.label_week.setText(week)
    def updateWeather(self, res, path):
        weather = res[0]
        tips = res[5]
        tip = res[3]
        tips_str = f"{tips}%  {tip}m/s"
        range_str= f"temperature: {res[2]}°C"
        self.label_describe.setText(weather.center(8))
        self.label_others.setText(tips_str)
        self.label_weather.setText(range_str)
        self.label_weathericon.setPixmap(QtGui.QPixmap(path))

    def closeEvent(self, event):
            self.exQthread.running = False
            self.exQthread.wait()
            event.accept()

def start_server():
    host = '0.0.0.0'
    port = 12426
    max_zeros = 5  # 连续0的最大数量

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("等待客户端连接...")

    program_started = False  # 记录程序是否已经启动
    zero_count = 0  # 计数器初始化

    while True:
        conn, address = server_socket.accept()
        print("连接来自: " + str(address))

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print("从客户端收到的数据: " + str(data))

            if data == '0':
                zero_count += 1
                if zero_count >= max_zeros:
                    print("连续检测到20个0，自动关闭程序")
                    conn.close()
                    sys.exit()
            else:
                zero_count = 0  # 如果收到的数据不是0，重置计数器

            if data == '1':
                if not program_started:
                    # 启动 GUI 程序（第一次检测到1时）
                    threading.Thread(target=main).start()
                    program_started = True

        conn.close()

def main():
    app = QApplication(sys.argv)
    window = MagicUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    time.sleep(2)
    main()
