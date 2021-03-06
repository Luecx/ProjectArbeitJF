
### interpolate data with highlighted datapoints
reset session

#set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
#set output './production/SpeedKraftMesh.eps'

set title "" 

set xrange [100:1000]
set yrange [0.01:2.5]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


unset key
set view 70,330,1,1

set dgrid3d 30,30
set hidden3d
splot "SpeedNeu.dat" u 1:2:3 with lines lc rgb "black"


### end of code
