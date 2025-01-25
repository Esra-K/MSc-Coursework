set terminal postscript color solid "Courier" 8
set output "nucmer.ps"
set ytics ( \
 "137795" 1, \
 "137797" 863, \
 "137827" 1847, \
 "137829" 2697, \
 "137892" 3575, \
 "137957" 4275, \
 "137999" 5096, \
 "138021" 6509, \
 "138043" 11082, \
 "138045" 12054, \
 "138059" 13173, \
 "138088" 14374, \
 "138123" 15385, \
 "138127" 16165, \
 "138186" 16857, \
 "138207" 25670, \
 "138208" 28547, \
 "138232" 54154, \
 "138233" 57161, \
 "138236" 65674, \
 "138237" 72381, \
 "138238" 115539, \
 "138239" 120128, \
 "138259" 132521, \
 "138261" 150616, \
 "138262" 158037, \
 "138291" 161695, \
 "138310" 194566, \
 "138330" 202212, \
 "138378" 213030, \
 "138387" 248215, \
 "138388" 279363, \
 "138389" 301862, \
 "" 308837 \
)
set size 1,1
set grid
unset key
set border 10
set tics scale 0
set xlabel "B_anthracis_Mslice"
set ylabel "QRY"
set format "%.0f"
set mouse format "%.0f"
set mouse mouseformat "[%.0f, %.0f]"
set mouse clipboardformat "[%.0f, %.0f]"
set xrange [0:312600]
set yrange [0:312600]
set style line 1  lt 1 lw 2 pt 6 ps 0.5
set style line 2  lt 3 lw 2 pt 6 ps 0.5
set style line 3  lt 2 lw 2 pt 6 ps 0.5
plot \
 "nucmer.fplot" title "FWD" w lp ls 1, \
 "nucmer.rplot" title "REV" w lp ls 2
