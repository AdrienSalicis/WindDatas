@echo off
chcp 65001 >nul
title WindDatas Launcher
cls

echo ==========================================
echo   🚀 WindDatas - Initialisation projet
echo ==========================================

REM === Initialisation Conda (pour cmd / PowerShell) ===
CALL "%USERPROFILE%\anaconda3\Scripts\activate.bat"

REM === Vérification existence environnement ===
CALL conda info --envs | findstr "winddatas" >nul
IF ERRORLEVEL 1 (
    echo [❌] L'environnement 'winddatas' n'existe pas.
    pause
    exit /b
)

echo [✅] Environnement 'winddatas' trouvé.

REM === Activation environnement ===
CALL conda activate winddatas

REM === Aller dans le dossier du script ===
cd /d "%~dp0"
echo [📁] Répertoire courant : "%cd%"


REM === Test des imports Python ===
echo [🧪] Vérification des bibliothèques essentielles...
python -c "import numpy, pandas, matplotlib, meteostat, cdsapi, docx, geopy; print('[✅] Tous les modules sont disponibles.')"
IF ERRORLEVEL 1 (
    echo [❌] Un ou plusieurs modules sont manquants ou corrompus.
    pause
    exit /b
)

REM === Demande de confirmation ===
set /p launch=Souhaitez-vous lancer script.py ? (O/N) : 
if /I "%launch%"=="O" (
    echo.
    echo [🚀] Lancement de script.py...
    python script.py
) else (
    echo [⏹️] Lancement annulé.
)

pause
