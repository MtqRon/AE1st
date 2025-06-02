setlocal
set /p day="Enter day>>>"
gcc .\measure.c .\daily_sort\%day%\bubble.c .\daily_sort\%day%\selection.c .\daily_sort\%day%\insertion.c .\daily_sort\%day%\shell.c .\daily_sort\%day%\merge.c .\daily_sort\%day%\heap.c .\daily_sort\%day%\counting.c .\daily_sort\%day%\radix.c -o %day%