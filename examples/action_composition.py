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

task = "concurrent actions"

if task == "concurrent actions":
    left_wrist_pose = [0.0, 0.0, 0.0, 0.2, 0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    act1 = digit.move_wrist_to_pose(left_wrist_pose, "left", duration=1.0)
    right_wrist_pose = [0.0, 0.0, 0.0, 0.2, -0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    act2 = digit.move_wrist_to_pose(right_wrist_pose, "right", duration=1.0)
    desired_pose = [0.3, 0.4, 0.0, 0.0, 0.0, 0.7]
    act3 = digit.move_torso_to_pose(desired_pose)
    digit.perform_actions_concurrently([act1, act2, act3])
    sleep(20)

elif task == "sequential actions":
    left_wrist_pose = [0.0, 0.0, 0.0, 0.2, 0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    act1 = digit.move_wrist_to_pose(left_wrist_pose, "left", duration=1.0)
    right_wrist_pose = [0.0, 0.0, 0.0, 0.2, -0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    act2 = digit.move_wrist_to_pose(right_wrist_pose, "right", duration=1.0)
    desired_pose = [0.3, 0.4, 0.0, 0.0, 0.0, 0.7]
    act3 = digit.move_torso_to_pose(desired_pose)
    digit.perform_actions_sequentially([act1, act2, act3])
    sleep(20)


sleep(5)

# close the web socket connection
client.close()