
### interpolate data with highlighted datapoints
reset session

#set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
#set output './production/SpeedKraft.eps'

set title "" 

set xrange [100:1000]
set yrange [0.49:2.51]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


unset key
set view 70,250,1,1

#set dgrid3d 100,100
set hidden3d
splot "SpeedKraft.dat" u 1:2:3 pt 7 lw 1 lc rgb "black" 


### end of code
