#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération automatique de PNG pour événements
Génère 3 PNG par ligne du CSV : prenom.png, prenom_thema.png, prenom_QQO.png
"""

import os
import csv
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Configuration
CSV_FILE = "data.csv"
OUTPUT_DIR = "export_png"
INVITE_PNG = "invite.png"
FONT_ICE_CREAM = "icecream-standard.otf"
FONT_LIGURINO = "ligurino bold.ttf"

# Dimensions
WIDTH = 1920
HEIGHT = 1080

# Couleurs
WHITE = (255, 255, 255, 255)
PINK_FRAME = (255, 116, 162, 245)

# Tailles de police
FONT_SIZE_PNG1 = 66   # Prénom (icecream)
FONT_SIZE_PNG2 = 60    # Thema (ligurino)
FONT_SIZE_PNG3 = 73    # QQO (ligurino)

# Marges et positions
FRAME_MARGIN_X = 90  # Marge horizontale (gauche/droite) du cadre rose
FRAME_MARGIN_Y = 0   # Marge verticale (haut/bas) du cadre rose
FRAME_Y = 844  # Position Y du cadre rose

# Positions pour PNG 3 (QQO)
X_POSITION_QQO = 583
MAX_WIDTH_QQO = 1700  # Largeur maximale avant passage en 2 lignes

# Positions Y pour PNG 3 (alignées avec les labels Quoi/Quand/Où/Infos)
Y_POSITIONS = {
    'quoi': {'1_ligne': 349, '2_lignes': 300},
    'quand': {'1_ligne': 543, '2_lignes': 493},
    'ou': {'1_ligne': 748, '2_lignes': 693},
    'contact': {'1_ligne': 940, '2_lignes': 879}
}

# Position pour PNG 2 (thema)
Y_QUOI_THEMA = 967
X_ALIGN_RIGHT_THEMA = 1824

# Effets pour PNG 3
TRACKING = 40  # Espacement entre les caractères (comme Photoshop tracking)
SHADOW_OPACITY = 0.80  # %
SHADOW_BLUR_SIZE = 10


def sanitize_filename(name):
    """Nettoie le nom pour créer un nom de fichier valide"""
    # Remplace les espaces et caractères spéciaux
    name = name.strip()
    name = name.replace(' ', '_')
    name = name.replace('/', '_')
    name = name.replace('\\', '_')
    name = name.replace(':', '_')
    return name


def get_text_width_with_tracking(text, font, tracking):
    """
    Calcule la largeur du texte avec tracking
    Le tracking dans Photoshop est en millièmes d'em (1000 = 1em)
    """
    draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    
    # Largeur de base sans tracking
    bbox = draw.textbbox((0, 0), text, font=font)
    base_width = bbox[2] - bbox[0]
    
    # Ajouter le tracking entre les caractères
    # tracking = 40 signifie 40/1000 de la taille de la police
    font_size = font.size
    tracking_px = (tracking / 1000) * font_size
    
    # Nombre d'espaces entre caractères (n-1 pour n caractères)
    num_gaps = len(text) - 1
    total_tracking = tracking_px * num_gaps
    
    return base_width + total_tracking


def draw_text_with_tracking(draw, position, text, font, fill, tracking):
    """
    Dessine du texte avec tracking (espacement entre caractères)
    """
    x, y = position
    font_size = font.size
    tracking_px = (tracking / 1000) * font_size
    
    current_x = x
    for char in text:
        draw.text((current_x, y), char, font=font, fill=fill)
        # Mesurer la largeur du caractère
        bbox = draw.textbbox((0, 0), char, font=font)
        char_width = bbox[2] - bbox[0]
        # Avancer avec le tracking
        current_x += char_width + tracking_px


def create_shadow_layer(text, font, position, tracking, blur_size, opacity):
    """
    Crée une couche d'ombre avec flou et opacité
    """
    # Créer une image temporaire pour l'ombre
    shadow_img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    
    # Couleur de l'ombre (noir avec opacité)
    shadow_alpha = int(255 * opacity)
    shadow_color = (0, 0, 0, shadow_alpha)
    
    # Dessiner le texte avec tracking pour l'ombre
    draw_text_with_tracking(shadow_draw, position, text, font, shadow_color, tracking)
    
    # Appliquer le flou gaussien
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=blur_size))
    
    return shadow_img


def split_text_if_needed(text, font, max_width, tracking):
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
    
    # Mesurer le texte avec tracking
    text_width = get_text_width_with_tracking(text, font, tracking)
    
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
    font = ImageFont.truetype(FONT_ICE_CREAM, FONT_SIZE_PNG1)
    
    bbox = draw.textbbox((0, 0), nom, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Cadre à 66% : marge horizontale 59px (66% de 90), hauteur 100px (66% de 152)
    frame_margin_x = 59
    frame_height = 100
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
    if not os.path.exists(INVITE_PNG):
        print(f"⚠ Erreur : {INVITE_PNG} introuvable")
        return
    
    img = Image.open(INVITE_PNG).convert('RGBA')
    
    # Vérifier les dimensions
    if img.size != (WIDTH, HEIGHT):
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(img)
    
    # Charger la police
    font = ImageFont.truetype(FONT_LIGURINO, FONT_SIZE_PNG2)
    
    # Mesurer le texte
    bbox = draw.textbbox((0, 0), quoi, font=font)
    text_width = bbox[2] - bbox[0]
    
    # Position X (aligné à droite)
    text_x = X_ALIGN_RIGHT_THEMA - text_width
    
    # Dessiner le texte
    quoi_clean = quoi.replace('|', '').strip()
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
    font = ImageFont.truetype(FONT_LIGURINO, FONT_SIZE_PNG3)
    
    # Données à afficher
    data = {
        'quoi': quoi,
        'quand': quand,
        'ou': ou,
        'contact': contact
    }
    
    # Traiter chaque champ
    for key, text in data.items():
        lines, is_2_lignes = split_text_if_needed(text, font, MAX_WIDTH_QQO, TRACKING)
        
        if is_2_lignes:
            y_pos = Y_POSITIONS[key]['2_lignes']
        else:
            y_pos = Y_POSITIONS[key]['1_ligne']
        
        # Dessiner chaque ligne avec ombre et tracking
        for i, line in enumerate(lines):
            current_y = y_pos + i * 70
            position = (X_POSITION_QQO, current_y)
            
            # Créer et appliquer l'ombre
            shadow = create_shadow_layer(line, font, position, TRACKING, SHADOW_BLUR_SIZE, SHADOW_OPACITY)
            img = Image.alpha_composite(img, shadow)
            
            # IMPORTANT: Recréer draw après alpha_composite
            draw = ImageDraw.Draw(img)
            
            # Dessiner le texte avec tracking
            draw_text_with_tracking(draw, position, line, font, WHITE, TRACKING)
    
    img.save(output_path)
    print(f"✓ Créé : {output_path}")


def process_csv():
    """
    Lit le CSV et génère tous les PNG
    """
    # Créer le dossier de sortie
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not os.path.exists(CSV_FILE):
        print(f"⚠ Erreur : {CSV_FILE} introuvable")
        print(f"Créez un fichier {CSV_FILE} avec vos données.")
        return
    
    # Lire le CSV (avec tabulations comme séparateur)
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
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
                os.path.join(OUTPUT_DIR, f"{clean_name}.png")
            )
            
            create_png_2_thema(
                quoi, 
                nom,
                os.path.join(OUTPUT_DIR, f"{clean_name}_thema.png")
            )
            
            create_png_3_qqo(
                quoi, 
                ou, 
                quand, 
                contact, 
                nom,
                os.path.join(OUTPUT_DIR, f"{clean_name}_QQO.png")
            )
            
            count += 1
        
        print(f"\n✅ Terminé ! {count * 3} PNG générés dans {OUTPUT_DIR}/")


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
    
    # Vérifier les polices
    if not os.path.exists(FONT_ICE_CREAM):
        print(f"⚠ Police manquante : {FONT_ICE_CREAM}")
    
    if not os.path.exists(FONT_LIGURINO):
        print(f"⚠ Police manquante : {FONT_LIGURINO}")
    
    # Lancer le traitement
    process_csv()