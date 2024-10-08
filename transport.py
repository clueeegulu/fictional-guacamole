import socket
import time
import sys
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from Magicmain import MagicUI
from select import SelectPageWindow, ImitatedPageWindow
from imitated_output import ImitatedOutputWindow
from UI import MainWindow
import shared
import struct

wakeup = 0
def handle_client(client_socket):
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    app.exec_()  # 启动PyQt5事件循环

def handle_capture(client_socket):
    while True:
        shared.capture_event.wait()
        command = "capture"
        client_socket.sendall(command.encode())
        print(f"Sent command to client: {command}")

        data = b''
        while len(data) < 8:
            packet = client_socket.recv(8 - len(data))
            if not packet:
                break
            data += packet
        if not data:
            break

        print(f"服务器：接收到的图片大小字节为 {data}, 长度为 {len(data)} 字节")

        image_size = struct.unpack('!Q', data)[0]
        print(f"Expecting image of size: {image_size} bytes")

        client_socket.sendall("OK".encode('utf-8'))

        received_data = b""
        while len(received_data) < image_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            received_data += packet

        if len(received_data) == image_size:
            with open("D:\\software\\PyCharm\\Py_Projects\\pifect_mirror\\data\\nomakeup.jpg", "wb") as f:
                f.write(received_data)
            print(f"Image received and saved successfully as 'nomakeup.jpg'")
        else:
            print("Failed to receive complete image data.")

        client_socket.close()
        break

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'  # 监听所有可用的网络接口
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")


    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Received connection from {addr}")
            time.sleep(5)
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            capture_thread = threading.Thread(target=handle_capture, args=(client_socket,))
            client_thread.start()
            capture_thread.start()
    except KeyboardInterrupt:        print("Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
