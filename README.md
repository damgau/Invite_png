# Générateur de PNG pour Événements

Script Python automatisant la création de 3 PNG par événement à partir d'un fichier CSV.

## 📁 Structure du projet

```
projet/
├── png_generator.py       # Script principal
├── icecream-standard.otf  # Police pour les noms
├── ligurino bold.ttf      # Police pour les infos
├── invite.png             # Image de fond 1920x1080 (transparent)
├── data.csv               # Données des événements
└── export_png/            # Dossier de sortie (créé automatiquement)
```

## 🚀 Installation

### 1. Installer Python 3
Si ce n'est pas déjà fait, télécharge Python depuis [python.org](https://www.python.org/downloads/)

### 2. Installer Pillow
Ouvre un terminal et exécute :
```bash
pip install Pillow
```

### 3. Préparer les fichiers
- Place les polices `icecream-standard.otf` et `ligurino bold.ttf` à la racine
- Place `invite.png` (1920x1080, transparent) à la racine
- Crée ton fichier `data.csv`

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

## ▶️ Utilisation

### Méthode 1 : Double-clic (Windows)
Double-clique sur `png_generator.py`

### Méthode 2 : Terminal
```bash
python png_generator.py
```

### Méthode 3 : Ligne de commande (Linux/Mac)
```bash
python3 png_generator.py
```

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

### "Pillow n'est pas installé"
```bash
pip install Pillow
```

### "Police manquante"
Vérifie que `icecream-standard.otf` et `ligurino bold.ttf` sont bien à la racine du projet

### "invite.png introuvable"
Place l'image `invite.png` (1920x1080, transparent) à la racine

### "data.csv introuvable"
Crée un fichier `data.csv` avec tes données

## 📋 Exemple complet

1. Copie tes lignes depuis Google Sheets
2. Colle-les dans `data.csv` (sauvegarde)
3. Lance `python png_generator.py`
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
