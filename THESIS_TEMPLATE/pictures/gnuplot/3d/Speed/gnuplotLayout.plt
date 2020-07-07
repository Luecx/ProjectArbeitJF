
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './production/SpeedKraft.eps'

set title "" 

set xrange [100:1000]
set yrange [0.01:2.50]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


unset key
set palette grey positive gamma 1

#plot "SpeedNeu.dat" using 1:2:5 with image
plot "SpeedNeu.dat" using 1:2:5 with points pt 5 lc palette

### end of code
