
### interpolate data with highlighted datapoints
reset session

#set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
#set output './production/image1.eps'

set title "Titel" 

set xrange [0.9:3.1]
set yrange [0.9:3.1]

set xlabel "x-Achse [Einheit]" 
set ylabel "y-Achse [Einheit]" rotate by 90

# ---------------------------------------------------------------------------------------


set palette grey
set grid
set size square
set view map
set pm3d at b
set pm3d interpolate 2,2
set dgrid3d 50,50,2

set table $DataInterpolated
    splot "inputDatei.dat" u 1:2:3 
unset table
unset dgrid3d

set format y "%.1f"
set format x "%.1f"



splot $DataInterpolated u 1:2:3 w pm3d palette notitle, \
      "inputDatei.dat" u 1:2:3 w p pt 1 lw 2 lc rgb "black" notitle

### end of code
