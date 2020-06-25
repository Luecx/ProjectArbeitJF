# 2D Plotten von Punkten

set terminal postscript eps enhanced color font 'Helvetica,10'

set size square
set grid

set format y "%g"
set format x "%.2f"


set style line 1 \
    linecolor rgb '#222222' \
    linetype 1 linewidth 3 \
    pointtype 7 pointsize 1.5

set style line 2 \
    linecolor rgb '#222222' \
    linetype 1 linewidth 3 \
    pointtype 6 pointsize 1.5

# -----------------------------------------------------------------------------------------------------
set output './production/Hoehe_Massenratio.eps'
set title "Massenverhaeltnis bei variierter Hoehe" 

set xrange [0.3:1.7]
set yrange [0.01:0.1]

set xlabel "Hoehe [cm]" 
set ylabel "Massenratio [-]" rotate by 90


plot "Hoehe.dat" u 1:2 title "Uebergang Einzel- zu Doppelschlag" with linespoints linestyle 1, \
	"Hoehe.dat" u 1:3 title "Uebergang Doppel- zu Mehrfachschlag" with linespoints linestyle 2  
	
# -----------------------------------------------------------------------------------------------------


set output
set terminal pop
