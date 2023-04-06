import sys 
sys.path.append("digitinterface")
from digitinterface import BasicClient
from digitinterface import DigitInterface
from time import sleep

ip_real = "ws://10.10.1.1:8080"
ip_sim = "ws://127.0.0.1:8080"

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

digit = DigitInterface(client)

task = "sequential actions"

if task == "wrist pose":
    left_wrist_pose = digit.get_wrist_pose("left")
    right_wrist_pose = digit.get_wrist_pose("right")
    print("left wrist pose: ",left_wrist_pose)
    print("right wrist pose: ", right_wrist_pose)

elif task == "move left wrist":
    left_wrist_pose = [0.0, 0.0, 0.0, 0.2, 0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    digit.move_wrist_to_pose(left_wrist_pose, "left", duration=1.0)

elif task == "move right wrist":
    right_wrist_pose = [0.0, 0.0, 0.0, 0.2, -0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    digit.move_wrist_to_pose(right_wrist_pose, "right", duration=1.0)

elif task == "move both wrists":
    left_wrist_pose = [0.0, 0.0, 0.0, 0.2, 0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    right_wrist_pose = [0.0, 0.0, 0.0, 0.2, -0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    digit.move_both_wrists_to_pose(left_wrist_pose, right_wrist_pose, duration=1.0)

elif task == "move wrists sequentially":
    left_wrist_pose = [0.0, 0.0, 0.0, 0.2, 0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    right_wrist_pose = [0.0, 0.0, 0.0, 0.2, -0.3, 0.2] #[roll,pitch,yaw,x,y,z]
    digit.move_wrist_to_pose(right_wrist_pose, "right", duration=1.0)
    sleep(3)
    digit.move_both_arms_sequentially_to_pose(left_wrist_pose, "left", "right", right_wrist_pose, duration=1.0)

elif task == "move at velocity":
    desired_velocity = [0.0, 0.5, 0.0]
    digit.move_at_velocity(desired_velocity, avoid_obstacles=False)
    sleep(10)

elif task == "move to waypoint":
    desired_waypoint = [1.57, 5.0, 5.0]
    digit.move_to_waypoint(desired_waypoint, avoid_obstacles=False)
    sleep(20)

elif task == "move torso to pose":
    desired_pose = [0.3, 0.4, 0.0, 0.0, 0.0, 0.7]
    digit.move_torso_to_pose(desired_pose)
    sleep(10)

elif task == "concurrent actions":
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
client.close()