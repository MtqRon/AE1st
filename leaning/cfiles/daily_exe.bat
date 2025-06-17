setlocal
set /p day="Enter day>>>"

gcc .\measure.c .\daily_sort\%day%\bubble.c .\daily_sort\%day%\selection.c .\daily_sort\%day%\insertion.c .\daily_sort\%day%\shell.c .\daily_sort\%day%\merge.c .\daily_sort\%day%\quick.c .\daily_sort\%day%\heap.c .\daily_sort\%day%\bucket.c .\daily_sort\%day%\counting.c .\daily_sort\%day%\radix.c -o %day%

.\%day%.exe bubble 34000
.\%day%.exe selection 40000
.\%day%.exe insertion 59000
.\%day%.exe merge 9300000
.\%day%.exe shell 4900000
.\%day%.exe quick 5000000
.\%day%.exe heap 6700000
.\%day%.exe bucket 10000000 1000000
.\%day%.exe counting 100000000 3000
.\%day%.exe radix 16500000 