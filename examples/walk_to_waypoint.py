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

desired_waypoint = [1.57, 5.0, 5.0] #[yaw, x, y]
digit.move_to_waypoint(desired_waypoint, avoid_obstacles=False)
sleep(20)


sleep(5)

# close the web socket connection
client.close()