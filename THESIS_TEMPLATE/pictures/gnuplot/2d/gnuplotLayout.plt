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

# -----------------------------------------------------------------------------------------------------
set output './production/image1.eps'
set title "Titel" 

set xrange [1:20]
set yrange [0:10]

set xlabel "x-Achse [Einheit]" 
set ylabel "y-Achse [Einheit]" rotate by 90


plot "inputDatei.dat" title "label" with linespoints linestyle 1
# -----------------------------------------------------------------------------------------------------


set output
set terminal pop
