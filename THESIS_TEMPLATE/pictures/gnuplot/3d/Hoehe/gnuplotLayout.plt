
### interpolate data with highlighted datapoints
reset session

set terminal postscript eps enhanced color font 'Helvetica,10'

# ---------------------------------------------------------------------------------------
set output './production/Auslenkungsfakt.eps'

#set title "Titel" 

#set xrange [0.9:3.1]
#set yrange [0.9:3.1]

#set xlabel "x-Achse [Einheit]" 
#set ylabel "y-Achse [Einheit]" rotate by 90

# ---------------------------------------------------------------------------------------

set xtics font "Times New Roman,25" ("Hoehe" 0.25, "Geschwindigkeit" 1.75, "Radius" 3.25,)
set ytics font ",25"
set style line 1 lc rgb "black"
set style line 2 lc rgb "grey"

set key right font "Times New Roman,40"
set boxwidth 0.5
set style fill solid

plot 'Auslenkungsfakt.dat'  every 2    using 1:2 title "" with boxes ls 1,\
     'Auslenkungsfakt.dat'  every 2::1 using 1:2 title "" with boxes ls 2

### end of code
