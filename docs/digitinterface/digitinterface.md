# DigitInterface

[Digitinterface Index](../README.md#digitinterface-index) /
[Digitinterface](./index.md#digitinterface) /
DigitInterface

> Auto-generated documentation for [digitinterface.digitinterface](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py) module.

- [DigitInterface](#digitinterface)
  - [BasicClient](#basicclient)
    - [BasicClient().closed](#basicclient()closed)
    - [BasicClient().opened](#basicclient()opened)
    - [BasicClient().received_message](#basicclient()received_message)
  - [DigitInterface](#digitinterface-1)
    - [DigitInterface().close_gripper](#digitinterface()close_gripper)
    - [DigitInterface().get_wrist_pose](#digitinterface()get_wrist_pose)
    - [DigitInterface().move_at_velocity](#digitinterface()move_at_velocity)
    - [DigitInterface().move_both_arms_sequentially_to_pose](#digitinterface()move_both_arms_sequentially_to_pose)
    - [DigitInterface().move_both_wrists_to_pose](#digitinterface()move_both_wrists_to_pose)
    - [DigitInterface().move_to_waypoint](#digitinterface()move_to_waypoint)
    - [DigitInterface().move_torso_to_pose](#digitinterface()move_torso_to_pose)
    - [DigitInterface().move_wrist_to_pose](#digitinterface()move_wrist_to_pose)
    - [DigitInterface().open_gripper](#digitinterface()open_gripper)
    - [DigitInterface().perform_actions_concurrently](#digitinterface()perform_actions_concurrently)
    - [DigitInterface().perform_actions_sequentially](#digitinterface()perform_actions_sequentially)

## BasicClient

[Show source in digitinterface.py:6](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L6)

Websocket Client Class

#### Arguments

- `ip` *string* - Websocket URI. For simulation, it is "ws://127.0.0.1:8080"
            and for the physical robot, it is "ws://10.10.1.1:8080"
- `protocols` *list* - It is always ["json-v1-agility"]

#### Returns

A web socket object with which you can send and receive
        JSON messages to digit as well as open or close the web
        socket connection

Type: *WebSocketClient*

#### Signature

```python
class BasicClient(WebSocketClient):
    ...
```

### BasicClient().closed

[Show source in digitinterface.py:31](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L31)

 Sends the privilege request command over the web socket to Digit
to request command privilege for the user.

#### Signature

```python
def closed(self, code, reason):
    ...
```

### BasicClient().opened

[Show source in digitinterface.py:19](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L19)

Sends the privilege request command over the web socket to Digit
to request command privilege for the user.

#### Signature

```python
def opened(self):
    ...
```

### BasicClient().received_message

[Show source in digitinterface.py:37](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L37)

Receives message from Digit through the web socket connection

#### Arguments

- `m` *JSON* - The JSON message received from Digit.

#### Signature

```python
def received_message(self, m):
    ...
```



## DigitInterface

[Show source in digitinterface.py:70](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L70)

#### Signature

```python
class DigitInterface:
    def __init__(self, client):
        ...
```

### DigitInterface().close_gripper

[Show source in digitinterface.py:272](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L272)

This is a docstring for the some_method method.

#### Signature

```python
def close_gripper(self, armname):
    ...
```

### DigitInterface().get_wrist_pose

[Show source in digitinterface.py:241](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L241)

Returns the pose rpyxyz of the wrist of Digit

#### Arguments

- `armname` *string* - "left" or "right"

- `reference_frame` *string* - Frame of reference of the wrist pose.
        The default is "base" which is the pelvis of Digit.

#### Returns

The pose of the wrist in a python List formatted as
        [roll pitch yaw x y z]

Type: *list*

#### Signature

```python
def get_wrist_pose(self, armname, reference_frame="base"):
    ...
```

### DigitInterface().move_at_velocity

[Show source in digitinterface.py:312](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L312)

Commands the robot to move at a desired velocity

#### Arguments

- `waypoint` *list* - spatial velocity of the robot's base in
            a python List formatted as [yaw_velocity, vx, vy]

- `execute` *bool* - Whether or not to execute this action

- `execute` *bool* - Whether or not to execute this action

#### Returns

The JSON message command in Python syntax

Type: *list*

#### Signature

```python
def move_at_velocity(
    self, velocity, avoid_obstacles=True, obstacle_threshold=0.5, execute=True
):
    ...
```

### DigitInterface().move_both_arms_sequentially_to_pose

[Show source in digitinterface.py:178](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L178)

Maintains the pose of one wrist as the other wrist moves to a
specified pose

#### Arguments

- `pose` *list* - The desired pose of the target wrist in a python List formatted as
        [roll pitch yaw x y z]

- `armname` *string* - "left" or "right". The name of the target wrist

- `prevarmname` *string* - "left" or "right". The name of the other arm

- `prevarmpose` *list* - The pose at which to maintain the other arm in a python List formatted as
        [roll pitch yaw x y z]

- `duration` *float* - The desired duration of the entire motion in seconds.

- `execute` *bool* - Whether or not to execute this action

#### Returns

The JSON message command in Python syntax

Type: *list*

#### Signature

```python
def move_both_arms_sequentially_to_pose(
    self, pose, armname, prevarmname, prevarmpose, duration=2.0, execute=True
):
    ...
```

### DigitInterface().move_both_wrists_to_pose

[Show source in digitinterface.py:86](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L86)

Moves both wrists concurrently to the specified poses

#### Arguments

- `lpose` *list* - The desired pose of the left wrist in a python List formatted as
        [roll pitch yaw x y z]

- `rpose` *list* - The desired pose of the right wrist in a python List formatted as
        [roll pitch yaw x y z]

- `duration` *float* - The desired duration of the entire motion in seconds.

- `execute` *bool* - Whether or not to execute this action

#### Returns

The JSON message command in Python syntax

Type: *list*

#### Signature

```python
def move_both_wrists_to_pose(self, lpose, rpose, duration=2.0, execute=True):
    ...
```

### DigitInterface().move_to_waypoint

[Show source in digitinterface.py:283](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L283)

Commands the robot to move to a desired waypoint

#### Arguments

- `waypoint` *list* - target waypoint to walk to in the specified reference frame
         in a python List formatted as [yaw, x, y]

- `execute` *bool* - Whether or not to execute this action

#### Returns

The JSON message command in Python syntax

Type: *list*

#### Signature

```python
def move_to_waypoint(
    self,
    waypoint,
    position_tolerance=0.2,
    orientation_tolerance=0.2,
    avoid_obstacles=True,
    obstacle_threshold=0.5,
    reference_frame="world",
    execute=True,
):
    ...
```

### DigitInterface().move_torso_to_pose

[Show source in digitinterface.py:340](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L340)

Commands the torso to move to a specified position and
orientation relative to the center of the robot's support polygon

#### Arguments

- `pose` *list* - The desired pose of the torso in a python List formatted as
            [roll pitch yaw x y z]

- `duration` *float* - The desired duration of the entire motion in seconds.

- `execute` *bool* - Whether or not to execute this action

#### Returns

The JSON message command in Python syntax

Type: *list*

#### Signature

```python
def move_torso_to_pose(self, pose, duration=5.0, execute=True):
    ...
```

### DigitInterface().move_wrist_to_pose

[Show source in digitinterface.py:143](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L143)

Moves the specified wrist to the specified pose

#### Arguments

- `pose` *list* - The desired pose of the wrist in a python List formatted as
        [roll pitch yaw x y z]

- `armname` *string* - "left" or "right"

- `duration` *float* - The desired duration of the entire motion in seconds.

- `execute` *bool* - Whether or not to execute this action

#### Returns

The JSON message command in Python syntax

Type: *list*

#### Signature

```python
def move_wrist_to_pose(self, pose, armname, duration=2.0, execute=True):
    ...
```

### DigitInterface().open_gripper

[Show source in digitinterface.py:277](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L277)

This is a docstring for the some_method method.

#### Signature

```python
def open_gripper(self, armname):
    ...
```

### DigitInterface().perform_actions_concurrently

[Show source in digitinterface.py:365](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L365)

Execute a list of actions simultaneously

#### Arguments

- `actions` *list* - A list of JSON message commands in Python syntax

- `execute` *bool* - Whether or not to execute this action

#### Returns

The JSON message command in Python syntax

Type: *list*

#### Signature

```python
def perform_actions_concurrently(self, actions, execute=True):
    ...
```

### DigitInterface().perform_actions_sequentially

[Show source in digitinterface.py:383](https://github.com/adubredu/digitinterface/blob/main/digitinterface/digitinterface.py#L383)

Execute a list of actions sequentially

#### Arguments

- `actions` *list* - A list of JSON message commands in Python syntax

- `execute` *bool* - Whether or not to execute this action

#### Returns

The JSON message command in Python syntax

Type: *list*

#### Signature

```python
def perform_actions_sequentially(self, actions, execute=True):
    ...
```