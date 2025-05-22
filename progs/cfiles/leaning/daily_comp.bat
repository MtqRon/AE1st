setlocal
set /p day="Enter day>>>"
gcc .\measure.c .\daily_sort\%day%\bubble.c .\daily_sort\%day%\insertion.c .\daily_sort\%day%\shell.c .\daily_sort\%day%\merge.c .\daily_sort\%day%\heap.c .\daily_sort\%day%\counting.c -o %day%