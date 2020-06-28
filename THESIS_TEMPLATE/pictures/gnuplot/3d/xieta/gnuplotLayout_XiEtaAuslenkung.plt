
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './production/XiEtaAuslenkung.eps'

set title "" 

set xrange [0.5:0.99]
set yrange [0.5:0.99]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


unset key
set view 55,330,1,1

set dgrid3d 30,30
set hidden3d
splot "xieta.dat" u 1:2:4 with lines lc rgb "black"


### end of code
