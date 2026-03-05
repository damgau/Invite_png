@echo off
REM ============================================================
REM   Générateur de PNG pour Événements - Launcher Windows
REM ============================================================
REM
REM   Double-cliquez sur ce fichier pour générer vos PNG !
REM
REM ============================================================

echo.
echo ============================================================
echo   GENERATEUR DE PNG POUR EVENEMENTS
echo ============================================================
echo.

REM Change to the script directory (handles spaces in paths)
cd /d "%~dp0"

REM Check if Python is installed
echo [1/5] Verification de l'installation de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH.
    echo.
    echo Telechargez Python depuis : https://www.python.org/downloads/
    echo IMPORTANT : Cochez "Add Python to PATH" lors de l'installation !
    echo.
    pause
    exit /b 1
)
python --version
echo.

REM Check if virtual environment exists, create if needed
if not exist ".venv" (
    echo [2/5] Creation de l'environnement virtuel...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer l'environnement virtuel.
        pause
        exit /b 1
    )
    echo Environnement virtuel cree avec succes.
) else (
    echo [2/5] Environnement virtuel deja present.
)
echo.

REM Activate virtual environment
echo [3/5] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel.
    pause
    exit /b 1
)
echo.

REM Install/upgrade dependencies
echo [4/5] Installation des dependances...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERREUR] Impossible d'installer les dependances.
    pause
    exit /b 1
)
echo Dependances installees.
echo.

REM Run the PNG generator
echo [5/5] Generation des PNG...
echo.
python png_generator.py
set SCRIPT_EXIT_CODE=%errorlevel%
echo.

REM Show results
if %SCRIPT_EXIT_CODE% equ 0 (
    echo ============================================================
    echo   GENERATION TERMINEE AVEC SUCCES !
    echo ============================================================
    echo.
    echo Vos fichiers PNG sont disponibles dans : export_png\
    echo.
    
    REM Ask if user wants to open the folder
    set /p OPEN_FOLDER="Voulez-vous ouvrir le dossier export_png ? (O/N) : "
    if /i "%OPEN_FOLDER%"=="O" (
        start explorer "export_png"
    )
    if /i "%OPEN_FOLDER%"=="o" (
        start explorer "export_png"
    )
) else (
    echo ============================================================
    echo   ERREUR LORS DE LA GENERATION
    echo ============================================================
    echo.
    echo Verifiez les messages d'erreur ci-dessus.
)

echo.
pause
