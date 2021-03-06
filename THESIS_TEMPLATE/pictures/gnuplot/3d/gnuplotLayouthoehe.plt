
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './production/Hoehe.eps'

set title "Schlaganzahl in Abh. von Massenverhaeltnis und Hoehe" 

set xrange [0.5:2.5]
set yrange [0.01:2.5]

set xlabel "Hoehe [cm]" 
set ylabel "Massenverhaeltnis [-]" rotate by 90

# ---------------------------------------------------------------------------------------


set palette grey
set grid
set size square
set view map
set pm3d at b
set pm3d interpolate 2,2
set dgrid3d 300,300,2

set table $DataInterpolated
    splot "Hoehe.dat" u 1:2:3 
unset table
unset dgrid3d

set format y "%.1f"
set format x "%.1f"



splot $DataInterpolated u 1:2:3 w pm3d palette notitle, \
      "inputDatei.dat" u 1:2:3 w p pt 1 lw 2 lc rgb "black" notitle

### end of code
