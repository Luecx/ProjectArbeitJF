
### interpolate data with highlighted datapoints
reset session

#set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
#set output './production/svmrAuslenkungAlternativ.eps'

set title "" 

set xrange [1:4.95]
set yrange [0.05:1.99]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


unset key
set size square
set palette grey positive gamma 1.5

#plot "SpeedNeu.dat" using 1:2:5 with image
plot "svmr.dat" using 1:2:4 with points pt 5 lc palette

### end of code
