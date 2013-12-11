src ../py2env/bin/activate
python run.py -t 20 $1
eog "$1.png"
