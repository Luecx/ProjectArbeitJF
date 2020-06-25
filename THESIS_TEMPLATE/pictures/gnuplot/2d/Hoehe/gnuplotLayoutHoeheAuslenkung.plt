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
set output './production/HoeheAuslenkung.eps'
set title "Maximale Auslenkung bei gegebenem h und MR" 

set xrange [0.005:2.55]
set yrange [0.01:1]

set xlabel "MR [cm]" 
set ylabel "Maximale Auslenkung [cm]" rotate by 90


plot "HoeheAuslenkung.dat" u 1:2 title "" with linespoints linestyle 1
	
# -----------------------------------------------------------------------------------------------------


set output
set terminal pop
