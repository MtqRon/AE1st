setlocal
set /p day="Enter day>>>"
gcc .\dayA_measure.c .\daily_sort\%day%\bubble.c .\daily_sort\%day%\selection.c .\daily_sort\%day%\merge.c .\daily_sort\%day%\counting.c .\daily_sort\%day%\quick.c -o %day%
.\%day%.exe bubble 34000
.\%day%.exe selection 40000
.\%day%.exe merge 9300000
.\%day%.exe quick 5000000
.\%day%.exe counting 100000000 3000