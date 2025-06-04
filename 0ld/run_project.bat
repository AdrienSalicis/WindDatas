@echo off
REM === WindDatas Launcher ===

REM === Initialisation Conda (important si lancé en dehors d'Anaconda Prompt) ===
CALL "%USERPROFILE%\anaconda3\Scripts\activate.bat"

REM === Activation de l'environnement ===
CALL conda activate winddatas

REM === Aller dans le dossier du script (ce fichier .bat) ===
cd /d "%~dp0"
echo [📁] Répertoire courant : %cd%

REM === Exécuter le script principal ===
echo [🚀] Exécution de script.py...
python "script.py"

echo.
pause
