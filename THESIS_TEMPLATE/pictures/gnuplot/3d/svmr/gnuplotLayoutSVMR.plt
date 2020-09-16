
### interpolate data with highlighted datapoints
reset session

#set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
#set output './productionNew/svmrAuslenkungAlternativ.eps'

set title "" 

set xrange [1:4.95]
set yrange [0.05:1.99]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


unset key
set view 70,330,1,1
set size square
set palette grey positive gamma 1.5

#plot "SpeedNeu.dat" using 1:2:5 with image
splot "svmrFixed.dat" using 1:2:4 with points pt 5 lc palette

### end of code
