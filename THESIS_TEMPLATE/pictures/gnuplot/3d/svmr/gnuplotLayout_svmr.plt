
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './productionNew/svmr.eps'

set title "" 

set xrange [1:2.45]
set yrange [0.05:2.45]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


set palette grey
set grid
set size square
set view map
set pm3d at b
set pm3d interpolate 1,1
set dgrid3d 50,50,2

set table $DataInterpolated
    splot "svmr.dat" u 1:2:3 
unset table
unset dgrid3d

set format y "%.2f"
set format x "%.2f"



splot $DataInterpolated u 1:2:3 w pm3d palette notitle, \
#      "svmr.dat" u 1:2:3 w p pt 1 lw 2 lc rgb "black" notitle

### end of code
