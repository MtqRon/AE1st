cd "C:\Users\mtqron\Desktop\AE1st"
git pull origin main

git add .
setlocal
set /p commit_mes="Enter comments>>>"
git commit -m "%commit_mes%"
git push -u origin main
pause
```