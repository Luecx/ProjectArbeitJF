
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './production/svmrKraft.eps'

set title "" 

set xrange [0.95:5]
set yrange [0.99:3]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


set palette grey
set grid
set size square
set view map
set pm3d at b
set pm3d interpolate 2,2
set dgrid3d 50,50,2

set table $DataInterpolated
    splot "svmr.dat" u 1:2:5 
unset table
unset dgrid3d

set format y "%.2f"
set format x "%.2f"



splot $DataInterpolated u 1:2:3 w pm3d palette notitle, \
#      "svmr.txt" u 1:2:5 w p pt 1 lw 2 lc rgb "black" notitle

### end of code
