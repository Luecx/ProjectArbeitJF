
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './production/XiEtaKraft.eps'

set title "" 

set xrange [0.49:1]
set yrange [0.49:1]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


unset key
set view 80,340,1,1

#set dgrid3d 100,100
set hidden3d
splot "xieta.dat" u 1:2:5 pt 7 lw 1 lc rgb "black" 


### end of code
