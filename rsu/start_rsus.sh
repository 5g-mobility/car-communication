source venv/bin/activate

for ((i=10000; i < 10010; i++))
do
    python rsu.py --port "$i" &
done