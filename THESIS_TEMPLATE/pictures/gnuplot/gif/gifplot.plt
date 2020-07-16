set term gif animate delay 5
set output "animate.gif"
set yrange [0:50]
set xrange [0:50]
set zrange [-1:1]

n = 500

i = 0

set dgrid3d 25,25,6

load "animate.gnuplot"

set output

