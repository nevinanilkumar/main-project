import subprocess
import shlex, os
import socket,cv2, pickle,struct

def start_stream(host_ip, port):
    print("start stream")
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((host_ip,port)) 
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
            while len(data) < payload_size:
                    packet = client_socket.recv(254*1024) # 4Kb
                    if not packet: break
                    data+=packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            while len(data) < msg_size:
                    data += client_socket.recv(254*1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            print(len(frame_data))
            frame = pickle.loads(frame_data)
            cv2.namedWindow("RECEIVING VIDEO", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("RECEIVING VIDEO", 640, 480)
    
            cv2.imshow("RECEIVING VIDEO",frame)
            cv2.moveWindow("RECEIVING VIDEO", 40,30)
            cv2.resizeWindow("Resized_Window", 300, 700)
            if cv2.waitKey(1) == '13':
                    break
            cv2.getWindowProperty("RECEIVING VIDEO", 0)
    client_socket.close()

def connect_wifi(ssid, password):
	global current_wifi
	if (ssid != current_wifi):
        	subprocess.check_output(connect_network_cmd(ssid, password))
        	current_wifi = ssid
def getFrame():
  pass  
# commands
get_all_ssid_cmd = lambda : ['nmcli', '-f', 'SSID', 'dev', 'wifi']
get_current_ssid_cmd = lambda : ['iwgetid', '-r']
connect_network_cmd = lambda ssid, password : shlex.split(f"nmcli device wifi connect {ssid} password {password}")
# start_stream_play_cmd = lambda ip, port : shlex.split()
output = subprocess.check_output(get_all_ssid_cmd())
output = output.decode('utf-8')

networks = [i.strip() for i in output.split('\n')[1:] if i]
networks = list(set(networks))
# current wifi network
output = subprocess.check_output(get_current_ssid_cmd()).decode('utf-8')
current_wifi = output.strip()
# cam = VideoCapture(0)
