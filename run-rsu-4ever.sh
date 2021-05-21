
python rsu.py --port 10000

while [ $? -ne 0 ]
do

echo "Here we go again $?"
python rsu.py --port 10000

done

echo "Exit with code $?"