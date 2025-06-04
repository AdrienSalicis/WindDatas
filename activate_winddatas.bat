@echo off
chcp 65001 >nul

REM ⚙️ Activer l’environnement conda
call conda activate winddatas

REM 📁 Aller dans le dossier contenant les scripts
cd /d "%~dp0"

echo [✅] Activation terminée.