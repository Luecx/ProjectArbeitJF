splot 'mydata.dat' u 1:2:i+3 with lines
i = i+1
if (i < n) reread