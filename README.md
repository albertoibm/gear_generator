#Gear generator#
written in Python

It uses pygame to display and animate the creation of the gear

Example:

    python generador.py -n 10 -d 100 -a -o

It generates a gear with 10 teeth, 100 units diameter, animates it and prints out the list of points.

There is a file named angle.py included which prints the angle of a given x,y point. In case you need the list of points of the gear in order.

To sort them up just use the next line

    python generador.py -n N -p P -t -o | python angle.py | sort | awk -F ' ' '{print $2}'
