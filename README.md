# Générateur de PNG pour Événements

Script Python automatisant la création de 3 PNG par événement à partir d'un fichier CSV.

## 📁 Structure du projet

```
projet/
├── run_windows.bat        # 🚀 DOUBLE-CLIQUE ICI (Windows)
├── run_mac.sh             # 🚀 DOUBLE-CLIQUE ICI (macOS/Linux)
├── png_generator.py       # Script principal
├── requirements.txt       # Dépendances Python
├── icecream-standard.otf  # Police pour les noms
├── ligurino bold.ttf      # Police pour les infos
├── invite.png             # Image de fond 1920x1080 (transparent)
├── data.csv               # Données des événements
└── export_png/            # Dossier de sortie (créé automatiquement)
```

## 🚀 Installation & Utilisation Rapide

### ⚡ Méthode ONE-CLICK (Recommandée)

#### Windows
1. **Télécharge Python** depuis [python.org](https://www.python.org/downloads/)
   - ⚠️ **IMPORTANT** : Coche "Add Python to PATH" lors de l'installation !
2. **Télécharge ce projet** (ZIP ou Git clone)
3. **Prépare tes fichiers** :
   - Place les polices `icecream-standard.otf` et `ligurino bold.ttf` à la racine
   - Place `invite.png` (1920x1080, transparent) à la racine
   - Crée ton fichier `data.csv`
4. **Double-clique sur `run_windows.bat`** 🎉

Le script s'occupe de tout :
- ✅ Création automatique de l'environnement virtuel
- ✅ Installation des dépendances (Pillow)
- ✅ Génération de tes PNG
- ✅ Ouverture du dossier de résultats

#### macOS / Linux
1. **Télécharge Python 3** (déjà installé sur macOS récent)
2. **Télécharge ce projet** (ZIP ou Git clone)
3. **Prépare tes fichiers** (polices, invite.png, data.csv)
4. **Double-clique sur `run_mac.sh`** 🎉
   - Si ça ne marche pas, ouvre un terminal et exécute : `chmod +x run_mac.sh && ./run_mac.sh`

### 🛠️ Méthode Manuelle (Avancée)

Si tu préfères installer manuellement :

#### 1. Installer Python 3
Télécharge Python depuis [python.org](https://www.python.org/downloads/)

#### 2. Créer un environnement virtuel (optionnel mais recommandé)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 4. Préparer les fichiers
- Place les polices `icecream-standard.otf` et `ligurino bold.ttf` à la racine
- Place `invite.png` (1920x1080, transparent) à la racine
- Crée ton fichier `data.csv`

#### 5. Lancer le script
```bash
# Windows
python png_generator.py

# macOS/Linux
python3 png_generator.py
```

## 📝 Format du CSV

Le fichier `data.csv` doit contenir 7 colonnes séparées par des **tabulations** :

```
QUOI    QUAND    OÙ    NOM    HEURE    DATE_SOURCE    CONTACT
```

### Exemple (copier-coller depuis Google Sheets) :
```
Ceci est un test en une ligne	le 3 mars	Centre Culturel Dinant	Fiorine Guery	9h40	20 février	www.ccdinant.be
Ceci est un test en 2 lignes| Ceci est un test en 2 lignes	le 3, 4, 5 et 31 mars| et aussi en avril	Centre Culturel Dinant et| Centre Culturel Dinant	Amélie Bolen 2	9h40	20 février	www.ccdinant.be et| sur www.ccdinant.be
```

**Astuce** : Copie directement depuis Google Sheets et colle dans un fichier `.csv` - les tabulations seront préservées !

### ✂️ Forcer une coupure en 2 lignes (PNG 3 / QQO)

Pour forcer un texte sur 2 lignes, utilise le **pipe "|"** à l'endroit de la coupure :

```
Courses de caisses à savon|5ème édition
```

**Raccourci clavier sur Mac** : `Option + Shift + L` (AZERTY) ou `Option + 7` (QWERTY)

Si aucun pipe n'est présent, le script détecte automatiquement si le texte doit passer en 2 lignes (pour le PNG 3 / QQO).

## 📤 Résultat

Pour chaque ligne du CSV, le script génère 3 PNG dans `export_png/` :

### 1️⃣ `[nom]_prenom.png`
- Nom encadré dans un cadre rose (RGB: 255, 116, 162)
- Police : Ice Cream, 100px, blanc
- Centré horizontalement, cadre à y=844px
- Marge horizontale : 90px (gauche/droite)
- Marge verticale : 5px (haut/bas)

### 2️⃣ `[nom]_thema.png`
- Fond : invite.png
- Quoi (colonne "QUOI") en bas à droite
- Toujours sur une seule ligne (le `|` est retiré)
- Police : Ligurino, 54px, blanc
- Position : y=972px, aligné à droite (x=1824px)

### 3️⃣ `[nom]_QQO.png`
- 4 informations : Quoi, Où, Quand, Contact
- Police : Ligurino, 68px, blanc
- **Tracking** : 40 (espacement entre caractères)
- **Drop Shadow** :
  - Opacité : 33%
  - Distance : 0px (centré)
  - Spread : 10%
  - Size : 13px
- Gestion automatique des 2 lignes si texte > 1700px
- Positions prédéfinies pour chaque champ

## 🎨 Spécifications techniques

**Dimensions** : 1920x1080px (tous les PNG)  
**Fond** : Transparent (RGBA)  
**Couleur texte** : Blanc (255, 255, 255)  
**Cadre rose** : RGB(255, 116, 162)  
**Effets PNG 3** :
- Tracking (espacement lettres) : 40
- Drop shadow : Opacité 33%, Flou 13px, Distance 0px

## ⚠️ Résolution des problèmes

### Windows : "Python n'est pas reconnu..."
Python n'est pas dans le PATH. Deux solutions :
1. **Réinstalle Python** en cochant "Add Python to PATH"
2. **Ajoute Python manuellement au PATH** :
   - Cherche "Variables d'environnement" dans Windows
   - Dans "Variables système", édite "Path"
   - Ajoute le chemin d'installation de Python (ex: `C:\Users\TON_NOM\AppData\Local\Programs\Python\Python311\`)

### Windows : Le fichier .bat ne fait rien
- Vérifie que Python est installé
- Fais clic droit sur `run_windows.bat` → "Exécuter en tant qu'administrateur"
- Ouvre un terminal et exécute : `run_windows.bat` pour voir les messages d'erreur

### macOS : "Permission denied" sur run_mac.sh
```bash
chmod +x run_mac.sh
./run_mac.sh
```

### "Pillow n'est pas installé"
```bash
pip install -r requirements.txt
```
Ou manuellement :
```bash
pip install Pillow
```

### "Police manquante"
Vérifie que `icecream-standard.otf` et `ligurino bold.ttf` sont bien à la racine du projet

### "invite.png introuvable"
Place l'image `invite.png` (1920x1080, transparent) à la racine

### "data.csv introuvable"
Crée un fichier `data.csv` avec tes données

### Les accents ne s'affichent pas correctement
Le fichier CSV doit être encodé en UTF-8. Dans Excel/LibreOffice, choisis "UTF-8" lors de la sauvegarde.

## 📋 Exemple complet

### Workflow rapide (Windows) :
1. Copie tes lignes depuis Google Sheets
2. Colle-les dans `data.csv` (sauvegarde avec CTRL+S)
3. **Double-clique sur `run_windows.bat`** 🚀
4. Récupère tes PNG dans `export_png/`

### Workflow rapide (macOS/Linux) :
1. Copie tes lignes depuis Google Sheets
2. Colle-les dans `data.csv` (sauvegarde avec CMD+S)
3. **Double-clique sur `run_mac.sh`** 🚀
4. Récupère tes PNG dans `export_png/`

### Workflow manuel :
1. Copie tes lignes depuis Google Sheets
2. Colle-les dans `data.csv` (sauvegarde)
3. Lance `python png_generator.py` (ou `python3 png_generator.py`)
4. Récupère tes PNG dans `export_png/`

**C'est tout !** 🎉

## 🔧 Personnalisation

Tu peux modifier les constantes en haut du script :

### Positions Y (PNG 3 - Alignement avec les labels)
Si les textes ne s'alignent pas parfaitement avec les labels "Quoi", "Quand", "Où", "Infos", ajuste ces valeurs :

```python
Y_POSITIONS = {
    'quoi': {'1_ligne': 270, '2_lignes': 245},
    'quand': {'1_ligne': 420, '2_lignes': 395},
    'ou': {'1_ligne': 570, '2_lignes': 545},
    'contact': {'1_ligne': 720, '2_lignes': 695}
}
```

**Comment ajuster** :
- Augmente la valeur pour descendre le texte
- Diminue la valeur pour monter le texte
- Ajuste séparément pour 1 ligne et 2 lignes

### Autres paramètres modifiables :
- Tailles de police
- Couleurs
- Marges
- Position du cadre rose

### Effets de texte (PNG 3) :
```python
TRACKING = 40  # Espacement entre caractères (0 = normal, 40 = plus espacé)
SHADOW_OPACITY = 0.33  # Opacité de l'ombre (0.0 à 1.0)
SHADOW_BLUR_SIZE = 13  # Taille du flou de l'ombre en pixels
```

**Note** : Le tracking de 40 correspond au tracking de Photoshop (40/1000 em)

---

**Support** : En cas de problème, vérifie que tous les fichiers sont au bon endroit et que Pillow est installé.
