import cv2
from datetime import datetime
import socket
import pickle
import struct
import imutils
import threading
import pyshine as ps

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('\nHOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(10)
print("Listening at", socket_address)


def receive_client(addr, client_socket):
    try:
        print('Client {} CONNECTED!'.format(addr))
        if client_socket:
            data = b""
            payload_size = struct.calcsize("Q")  # Q: 8 bytes
            while True:
                
                while len(data) < payload_size:                   
                    packet = client_socket.recv(4*1024)# 4K
                    if not packet:
                        break
                    data += packet

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]  # Dữ liệu khung hình thực tế
                msg_size = struct.unpack("Q", packed_msg_size)[0]  # kích thước tin nhắn

                while len(data) < msg_size:
                    data += client_socket.recv(4*1024) # khôi phục dữ liệu khung hình thực tế

                
                frame_data = data[:msg_size]
                data = data[msg_size:] 
                frame = pickle.loads(frame_data)# giải mã byte thành loại khung hình thực tế
                
                # Chèn text
                text = f"Client: {addr}"
                frame = ps.putBText(frame, text, 10, 50, vspace=10, hspace=1, font_scale=0.7, background_RGB=(
                    255, 0, 0), text_RGB=(255, 250, 250))
                
                # Hiển thị
                cv2.imshow(f"From {addr}", frame)
                           
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
            client_socket.close()
    except Exception as e:
        print(f"Client {addr} DISCONNECTED\n")
        pass


if __name__ == "__main__":
    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(
            target=receive_client, args=(addr, client_socket))
        thread.start()
        print("Total Client:  ", threading.activeCount() - 1)
