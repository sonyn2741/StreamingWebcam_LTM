import socket,cv2, pickle,struct
import pyshine as ps 
import imutils 
from datetime import datetime
import time

# vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
vid = cv2.VideoCapture(0)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.100.3' #server
port = 9999
client_socket.connect((host_ip,port))
prev_frame_time = 0
new_frame_time = 0
if client_socket: 
	while (vid.isOpened()):
		try:
			img, frame = vid.read()
   
			new_frame_time = time.time()
			fps = 1/(new_frame_time-prev_frame_time)
			prev_frame_time = new_frame_time
			fps = int(fps)
			fps = "FPS = " + str(fps)
			
			frame = imutils.resize(frame,width=800)
			time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")	
			frame =  ps.putBText(frame,time_now,10,10,vspace=10,hspace=1,font_scale=0.7, background_RGB=(255,0,0),text_RGB=(255,250,250))
			frame = ps.putBText(frame,fps,680,10,vspace=10,hspace=1,font_scale=0.7, background_RGB=(255,0,0),text_RGB=(255,250,250))
			a = pickle.dumps(frame) 
			message = struct.pack("Q",len(a))+a
			client_socket.sendall(message)
   
			# cv2.imshow(f"TO: {host_ip}",frame)
			key = cv2.waitKey(1) & 0xFF
			if key == ord("q"):
				client_socket.close()
		except:
			print('\nVIDEO FINISHED!\n\n')
			break
	cv2.destroyAllWindows()		
