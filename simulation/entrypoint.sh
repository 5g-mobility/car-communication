#!/bin/bash

export SUMO_HOME="/opt/sumo"
. venv/bin/activate
python3.8 -m pip install -r requirements.txt
python3.8 simulation.py
