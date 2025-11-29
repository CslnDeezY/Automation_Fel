@echo off
set EXCEL_FILE=%1
set LUNA=%2
set AN=%3
set OUTPUT_FOLDER=%4

REM 1. Activare mediu virtual
call .venv\Scripts\activate

REM 2. Rulare script Python cu argumentele primite
python Import.py "%EXCEL_FILE%" "%LUNA%" "%AN%" "%OUTPUT_FOLDER%"

REM 3. Păstrează fereastra deschisă după execuție pentru a vedea rezultatul/erorile
pause

REM 4. Dezactivare (opțional, dar recomandat)
deactivate