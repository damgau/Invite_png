#!/bin/bash
# ============================================================
#   Générateur de PNG pour Événements - Launcher macOS/Linux
# ============================================================
#
#   Double-cliquez sur ce fichier pour générer vos PNG !
#   (ou exécutez : ./run_mac.sh)
#
# ============================================================

echo ""
echo "============================================================"
echo "  GÉNÉRATEUR DE PNG POUR ÉVÉNEMENTS"
echo "============================================================"
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Check if Python 3 is installed
echo "[1/5] Vérification de l'installation de Python..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "[ERREUR] Python 3 n'est pas installé."
    echo ""
    echo "Téléchargez Python depuis : https://www.python.org/downloads/"
    echo "Ou installez avec Homebrew : brew install python3"
    echo ""
    read -p "Appuyez sur Entrée pour continuer..."
    exit 1
fi
python3 --version
echo ""

# Check if virtual environment exists, create if needed
if [ ! -d ".venv" ]; then
    echo "[2/5] Création de l'environnement virtuel..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "[ERREUR] Impossible de créer l'environnement virtuel."
        read -p "Appuyez sur Entrée pour continuer..."
        exit 1
    fi
    echo "Environnement virtuel créé avec succès."
else
    echo "[2/5] Environnement virtuel déjà présent."
fi
echo ""

# Activate virtual environment
echo "[3/5] Activation de l'environnement virtuel..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERREUR] Impossible d'activer l'environnement virtuel."
    read -p "Appuyez sur Entrée pour continuer..."
    exit 1
fi
echo ""

# Install/upgrade dependencies
echo "[4/5] Installation des dépendances..."
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "[ERREUR] Impossible d'installer les dépendances."
    read -p "Appuyez sur Entrée pour continuer..."
    exit 1
fi
echo "Dépendances installées."
echo ""

# Run the PNG generator
echo "[5/5] Génération des PNG..."
echo ""
python png_generator.py
SCRIPT_EXIT_CODE=$?
echo ""

# Show results
if [ $SCRIPT_EXIT_CODE -eq 0 ]; then
    echo "============================================================"
    echo "  GÉNÉRATION TERMINÉE AVEC SUCCÈS !"
    echo "============================================================"
    echo ""
    echo "Vos fichiers PNG sont disponibles dans : export_png/"
    echo ""
    
    # Ask if user wants to open the folder
    read -p "Voulez-vous ouvrir le dossier export_png ? (O/N) : " OPEN_FOLDER
    if [ "$OPEN_FOLDER" = "O" ] || [ "$OPEN_FOLDER" = "o" ]; then
        open export_png
    fi
else
    echo "============================================================"
    echo "  ERREUR LORS DE LA GÉNÉRATION"
    echo "============================================================"
    echo ""
    echo "Vérifiez les messages d'erreur ci-dessus."
fi

echo ""
read -p "Appuyez sur Entrée pour fermer..."
