@echo off
setlocal enabledelayedexpansion

REM ========================
REM 設定：ここを書き換えて保存先フォルダを指定
REM 例:
REM set "TARGET_DIR=C:\Users\you\Documents\notes"
set "TARGET_DIR=C:\Users\MtqRon\Desktop\AE1st\TOEIC\daily_summarize"
REM ========================

REM フォルダがなければ作成
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

REM このバッチと同じ場所の format.md をテンプレとして使用
set "SCRIPT_DIR=%~dp0"
set "TEMPLATE=%SCRIPT_DIR%format.md"

if not exist "%TEMPLATE%" (
    echo [ERROR] format.md が見つかりません: "%TEMPLATE%"
    exit /b 1
)

REM 日付取得（ファイル名用 mm-dd, 中身用 mm/dd）
for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format \"MM-dd\""') do set "TODAY_MM_DD_FILE=%%I"
for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format \"MM/dd\""') do set "TODAY_MM_DD_TEXT=%%I"

REM 新規ファイルパス
set "NEW_FILE=%TARGET_DIR%\%TODAY_MM_DD_FILE%.md"

REM format.md をコピー
copy /Y "%TEMPLATE%" "%NEW_FILE%" >nul

REM %TODAY'S DATE% を mm/dd に置換
powershell -NoProfile -Command "$p='%%' + 'TODAY''S DATE' + '%%'; $f='%NEW_FILE%'; (Get-Content -Raw $f).Replace($p, '%TODAY_MM_DD_TEXT%') | Set-Content -LiteralPath $f"

REM VS Code で開く（code コマンドが使える前提）
code "%NEW_FILE%"

endlocal
