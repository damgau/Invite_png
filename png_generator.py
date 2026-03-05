#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération automatique de PNG pour événements
Génère 3 PNG par ligne du CSV : prenom.png, prenom_thema.png, prenom_QQO.png
"""

import os
import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Get script directory for relative paths (cross-platform compatibility)
SCRIPT_DIR = Path(__file__).resolve().parent

# Configuration (all paths relative to script directory)
CSV_FILE = SCRIPT_DIR / "data.csv"
OUTPUT_DIR = SCRIPT_DIR / "export_png"
INVITE_PNG = SCRIPT_DIR / "invite.png"
FONT_ICE_CREAM = SCRIPT_DIR / "icecream-standard.otf"
FONT_LIGURINO = SCRIPT_DIR / "ligurino bold.ttf"

# Dimensions
WIDTH = 1920
HEIGHT = 1080

# Couleurs
WHITE = (255, 255, 255, 255)
PINK_FRAME = (255, 116, 162, 245)

# Tailles de police
FONT_SIZE_PNG1 = 70   # Prénom (icecream)
FONT_SIZE_PNG2 = 57    # Thema (ligurino)
FONT_SIZE_PNG3 = 73    # QQO (ligurino)

# Marges et positions
FRAME_MARGIN_X = 90  # Marge horizontale (gauche/droite) du cadre rose
FRAME_MARGIN_Y = 0   # Marge verticale (haut/bas) du cadre rose
FRAME_Y = 890  # Position Y du cadre rose

# Positions pour PNG 3 (QQO)
X_POSITION_QQO = 583
MAX_WIDTH_QQO = 1700  # Largeur maximale avant passage en 2 lignes

# Positions Y pour PNG 3 (alignées avec les labels Quoi/Quand/Où/Infos)
Y_POSITIONS = {
    'quoi': {'1_ligne': 339, '2_lignes': 294},
    'quand': {'1_ligne': 529, '2_lignes': 484},
    'ou': {'1_ligne': 728, '2_lignes': 683},
    'contact': {'1_ligne': 915, '2_lignes': 870}
}

# Position pour PNG 2 (thema)
Y_QUOI_THEMA = 971
X_ALIGN_RIGHT_THEMA = 1824

# Effets pour PNG 3 (drop shadow Photoshop)
SHADOW_OPACITY = 0.85  # 85%
SHADOW_ANGLE = 84  # Degrés
SHADOW_DISTANCE = 5  # px
SHADOW_BLUR_SIZE = 13  # px


def sanitize_filename(name):
    """Nettoie le nom pour créer un nom de fichier valide"""
    # Remplace les espaces et caractères spéciaux
    name = name.strip()
    name = name.replace(' ', '_')
    name = name.replace('/', '_')
    name = name.replace('\\', '_')
    name = name.replace(':', '_')
    return name


def create_shadow_layer(text, font, position, blur_size, opacity, angle, distance):
    """
    Crée une couche d'ombre avec flou, opacité, angle et distance
    """
    import math
    
    # Calculer l'offset de l'ombre basé sur l'angle et la distance
    angle_rad = math.radians(angle)
    offset_x = distance * math.cos(angle_rad)
    offset_y = distance * math.sin(angle_rad)
    
    # Créer une image temporaire pour l'ombre
    shadow_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    
    # Couleur de l'ombre (noir avec opacité)
    shadow_alpha = int(255 * opacity)
    shadow_color = (0, 0, 0, shadow_alpha)
    
    # Position de l'ombre avec offset
    shadow_x = position[0] + offset_x
    shadow_y = position[1] + offset_y
    
    # Dessiner le texte de l'ombre
    shadow_draw.text((shadow_x, shadow_y), text, font=font, fill=shadow_color)
    
    # Appliquer le flou gaussien
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=blur_size))
    
    return shadow_img


def split_text_if_needed(text, font, max_width):
    """
    Divise le texte en 2 lignes si nécessaire
    Retourne (lignes, is_2_lignes)
    
    Si le texte contient un pipe "|", il sera forcé en 2 lignes à cet endroit.
    Sinon, le texte est mesuré et coupé automatiquement si trop long.
    """
    # Vérifier si un pipe "|" est présent pour forcer la coupure
    if '|' in text:
        parts = text.split('|', 1)  # Couper au premier pipe seulement
        return [parts[0].strip(), parts[1].strip()], True
    
    # Mesurer le texte
    draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    if text_width <= max_width:
        return [text], False
    
    # Diviser le texte en 2 lignes automatiquement
    words = text.split()
    if len(words) == 1:
        # Un seul mot trop long, on le coupe au milieu
        mid = len(text) // 2
        return [text[:mid] + '-', text[mid:]], True
    
    # Trouver le meilleur point de coupe
    mid = len(words) // 2
    line1 = ' '.join(words[:mid])
    line2 = ' '.join(words[mid:])
    
    return [line1, line2], True


# def create_png_1_prenom(nom, output_path):
#     """
#     Crée le PNG 1 : prénom.png
#     Nom encadré dans un cadre rose
#     """
#     img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
#     draw = ImageDraw.Draw(img)
    
#     # Charger la police
#     font = ImageFont.truetype(FONT_ICE_CREAM, FONT_SIZE_PNG1)

    
#     # Mesurer le texte
#     bbox = draw.textbbox((0, 0), nom, font=font)
#     text_width = bbox[2] - bbox[0]
#     text_height = bbox[3] - bbox[1]
    
#     # Dimensions du cadre (largeur dynamique, hauteur fixe à 157px)
#     frame_width = text_width + 2 * FRAME_MARGIN_X
#     frame_height = 152
    
#     # Position X centrée
#     frame_x = (WIDTH - frame_width) // 2
    
#     # Dessiner le cadre rose
#     draw.rectangle(
#         [frame_x, FRAME_Y, frame_x + frame_width, FRAME_Y + frame_height],
#         fill=PINK_FRAME
#     )
    
#     # Position du texte (centré dans le cadre)
#     text_x = frame_x + FRAME_MARGIN_X
#     text_y = FRAME_Y + (frame_height - text_height) // 2 - bbox[1]
    
#     # Dessiner le texte
#     draw.text((text_x, text_y), nom, font=font, fill=WHITE)
    
#     img.save(output_path)
#     print(f"✓ Créé : {output_path}")
def create_png_1_prenom(nom, output_path):
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Police à 66% (66% de 100)
    font = ImageFont.truetype(str(FONT_ICE_CREAM), FONT_SIZE_PNG1)
    
    bbox = draw.textbbox((0, 0), nom, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Cadre à 66% : marge horizontale 59px (66% de 90), hauteur 100px (66% de 152)
    frame_margin_x = 59
    frame_height = 82
    frame_width = text_width + 2 * frame_margin_x
    frame_x = (WIDTH - frame_width) // 2
    
    draw.rectangle(
        [frame_x, FRAME_Y, frame_x + frame_width, FRAME_Y + frame_height],
        fill=PINK_FRAME
    )
    
    text_x = frame_x + frame_margin_x
    text_y = FRAME_Y + (frame_height - text_height) // 2 - bbox[1]
    
    draw.text((text_x, text_y), nom, font=font, fill=WHITE)
    
    img.save(output_path)
    print(f"✓ Créé : {output_path}")

def create_png_2_thema(quoi, nom, output_path):
    """
    Crée le PNG 2 : prénom_thema.png
    Logo invite.png + quoi en bas à droite
    """
    # Charger l'image de fond
    if not INVITE_PNG.exists():
        print(f"⚠ Erreur : {INVITE_PNG} introuvable")
        return
    
    img = Image.open(str(INVITE_PNG)).convert('RGBA')
    
    # Vérifier les dimensions
    if img.size != (WIDTH, HEIGHT):
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(img)
    
    # Charger la police
    font = ImageFont.truetype(str(FONT_LIGURINO), FONT_SIZE_PNG2)
    
    # PNG thema: toujours sur une seule ligne, sans pipe "|"
    quoi_clean = quoi.replace('|', ' ').strip()

    # Mesurer le texte final pour un alignement droit stable
    bbox = draw.textbbox((0, 0), quoi_clean, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = X_ALIGN_RIGHT_THEMA - text_width

    # Dessiner le texte en une seule ligne
    draw.text((text_x, Y_QUOI_THEMA), quoi_clean, font=font, fill=WHITE)
    
    img.save(output_path)
    print(f"✓ Créé : {output_path}")


def create_png_3_qqo(quoi, ou, quand, contact, nom, output_path):
    """
    Crée le PNG 3 : prénom_QQO.png
    Infos complètes avec gestion automatique des 2 lignes
    Avec tracking et drop shadow
    """
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    
    # Charger la police
    font = ImageFont.truetype(str(FONT_LIGURINO), FONT_SIZE_PNG3)
    
    # Données à afficher
    data = {
        'quoi': quoi,
        'quand': quand,
        'ou': ou,
        'contact': contact
    }
    
    # Traiter chaque champ
    for key, text in data.items():
        lines, is_2_lignes = split_text_if_needed(text, font, MAX_WIDTH_QQO)
        
        if is_2_lignes:
            y_pos = Y_POSITIONS[key]['2_lignes']
        else:
            y_pos = Y_POSITIONS[key]['1_ligne']
        
        # Dessiner chaque ligne avec ombre
        for i, line in enumerate(lines):
            current_y = y_pos + i * 70
            position = (X_POSITION_QQO, current_y)
            
            # Créer et appliquer l'ombre
            shadow = create_shadow_layer(line, font, position, SHADOW_BLUR_SIZE, SHADOW_OPACITY, SHADOW_ANGLE, SHADOW_DISTANCE)
            img = Image.alpha_composite(img, shadow)
            
            # IMPORTANT: Recréer draw après alpha_composite
            draw = ImageDraw.Draw(img)
            
            # Dessiner le texte
            draw.text(position, line, font=font, fill=WHITE)
    
    img.save(output_path)
    print(f"✓ Créé : {output_path}")


def process_csv():
    """
    Lit le CSV et génère tous les PNG
    """
    # Créer le dossier de sortie
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if not CSV_FILE.exists():
        print(f"⚠ Erreur : {CSV_FILE.name} introuvable")
        print(f"Créez un fichier {CSV_FILE.name} avec vos données.")
        return
    
    # Lire le CSV (avec tabulations comme séparateur)
    with open(str(CSV_FILE), 'r', encoding='utf-8') as f:
        # Détecter le séparateur (tab ou virgule)
        sample = f.read(1024)
        f.seek(0)
        
        if '\t' in sample:
            reader = csv.reader(f, delimiter='\t')
        else:
            reader = csv.reader(f)
        
        count = 0
        for row in reader:
            if len(row) < 7:
                print(f"⚠ Ligne ignorée (pas assez de colonnes) : {row}")
                continue
            
            quoi, quand, ou, nom, contact = row[0], row[1], row[2], row[3], row[6]
            
            # Nettoyer le nom pour les fichiers
            clean_name = sanitize_filename(nom)
            
            print(f"\n📝 Traitement : {nom}")
            
            # Générer les 3 PNG
            create_png_1_prenom(
                nom, 
                str(OUTPUT_DIR / f"{clean_name}.png")
            )
            
            create_png_2_thema(
                quoi, 
                nom,
                str(OUTPUT_DIR / f"{clean_name}_thema.png")
            )
            
            create_png_3_qqo(
                quoi, 
                ou, 
                quand, 
                contact, 
                nom,
                str(OUTPUT_DIR / f"{clean_name}_QQO.png")
            )
            
            count += 1
        
        print(f"\n✅ Terminé ! {count * 3} PNG générés dans {OUTPUT_DIR.name}/")


if __name__ == "__main__":
    print("=" * 60)
    print("  GÉNÉRATEUR DE PNG POUR ÉVÉNEMENTS")
    print("=" * 60)
    
    # Vérifier les dépendances
    try:
        import PIL
    except ImportError:
        print("⚠ Pillow n'est pas installé.")
        print("Installez-le avec : pip install Pillow")
        exit(1)
    
    # Vérifier les ressources critiques (fail-fast)
    missing_resources = []

    for resource in [FONT_ICE_CREAM, FONT_LIGURINO, INVITE_PNG]:
        if not resource.exists():
            missing_resources.append(resource.name)

    if missing_resources:
        print("⚠ Ressources manquantes :")
        for resource in missing_resources:
            print(f"  - {resource}")
        exit(1)
    
    # Lancer le traitement
    process_csv()