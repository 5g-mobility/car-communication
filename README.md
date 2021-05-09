
# Cars Simulation with _Sumo_

Simulation of the movement of cars in the Costa Nova and Barra area using _Sumo_ and _Python_ to simulate all the data flow in a real situation: `Car -> RSU -> Broker` and ` Broker-> RSU-Car`

After running, the data will eventually be available at the _MQTT Broker_ `broker.es.av.it.pt` in the topic `its_center/inqueue/5g-mobility`

The data generated includes:
- Timestamp of the event
- Vehicle Id
- Position of the vehicle
- Vehicle speed
- Vehicle emissions
- Temperature outside according to vehicle sensors
- Light capture indication according to the vehicle's sensors
- Rain indication according to vehicle sensors
- Indication of the existence of fog according to the sensors of the vehicle

## Run on _Docker_

1. Build the _Docker_ image

```bash

docker-compose build

```

2. Run the simulation

```bash

docker-compose up -d

```

## Run on your environment

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

### How to run the application

First, you need to have sumo installed on your computer. Follow the [link](https://sumo.dlr.de/docs/Downloads.php#linux_binaries), if sumo isn't already installed.

1. Run the Road Side Unit (RSU) program

```bash

python rsu.py

```

2. Run the simulation program

```bash

python simulation.py

```
