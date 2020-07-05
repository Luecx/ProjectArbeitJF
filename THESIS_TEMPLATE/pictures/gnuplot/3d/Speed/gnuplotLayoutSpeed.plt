
### interpolate data with highlighted datapoints
reset session

#set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
#set output './production/SpeedKraft.eps'

set title "" 

set xrange [100:1000]
set yrange [0.01:2.5]

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


set palette grey
set grid
set size square
set view map
set pm3d at b
# set pm3d interpolate 2,2
set dgrid3d 1000,1000 qnorm 2
set table $DataInterpolated
    splot "SpeedNeu.dat" u 1:2:3 
unset table
unset dgrid3d

set format y "%.1f"
set format x "%.0f"



splot $DataInterpolated u 1:2:3 w pm3d palette notitle, \
    #  "Speed.dat" u 1:2:3 w p pt 1 lw 2 lc rgb "black" notitle

### end of code
