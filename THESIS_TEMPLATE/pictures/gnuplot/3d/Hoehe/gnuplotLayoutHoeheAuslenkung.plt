
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './production/Auslenkungsfakt.eps'

set title "" 

#set xrange []
#set yrange []

set xlabel "" 
set ylabel "" rotate by 90

# ---------------------------------------------------------------------------------------


set xtics ("Hoehe" 0.25, "Geschwindigkeit" 1.75, "Radius" 3.25,) font "TimesNewRoman,30"
set ytics font ",25"

set palette grey
unset key
#set key font "TimesNewRoman,45"
set boxwidth 0.5
set style fill solid

plot 'Auslenkungsfakt.dat' every 2    using 1:2 title "Mr_m_i_n" with boxes ls 1 lc rgb "black",\
     'Auslenkungsfakt.dat' every 2::1 using 1:2 title "Mr_m_a_x" with boxes ls 2 lc rgb "grey"

#set palette grey
#set grid
#set size square
#set view map
#set pm3d at b
#set pm3d interpolate 2,2
#set dgrid3d 50,50,2
unset key
#set table $DataInterpolated
 #   splot "HoeheAuslenkung.dat" u 1:2:3 
#unset table
#unset dgrid3d

#set format y "%.1f"
#set format x "%.1f"

#set view 70,340,1,1

#set dgrid3d 30,30
#set hidden3d
#splot "HoeheAuslenkung.dat" u 1:2:3 with lines lc rgb "black"

#splot "HoeheAuslenkung.dat" matrix with pm3d, "HoeheAuslenkung.dat" matrix with lines linewidth 0.1 linecolor rgb "black"

#splot $DataInterpolated u 1:2:3 w pm3d palette notitle, \
#      "HoeheAuslenkung.dat" u 1:2:3 w p pt 1 lw 2 lc rgb "black" notitle

### end of code
