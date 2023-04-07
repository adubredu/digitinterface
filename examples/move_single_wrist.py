from digitinterface.digitinterface import BasicClient
from digitinterface.digitinterface import DigitInterface
from time import sleep

# websocket URIs
ip_real = "ws://10.10.1.1:8080"
ip_sim = "ws://127.0.0.1:8080"

# connect to the AR Digit server
client = BasicClient(ip_sim, protocols=["json-v1-agility"])
client.daemon = False 
while True:
    try:
        client.connect()
        print("WS connection established")
        sleep(1)
        break
    except:
        print('WS connection NOT established')
        sleep(1)

# create a DigitInterface object
digit = DigitInterface(client)

task = "move left wrist"

if task == "move left wrist":
    left_wrist_pose = [0.0, 0.0, 0.0, 0.2, 0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    digit.move_wrist_to_pose(left_wrist_pose, "left", duration=1.0)

elif task == "move right wrist":
    right_wrist_pose = [0.0, 0.0, 0.0, 0.2, -0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    digit.move_wrist_to_pose(right_wrist_pose, "right", duration=1.0)




sleep(5)

# close the web socket connection
client.close()