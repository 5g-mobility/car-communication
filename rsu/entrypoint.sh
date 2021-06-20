#!/bin/bash

. venv/bin/activate
python3.8 -m pip install -r requirements.txt
python3.8 rsu.py --port 8000