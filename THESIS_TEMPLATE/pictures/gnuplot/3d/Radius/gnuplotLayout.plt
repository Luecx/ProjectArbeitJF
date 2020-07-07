
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './production/Radius.eps'

set title "" 

set xrange [0.5:10]
set yrange [0.01:2.50]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


unset key
set size square
set palette grey positive gamma 1

#plot "SpeedNeu.dat" using 1:2:5 with image
plot "Radius.dat" using 1:2:3 with points pt 5 lc palette


### end of code
