
### interpolate data with highlighted datapoints
reset session

#set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
#set output './production/SpeedAuslenkung.eps'

set title "" 

set xrange [100:1000]
set yrange [0.00:2.51]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


unset key
set view 70,340,1,1

#set dgrid3d 100,100
set hidden3d
splot "SpeedNeu.dat" u 1:2:5 pt 7 lw 1 lc rgb "black" 


### end of code
