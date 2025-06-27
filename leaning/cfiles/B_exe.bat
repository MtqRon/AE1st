setlocal
set /p day="Enter day>>>"
gcc .\dayB_measure.c .\daily_sort\%day%\insertion.c .\daily_sort\%day%\shell.c .\daily_sort\%day%\heap.c .\daily_sort\%day%\radix.c .\daily_sort\6-13\bucket.c -o %day%_B
.\%day%_B.exe insertion 40000
.\%day%_B.exe shell 500000
.\%day%_B.exe heap 5000000
.\%day%_B.exe radix 10000000
.\%day%_B.exe bucket 1000000 10000
