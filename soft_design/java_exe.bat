setlocal
set /p reponame="Enter package name>>>"
cd "C:\Users\NikoHam\Desktop\AE1st\soft_design\%reponame%-Jun13-MtqRon"
javac -d . %reponame%\*.java
set /p class_name="Enter class name>>>"
java %reponame%.%class_name%
if %errorlevel% neq 0 (
    echo Error: Java execution failed.
) else (
    echo Java program executed successfully.
)
endlocal