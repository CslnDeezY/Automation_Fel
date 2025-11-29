@echo off
REM Utilizare:
REM run_windows.bat "fisier_excel.xlsx" "Luna" "arhiva.zip"

setlocal enabledelayedexpansion

set "EXCEL=%~1"
set "LUNA=%~2"
set "ARHIVA=%~3"

if "%EXCEL%"=="" (
  echo Utilizare: run_windows.bat "fisier_excel" "luna" "arhiva.zip"
  exit /b 1
)
if "%LUNA%"=="" (
  echo Utilizare:
  echo   run_windows.bat "fisier_excel" "luna" "arhiva.zip"
  exit /b 1
)
if "%ARHIVA%"=="" (
  echo Utilizare:
  echo   run_windows.bat "fisier_excel" "luna" "arhiva.zip"
  exit /b 1
)

REM =============================
REM Folder output = folderul arhivei
REM =============================

REM Ia drive+path din parametrul 3 (are backslash final)
set "OUTPUT_FOLDER=%~dp3"

REM Normalizare sigură: folosim FOR cu un '.' adițional ca să evităm problema backslash+ghilimele
for %%A in ("%OUTPUT_FOLDER%.") do set "OUTPUT_FOLDER=%%~fA"
REM Dacă s-a păstrat un '.' final, îl eliminăm
if "%OUTPUT_FOLDER:~-1%"=="." set "OUTPUT_FOLDER=%OUTPUT_FOLDER:~0,-1%"

echo OUTPUT_FOLDER = "%OUTPUT_FOLDER%"
echo Folder output: "%OUTPUT_FOLDER%"

REM =============================
REM Activare mediu virtual
REM =============================
if exist ".venv\Scripts\activate.bat" (
  call .venv\Scripts\activate
)

REM =============================
REM 1) Ruleaza Import.py
REM =============================
echo.
echo === Rulare Import.py ===
python Import.py "%EXCEL%" "%LUNA%" "%OUTPUT_FOLDER%"
if errorlevel 1 (
  echo Eroare la rularea Import.py
  pause
  goto cleanup
)

REM =============================
REM 2) Gasim fisierul text generat
REM =============================

set "TXT_FILE="

for %%F in ("%OUTPUT_FOLDER%\\onomastici_%LUNA%_*.txt") do (
  set "TXT_FILE=%%~fF"
)

if "%TXT_FILE%"=="" (
  echo Eroare: nu am gasit fisierul generat in "%OUTPUT_FOLDER%".
  pause
  goto cleanup
)

echo Fisier text gasit: "%TXT_FILE%"

REM =============================
REM 3) Rulare RenameImages.py
REM =============================
echo.
echo === Rulare RenameImages.py ===
python RenameImages.py "%ARHIVA%" "%TXT_FILE%"
if errorlevel 1 (
  echo Eroare la rularea RenameImages.py
  pause
  goto cleanup
)

REM =============================
REM 4) Stergere fisier text
REM =============================
echo Stergere fisier text: "%TXT_FILE%"
del /f /q "%TXT_FILE%"

echo.
echo === Finalizat cu succes! ===
pause

:cleanup
if defined VIRTUAL_ENV (
  deactivate 2>nul
)

endlocal
