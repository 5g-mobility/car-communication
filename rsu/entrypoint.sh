#!/bin/bash

source venv/bin/activate

for ((i=8000; i < 8010; i++))
do
    python rsu.py --port "$i" &
done