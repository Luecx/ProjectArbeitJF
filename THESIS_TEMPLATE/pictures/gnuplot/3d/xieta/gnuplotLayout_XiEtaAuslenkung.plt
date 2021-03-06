
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './productionNew/XiEtaAuslenkung.eps'

set title "" 
set xrange [0.5:0.99]
set yrange [0.5:0.99]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


set palette grey
set size square
set view map
set pm3d at b
set pm3d interpolate 1,1
set dgrid3d 100,100,2

set table $DataInterpolated
    splot "xieta.dat" u 1:2:4 
unset table
unset dgrid3d

set format y "%.2f"
set format x "%.2f"



splot $DataInterpolated u 1:2:3 w pm3d palette notitle, \
#      "xieta.txt" u 1:2:4 w p pt 1 lw 2 lc rgb "black" notitle

### end of code
