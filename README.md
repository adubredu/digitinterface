# digitinterface

Python package for interacting with the Agility Robotics Digit v3 default controller interface.

## Installation
To install this package, run the following commands
```bash
git clone https://github.com/adubredu/digitinterface.git
cd digitinterface
pip install setuptools wheel ws4py
python setup.py sdist bdist_wheel
```

## Usage
First start up an Agility Robotics Digit simulation session using the command below
```bash
cd sim
./run_sim.sh
```

Next, open a new terminal and run your Python script.

Check the [examples](examples) folder for usage examples. Check out the official [documentation](https://adubredu.github.io/digitinterface) for more details.