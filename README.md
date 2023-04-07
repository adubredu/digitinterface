# digitinterface

Python package for interacting with the Agility Robotics Digit v3 default controller interface.

## Requirements
Python version >= 3.6

## Installation
To install this package, run the following commands
```bash
git clone https://github.com/adubredu/digitinterface.git
cd digitinterface
pip install setuptools wheel ws4py
python setup.py install
```

## Usage
First start up an Agility Robotics Digit simulation session using the command below
```bash
./sim/run_sim.sh
```
Navigate to `http://localhost:8080/` in your web browser and click on `Gamepad Interface` in the list of options to visualize the simulation

Next, open a new terminal and run your Python script.

Check the [examples](examples) folder for usage examples. Check out the official [documentation](https://adubredu.github.io/digitinterface) for more details.

To run an example Python script, say the `move_single_wrist.py` example, the simply run the Python script as
```bash
python examples/move_single_wrist.py
```