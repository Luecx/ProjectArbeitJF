
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './production/HoeheKraft.eps'

set title "Hoehe und maximale Kraft" 

set xrange [0.4:2.6]
set yrange [0.01:2.51]

set xlabel "Hoehe [cm]" 
set ylabel "MR [-]" rotate by 90

# ---------------------------------------------------------------------------------------


set palette grey
set grid
set size square
set view map
set pm3d at b
set pm3d interpolate 2,2
set dgrid3d 50,50,2

set table $DataInterpolated
    splot "HoeheKraft.dat" u 1:2:3 
unset table
unset dgrid3d

set format y "%.1f"
set format x "%.1f"



splot $DataInterpolated u 1:2:3 w pm3d palette notitle, \
      "HoeheKraft.dat" u 1:2:3 w p pt 1 lw 2 lc rgb "black" notitle

### end of code
