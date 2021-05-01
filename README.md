
# car-communication

## How to install

Make sure you are running Python 3.8 or higher

1. Create a virtual environment (venv)

```bash

python3 -m venv venv

```

  

2. Activate the virtual environment (you need to repeat this step, and this step only, every time you start a new terminal/session):

```bash

source venv/bin/activate

```

  

3. Install the game requirements:

```bash

pip install -r requirements.txt

```

## How to run the application

First, you need to have sumo installed on your computer. Follow the [link](https://sumo.dlr.de/docs/Downloads.php#linux_binaries), if sumo isn't already installed.

1. Run the Road Side Unit (RSU) program

```bash

python rsu.py

```

2. Run the simulation program

```bash

python simulation.py

```
