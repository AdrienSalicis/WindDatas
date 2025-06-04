@echo off
chcp 65001 > nul
echo [🔧] Initialisation du projet météo...

REM Crée l’environnement si nécessaire
IF NOT EXIST "venv\" (
    echo [🧪] Création de l'environnement virtuel...
    python -m venv "venv"
)

REM Active l’environnement
call "venv\Scripts\activate.bat"

REM Installation des dépendances
IF EXIST "requirements.txt" (
    echo [📦] Installation des dépendances...
    pip install -r "requirements.txt"
) ELSE (
    echo [⚠️] requirements.txt non trouvé.
)

REM Exécution du script principal
echo [🚀] Lancement du script script.py...
python "test_api_noaa.py"

REM Ouvre un shell pour continuer à travailler
cmd /k
