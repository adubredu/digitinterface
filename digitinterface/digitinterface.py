import numpy as np
import json
from ws4py.client.threadedclient import WebSocketClient
from time import sleep
import serial

class BasicClient(WebSocketClient):
    """Websocket Client Class
 
        :param string ip: Websocket URI. For simulation, it is "ws://127.0.0.1:8080" 
                    and for the physical robot, it is "ws://10.10.1.1:8080"
        :param list protocols: It is always ["json-v1-agility"]
        
        :returns: A web socket object with which you can send and receive
                JSON messages to digit as well as open or close the web 
                socket connection
        
        :rtype: WebSocketClient
    """
    def opened(self):
        """Sends the privilege request command over the web socket to Digit
            to request command privilege for the user.
        """
        self.operation_mode = None
        self.responded = True
        self.arm_pose = []
        privilege_request = ['request-privilege', 
                                {'privilege' : 'change-action-command',
                                 'priority' : 0}]
        self.send(json.dumps(privilege_request))

    def closed(self, code, reason):
        """ Sends the privilege request command over the web socket to Digit
            to request command privilege for the user.
        """
        print(("Closed", code, reason))

    def received_message(self, m):
        """ Receives message from Digit through the web socket connection
            
            :param JSON m: The JSON message received from Digit.
        """
        dataloaded = json.loads(m.data)
        message_type = str(dataloaded[0])
        message_dict = dataloaded[1]

        if message_type == 'privileges':
            self.done = message_dict['privileges'][0]['has']
            if self.done:
                print("Privilege request executed successfully.")

        elif message_type == 'robot-status':
            self.responded = True
            self.operation_mode = str(message_dict['operation-mode'])

        elif message_type == 'error':
            self.error_info = str(message_dict['info'])
            print('Error: ', self.error_info)

        elif message_type == 'action-status-changed':
            if message_dict['status'] == 'running': 
                self.completed = False

            elif message_dict['status'] == 'success': 
                self.completed = True
                
        elif message_type == 'object-kinematics':  
            self.arm_pose = message_dict['transform']['rpyxyz'] 


class DigitInterface:
    def __init__(self, client):
        """Initializes DigitInterface class

        :param WebsocketClient client: A WebsocketClient object

        :returns: A DigitInterface object

        :rtype: DigitInterface

        """
        self.client = client 
        self.armname = {'right':'right-hand', 'left':'left-hand'}
        self.arm_id = {'right':0, 'left':1}
        self.gripper1 = None 
        self.gripper2 = None

# arm motion
    def move_both_wrists_to_pose(self, lpose, rpose, duration=2.0, execute=True):
        """Moves both wrists concurrently to the specified poses

            :param list lpose: The desired pose of the left wrist in a python List formatted as 
                    [roll pitch yaw x y z] 

            :param list rpose: The desired pose of the right wrist in a python List formatted as 
                    [roll pitch yaw x y z] 

            :param float duration: The desired duration of the entire motion in seconds. 

            :param bool execute: Whether or not to execute this action 

            :returns: The JSON message command in Python syntax 

            :rtype: list
             
        """
        msg = ["action-concurrent",
                {
                    "actions": [
                        ["action-end-effector-move",
                              {
                                "end-effector": 'left-hand',
                                "waypoints": [
                                              {"rpyxyz":[*lpose]},
                                              {"rpyxyz":[*lpose]}],
                                "reference-frame": {
                                  "robot-frame": "base"
                                },
                                "stall-threshold": None,
                                "cyclic": False,
                                "max-speed": 0.5,
                                "duration": duration,
                                "transition-duration": None
                              }, 0],
                        ["action-end-effector-move",
                            {
                                "end-effector": 'right-hand',
                                "waypoints": [
                                              {"rpyxyz":[*rpose]},
                                              {"rpyxyz":[*rpose]}],
                                "reference-frame": {
                                  "robot-frame": "base"
                                },
                                "stall-threshold": None,
                                "cyclic": False,
                                "max-speed": 0.5,
                                "duration": duration,
                                "transition-duration": None
                              }, 0]  
                    ]
                }
        ]
        if execute: self.client.send(json.dumps(msg))
        return msg

    def move_wrist_to_pose(self, pose, armname, duration=2.0, execute=True):  
        """Moves the specified wrist to the specified pose

            :param list pose: The desired pose of the wrist in a python List formatted as 
                    [roll pitch yaw x y z] 

            :param string armname: "left" or "right"

            :param float duration: The desired duration of the entire motion in seconds. 

            :param bool execute: Whether or not to execute this action 
             
            :returns: The JSON message command in Python syntax 

            :rtype: list 
        """
        arm = self.armname[armname]
        msg = ["action-end-effector-move",
          {
            "end-effector": arm,
            "waypoints": [
                          {"rpyxyz":[*pose]},
                          {"rpyxyz":[*pose]}],
            "reference-frame": {
              "robot-frame": "base"
            },
            "stall-threshold": None,
            "cyclic": False,
            "max-speed": 0.5,
            "duration": duration,
            "transition-duration": None
          }, 0] 
        if execute: self.client.send(json.dumps(msg)) 
        return msg

    def move_both_arms_sequentially_to_pose(self, pose, armname, prevarmname, prevarmpose, duration=2.0, execute=True):
        """Maintains the pose of one wrist as the other wrist moves to a 
            specified pose

            :param list pose: The desired pose of the target wrist in a python List formatted as 
                    [roll pitch yaw x y z] 

            :param string armname: "left" or "right". The name of the target wrist

            :param string prevarmname: "left" or "right". The name of the other arm

            :param list prevarmpose: The pose at which to maintain the other arm in a python List formatted as 
                    [roll pitch yaw x y z] 

            :param float duration: The desired duration of the entire motion in seconds. 

            :param bool execute: Whether or not to execute this action 
             
            :returns: The JSON message command in Python syntax 

            :rtype: list
        """
        current_arm = self.armname[armname]
        previous_arm = self.armname[prevarmname]
        msg = ["action-concurrent",
                {
                    "actions": [
                        ["action-end-effector-move",
                            {
                                "end-effector": previous_arm,
                                "waypoints": [
                                            {"rpyxyz":[*prevarmpose]},
                                            {"rpyxyz":[*prevarmpose]}],
                                "reference-frame": {
                                "robot-frame": "base"
                                },
                                "stall-threshold": None,
                                "cyclic": False,
                                "max-speed": 0.5,
                                "duration": duration,
                                "transition-duration": None
                            }, 0],
                        ["action-end-effector-move",
                            {
                                "end-effector": current_arm,
                                "waypoints": [
                                            {"rpyxyz":[*pose]},
                                            {"rpyxyz":[*pose]}],
                                "reference-frame": {
                                "robot-frame": "base"
                                },
                                "stall-threshold": None,
                                "cyclic": False,
                                "max-speed": 0.5,
                                "duration": duration,
                                "transition-duration": None
                            }, 0]  
                    ]
                }
        ]
        if execute: self.client.send(json.dumps(msg))  
        return msg

    def get_wrist_pose(self, armname, reference_frame="base"):
        """Returns the pose rpyxyz of the wrist of Digit

            :param string armname: "left" or "right"

            :param string reference_frame: Frame of reference of the wrist pose. 
                    The default is "base" which is the pelvis of Digit. 
            
            :returns: The pose of the wrist in a python List formatted as 
                    [roll pitch yaw x y z] 

            :rtype: list
        """
        arm = self.armname[armname]
        msg = [
            "get-object-kinematics",
            {
                "object": {"robot-frame":arm},
                "relative-to": {
                "robot-frame":reference_frame
                },
                "in-coordinates-of": {}
            }
            ]
        self.client.send(json.dumps(msg))
        sleep(0.05)
        pose = self.client.arm_pose 
        return pose


# gripper motion
    def start_up_gripper1(self, serialport, baudrate=9600):
        """Creates a serial object for gripper 1

        :param string serialport: The path to Gripper 1's serial port. It should
                look like "/dev/tty/USBX" where "X" is a number

        :param int baudrate: The baud rate of the serial communication. 

        """
        if self.gripper1 is None:
            self.gripper1 = serial.Serial(serialport, baudrate)       

    def start_up_gripper2(self, serialport, baudrate=9600):
        """Creates a serial object for gripper 2

        :param string serialport: The path to Gripper 2's serial port. It should
                look like "/dev/tty/USBX" where "X" is a number

        :param int baudrate: The baud rate of the serial communication. 

        """
        if self.gripper2 is None:
            self.gripper2 = serial.Serial(serialport, baudrate) 

    def close_gripper1(self):
        """Closes the fingers of Gripper 1"""
        if self.gripper1 is None:
            print("Gripper 1 not initialized")
            return
        self.gripper1.write(b'c')

    def open_gripper1(self):
        """Opens the fingers of Gripper 1"""
        if self.gripper1 is None:
            print("Gripper 1 not initialized")
            return
        self.gripper1.write(b'o')

    def close_gripper2(self):
        """Closes the fingers of Gripper 2"""
        if self.gripper2 is None:
            print("Gripper 2 not initialized")
            return
        self.gripper2.write(b'c')

    def open_gripper2(self):
        """Opens the fingers of Gripper 2"""
        if self.gripper2 is None:
            print("Gripper 2 not initialized")
            return
        self.gripper2.write(b'o')


# locomotion
    def move_to_waypoint(self, waypoint, position_tolerance=0.2, orientation_tolerance=0.2,
                        avoid_obstacles=True, obstacle_threshold=0.5, reference_frame="world", execute=True):
        """Commands the robot to move to a desired waypoint  

            :param list waypoint: target waypoint to walk to in the specified reference frame
                     in a python List formatted as [yaw, x, y]

            :param bool execute: Whether or not to execute this action 

            :returns: The JSON message command in Python syntax 

            :rtype: list
        """
        msg = [
            "action-goto",
            {
                "target":{"rpyxyz":[0.0, 0.0, waypoint[0], waypoint[1], waypoint[2], 0.0]},
                "position-tolerance":position_tolerance,
                "orientation-tolerance":orientation_tolerance,
                "reference-frame":{"special-frame":reference_frame},
                "mobility-parameters":{
                    "avoid-obstacles":avoid_obstacles,
                    "obstacle-threshold":obstacle_threshold
                }
            }
        ] 
        if execute: self.client.send(json.dumps(msg))
        return msg

    def move_at_velocity(self, velocity, avoid_obstacles=True, obstacle_threshold=0.5, execute=True):
        """Commands the robot to move at a desired velocity  

            :param list waypoint: spatial velocity of the robot's base in
                        a python List formatted as [yaw_velocity, vx, vy]

            :param bool execute: Whether or not to execute this action 

            :param bool execute: Whether or not to execute this action 
            
            :returns: The JSON message command in Python syntax 

            :rtype: list
        """
        msg = [
            "action-move",
            {
                "velocity":{"rpyxyz":[0.0, 0.0, velocity[0], velocity[1], velocity[2], 0.0]},
                "mobility-parameters":{
                    "avoid-obstacles":avoid_obstacles,
                    "obstacle-threshold":obstacle_threshold
                }
            }
        ]
        if execute: self.client.send(json.dumps(msg))
        return msg

# miscellaneous motions 
    def move_torso_to_pose(self, pose, duration=5.0, execute=True):
        """Commands the torso to move to a specified position and 
        orientation relative to the center of the robot's support polygon

        :param list pose: The desired pose of the torso in a python List formatted as 
                    [roll pitch yaw x y z]  

        :param float duration: The desired duration of the entire motion in seconds.

        :param bool execute: Whether or not to execute this action 

        :returns: The JSON message command in Python syntax 

        :rtype: list 
        """
        msg = [
            "action-stand",
            {
                "base-pose":{"rpyxyz":[*pose]},
                "duration":duration
            }
        ]
        if execute: self.client.send(json.dumps(msg))
        return msg

    def perform_actions_concurrently(self, actions, execute=True):
        """Execute a list of actions simultaneously

        :param list actions: A list of JSON message commands in Python syntax

        :param bool execute: Whether or not to execute this action

        :returns: The JSON message command in Python syntax 

        :rtype: list
        
        """
        msg = ["action-concurrent",
                {"actions": actions}
        ]
        if execute: self.client.send(json.dumps(msg))
        return msg

    def perform_actions_sequentially(self, actions, execute=True):
        """Execute a list of actions sequentially

        :param list actions: A list of JSON message commands in Python syntax

        :param bool execute: Whether or not to execute this action

        :returns: The JSON message command in Python syntax 

        :rtype: list
        
        """
        msg = ["action-sequential",
                {"actions": actions}
        ]
        if execute: self.client.send(json.dumps(msg))
        return msg