
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './production/SpeedAuslenkung.eps'

set title "Geschwindigkeit in Abhaengigkeit der maximalen Auslenkung" 

set xrange [1:10]
set yrange [0.01:2.5]

set xlabel "Geschwindigkeit [cm/s]" 
set ylabel "MR [-]" rotate by 90

# ---------------------------------------------------------------------------------------


set palette grey
set grid
set size square
set view map
set pm3d at b
set pm3d interpolate 2,2
set dgrid3d 300,300,2

set table $DataInterpolated
    splot "SpeedAuslenkung.dat" u 1:2:3 
unset table
unset dgrid3d

set format y "%.1f"
set format x "%.1f"



splot $DataInterpolated u 1:2:3 w pm3d palette notitle, \
      "SpeedAuslenkung.dat" u 1:2:3 w p pt 1 lw 2 lc rgb "black" notitle

### end of code
